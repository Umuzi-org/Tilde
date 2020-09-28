from django.contrib import admin
from . import models


# class AttendanceAdmin(admin.ModelAdmin):
#     list_display = ('user', 'status', 'timestamp')

# Register your models here.
# admin.site.register(Attendance, AttendanceAdmin)
admin.site.register(models.MorningAttendance)
admin.site.register(models.AfternoonAttendance)
admin.site.register(models.EveningAttendance)
admin.site.register(models.Leave)
