from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from . import models
from core import models as core_models
from adminsortable2.admin import SortableInlineAdminMixin
from automarker import models as automarker_models
from guardian.shortcuts import get_objects_for_user


class ContentItemAutoMarkerConfigAdmin(admin.TabularInline):
    model = automarker_models.ContentItemAutoMarkerConfig


class ContentItemOrderPostAdmin(admin.TabularInline):
    model = models.ContentItem.prerequisites.through
    fk_name = "post"


class ContentItemOrderPreAdmin(admin.TabularInline):
    model = models.ContentItem.unlocks.through
    fk_name = "pre"


@admin.register(models.ContentItem)
class ContentItemAdmin(admin.ModelAdmin):
    inlines = (
        ContentItemOrderPostAdmin,
        ContentItemOrderPreAdmin,
        ContentItemAutoMarkerConfigAdmin,
    )

    list_display = ["content_type", "title", "tag_list"]
    search_fields = ["title"]
    list_filter = ["content_type"]
    ordering = ["title"]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related("tags")

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.tags.all())

    # def label(self, obj):
    #     return f"[{obj.content_type_nice}] {obj}"


class CurriculumContentInline(
    SortableInlineAdminMixin, admin.TabularInline
):  # or admin.StackedInline
    model = models.CurriculumContentRequirement


@admin.register(core_models.Curriculum)
class CurriculumAdmin(admin.ModelAdmin):
    inlines = (CurriculumContentInline,)
    ordering = ["name"]
    search_fields = ["name"]


class RecruitProjectReviewInLine(admin.TabularInline):
    model = models.RecruitProjectReview
    extra = 0


@admin.register(models.RecruitProject)
class RecruitProjectAdmin(admin.ModelAdmin):
    inlines = (RecruitProjectReviewInLine,)
    list_filter = ["content_item"]


@admin.register(models.AgileCard)
class AgileCardAdmin(admin.ModelAdmin):
    list_display = [
        "order",
        "status",
        "content_type",
        "content_item",
    ]
    list_filter = ["status", "assignees"]
    ordering = ["order"]


@admin.register(models.ReviewTrust)
class ReviewTrustAdmin(admin.ModelAdmin):
    list_display = ["__str__", "user"]
    search_fields = ["user__email"]


@admin.register(models.RecruitProjectReview)
class RecruitProjectReviewAdmin(admin.ModelAdmin):
    # list_filter = ["content_item"]
    list_display = ["recruit_project", "status", "reviewer_user"]
    ordering = ("-timestamp",)
    #     "order",
    #     "status",
    #     "content_type",
    #     "content_item",
    # ]
    # list_filter = ["content_item"]


@admin.register(models.CourseRegistration)
class CourseRegistrationAdmin(admin.ModelAdmin):
    list_display = ["__str__", "registration_date", "active"]
    ordering = ("-registration_date",)


from core.models import User


from django.contrib.auth.forms import AdminPasswordChangeForm

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from core.admin_forms import (
    UserAdminCreationForm,
    UserAdminChangeForm,
)


class CourseRegistrationInline(
    SortableInlineAdminMixin, admin.TabularInline
):  # or admin.StackedInline
    model = models.CourseRegistration


# class GroupInline(admin.TabularInline):
#     model = core_models.Group


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserAdminChangeForm
    add_form = UserAdminCreationForm
    change_password_form = AdminPasswordChangeForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    inlines = (
        CourseRegistrationInline,
        # GroupInline,
        # RecruitProjectInline,
    )
    list_display = ("email", "is_superuser", "active")
    list_filter = (
        "is_superuser",
        "is_staff",
        "active",
    )
    fieldsets = (
        ("Personal info", {"fields": ("first_name", "last_name")}),
        (None, {"fields": ("email", "password")}),
        ("Permissions", {"fields": ("is_superuser", "is_staff", "active", "groups")}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {"classes": ("wide",), "fields": ("email", "password1", "password2")}),
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email", "first_name", "last_name")
    filter_horizontal = ()
    filter_horizontal = (
        "groups",
        # "user_permissions",
    )

    actions = ["bulk_activate_users", "bulk_deactivate_users", "invite_to_github_repos"]

    def bulk_activate_users(self, request, users):
        users.update(active=True)

    bulk_activate_users.short_description = "Activate selected users"

    def bulk_deactivate_users(self, request, users):
        users.update(active=False)

    bulk_deactivate_users.short_description = "Deactivate selected users"

    def invite_to_github_repos(self, request, users):
        permitted_teams_for_users = self._get_permitted_teams_for_users(users)
        if request.POST.get("post", None):
            from long_running_request_actors import (
                invite_collaborators_for_team_projects as actor,
            )

            for team_name in permitted_teams_for_users:
                actor.send_with_options(kwargs={"team_name": team_name})
            messages.add_message(
                request,
                messages.INFO,
                f"Adding user(s) as collaborators in the background",
            )
        else:
            opts = self.model._meta
            request.current_app = self.admin_site.name

            return TemplateResponse(
                request,
                "admin/invite_to_github_repos_confirm.html",
                {
                    **self.admin_site.each_context(request),
                    "title": _("Are you sure?"),
                    "opts": opts,
                    "app_label": opts.app_label,
                    "permitted_teams_for_users": permitted_teams_for_users,
                    "queryset": users,
                    "action_checkbox_name": ACTION_CHECKBOX_NAME,
                },
            )

    def _get_permitted_teams_for_users(self, users) -> list:
        teams = []
        for user in users:
            for team in get_objects_for_user(
                user,
                core_models.Team.PERMISSION_REPO_COLLABORATER_AUTO_ADD,
                klass=core_models.Team.objects.filter(active=True),
            ):
                teams.append(team.name)
        return sorted(set(teams))


admin.site.register(User, UserAdmin)
admin.site.register(models.WorkshopAttendance)
admin.site.register(models.TopicProgress)

from django.contrib.auth.models import Group

admin.site.unregister(Group)
