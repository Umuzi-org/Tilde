from django.contrib import admin
from . import models
from guardian.admin import GuardedModelAdmin
from rest_framework.decorators import action
from core.permissions import IsStaffUser


class UserSetInline(admin.TabularInline):
    model = models.User.groups.through
    raw_id_fields = ("user",)

@action(
    detail=True,
    permission_classes=[IsStaffUser]
)
def delete_all_inactive_teams(instance, request, queryset: object):
    return [team.delete() for team in queryset if not team.active]


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
    actions = [delete_all_inactive_teams]


admin.site.register(models.UserProfile)
admin.site.site_header = "Tilde Administration"
admin.site.enable_nav_sidebar = False
