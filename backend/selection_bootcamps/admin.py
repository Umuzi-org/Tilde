from django.contrib import admin

from . import models


@admin.register(models.Bootcamp)
class BootcampAdmin(admin.ModelAdmin):
    pass
