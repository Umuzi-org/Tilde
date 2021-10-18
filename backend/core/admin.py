from django.contrib import admin
from . import models
from guardian.admin import GuardedModelAdmin


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
admin.site.site_header = "Tilde Administration"
admin.site.enable_nav_sidebar = False
