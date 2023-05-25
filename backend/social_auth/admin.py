from django.contrib import admin

from . import models


@admin.register(models.SocialProfile)
class SocialProfileAdmin(admin.ModelAdmin):
    search_fields = ("user__email", "github_name")
