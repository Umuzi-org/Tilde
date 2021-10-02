from django.contrib import admin
from . import models
from guardian.admin import GuardedModelAdmin
from rest_framework.decorators import action
from core.permissions import IsStaffUser


class UserSetInline(admin.TabularInline):
    model = models.User.groups.through
    raw_id_fields = ("user",)


@action(
    methods=['post'],
    detail=True,
    permission_classes=[IsStaffUser],
    get_objects=models.Team.users
)
def deactivate_all_inactive_team_members(queryset, something):
    members_in_team = models.Team.active_users
    breakpoint()
    queryset.update(active=False)

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
    actions = [deactivate_all_inactive_team_members]


admin.site.register(models.UserProfile)
admin.site.site_header = "Tilde Administration"
admin.site.enable_nav_sidebar = False
