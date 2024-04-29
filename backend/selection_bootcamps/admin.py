from django.contrib import admin

from . import models


@admin.register(models.Bootcamp)
class BootcampAdmin(admin.ModelAdmin):
    list_display = [
        "__str__",
        "start_date",
        "end_date",
        "active",
    ]
    list_filter = ["active"]
    list_editable = ["active"]


@admin.register(models.ProvisionalGroup)
class ProvisionalGroupAdmin(admin.ModelAdmin):
    list_display = ["__str__", "start_date", "paid", "group_type", "active"]

    list_filter = ["paid", "group_type", "active"]
    list_editable = ["active"]
