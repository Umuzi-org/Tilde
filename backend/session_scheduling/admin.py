from . import models

from django.contrib import admin


@admin.register(models.SessionType)
class SessionTypeAdmin(admin.ModelAdmin):
    readonly_fields = ["name"]
