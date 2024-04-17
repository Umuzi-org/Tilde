from django.contrib import admin

from . import models


@admin.register(models.Bootcamp)
class BootcampAdmin(admin.ModelAdmin):
    pass


@admin.register(models.ProvisionalGroup)
class ProvisionalGroupAdmin(admin.ModelAdmin):
    pass
