from . import models

from django.contrib import admin


@admin.register(models.SessionType)
class SessionTypeAdmin(admin.ModelAdmin):
    readonly_fields = ["name"]
    fields = ["name", "description", "duration_minutes", "event_title", "event_copy"]


@admin.register(models.Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ["__str__", "due_date", "facilitator", "start_time", "is_cancelled"]
    list_filter = ["session_type", "extra_title_text", "is_cancelled"]
    readonly_fields = ["created_date", "end_time"]
    filter_vertical = ("attendees", "guest_facilitators")
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "session_type",
                    "extra_title_text",
                    "flavours",
                    "is_cancelled",
                ],
            },
        ),
        (
            "People",
            {
                "fields": ["facilitator", "guest_facilitators", "attendees"],
                "classes": [],
            },
        ),
        (
            "Dates and times",
            {"fields": ["created_date", "due_date", "start_time", "end_time"]},
        ),
        ("Related", {"fields": ["related_object_content_type", "related_object_id"]}),
    ]
