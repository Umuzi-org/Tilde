from django.contrib import admin
from . import models
from guardian.admin import GuardedModelAdmin


class UserSetInline(admin.TabularInline):
    model = models.User.groups.through
    raw_id_fields = ("user",)


def deactivate_team_members(TeamAdminInstance, request, queryset: object):
    for team in queryset:
        for team_member in team.active_users:
            team_member.active = False
            team_member.save()


@admin.register(models.Team)
class TeamAdmin(GuardedModelAdmin):
    list_display = ["name", "active"]
    list_filter = ["active"]
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
admin.site.site_header = "Tilde Administration"
admin.site.enable_nav_sidebar = False
