from django.contrib import admin
from . import models
from guardian.admin import GuardedModelAdmin


class UserSetInline(admin.TabularInline):
    model = models.User.groups.through
    raw_id_fields = ("user",)

#@admin.ModelAdmin.actions(description='Not doing much right now')
#def make_inactive(modeladmin, request, queryset):
    #queryset.update(active=False)
def make_inactive(request, queryset):
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
    actions = [make_inactive]


admin.site.register(models.UserProfile)
admin.site.site_header = "Tilde Administration"
admin.site.enable_nav_sidebar = False
