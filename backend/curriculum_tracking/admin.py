from django.contrib import admin, messages
from . import models
from core import models as core_models
from adminsortable2.admin import SortableInlineAdminMixin
from automarker import models as automarker_models
from .forms import BulkAddLearnersToTeamForm
from .helpers import add_users_to_team, remove_leading_and_trailing_whitespace
from django.shortcuts import render, redirect
from django.urls import path


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

    actions = ["bulk_activate_users", "bulk_deactivate_users"]

    def bulk_activate_users(self, request, users):
        users.update(active=True)

    bulk_activate_users.short_description = "Activate selected users"

    def bulk_deactivate_users(self, request, users):
        users.update(active=False)

    bulk_deactivate_users.short_description = "Deactivate selected users"


class BulkAddLearnersToTeamAdmin(admin.AdminSite):
    site_header = "Tilde administration"
    site_title = "Bulk add learners to team"

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "bulk_add_learners_to_team/",
                self.admin_view(self.bulk_add_learners_to_team_view),
                name="bulk_add_learners_to_team",
            ),
        ]
        return urls + custom_urls

    def bulk_add_learners_to_team_view(self, request):
        if request.method == "POST":
            team_name = request.POST["team_name"]
            email_addresses = request.POST["email_addresses"]
            form = BulkAddLearnersToTeamForm(request.POST)
            if form.is_valid():
                team_name = remove_leading_and_trailing_whitespace(team_name)
                add_users_to_team(team_name, [email_addresses])
                messages.success(
                    request, "You have successfully added learners to a team"
                )
                return redirect("bulk_add_learners_to_team")
        else:
            form = BulkAddLearnersToTeamForm()

        context = {"form": form}
        return render(request, "admin/bulk_add_learners_to_team.html", context)


custom_admin_site = BulkAddLearnersToTeamAdmin(name="admin")


admin.site.register(User, UserAdmin)
admin.site.register(models.WorkshopAttendance)
admin.site.register(models.TopicProgress)

from django.contrib.auth.models import Group

admin.site.unregister(Group)
