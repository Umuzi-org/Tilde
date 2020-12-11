from django.contrib import admin
from . import models
from guardian.admin import GuardedModelAdmin


class TeamMembershipInline(admin.StackedInline):  # or admin.StackedInline
    model = models.TeamMembership


@admin.register(models.Team)
class TeamAdmin(GuardedModelAdmin):
    list_display = ["name", "active"]
    list_filter = ["active"]
    inlines = (
        TeamMembershipInline,
        # RecruitProjectInline,
    )


admin.site.register(models.ProductTeam)
admin.site.register(models.UserProfile)
admin.site.register(models.RecruitCohort)
admin.site.register(models.EmployerPartner)

admin.site.site_header = "Tilde Administration"
