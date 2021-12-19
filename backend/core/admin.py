from django.contrib import admin
from . import models
from guardian.admin import GuardedModelAdmin
from adminsortable2.admin import SortableInlineAdminMixin


class UserSetInline(admin.TabularInline):
    model = models.User.groups.through
    raw_id_fields = ("user",)


@admin.register(models.Team)
class TeamAdmin(GuardedModelAdmin):
    def deactivate_team_members(self, request, queryset: object):
        for team in queryset:
            for team_member in team.active_users:
                team_member.active = False
                team_member.save()

    list_display = ["name", "active"]
    list_filter = ["active"]
    search_fields = ["name"]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "active",
                    "sponsor_organisation",
                    "school_organisation",
                    # "created_date",
                )
            },
        ),
    )
    inlines = [UserSetInline]
    actions = [deactivate_team_members]


admin.site.register(models.UserProfile)


class StreamCurriculumInline(
    SortableInlineAdminMixin, admin.TabularInline
):  # or admin.StackedInline
    model = models.StreamCurriculum


@admin.register(models.Stream)
class StreamAdmin(admin.ModelAdmin):
    inlines = (StreamCurriculumInline,)


@admin.register(models.StreamRegistration)
class StreamRegistrationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "name",
        "start_date",
        "latest_end_date",
        "ideal_end_date",
        "active",
    ]
    list_filter = ["active", "stream", "employer_partner"]
    search_fields = ["name", "user__email"]


admin.site.site_header = "Tilde Administration"
admin.site.enable_nav_sidebar = False
