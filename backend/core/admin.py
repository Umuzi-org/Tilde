from django.contrib import admin
from . import models


class UserGroupMembershipInline(admin.StackedInline):  # or admin.StackedInline
    model = models.UserGroupMembership


@admin.register(models.UserGroup)
class UserGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "active"]
    list_filter = ["active"]
    inlines = (
        UserGroupMembershipInline,
        # RecruitProjectInline,
    )


admin.site.register(models.ProductTeam)
admin.site.register(models.UserProfile)
admin.site.register(models.RecruitCohort)
admin.site.register(models.EmployerPartner)

admin.site.site_header = "Tilde Administration";
