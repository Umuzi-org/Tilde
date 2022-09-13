from . import models
from rest_framework import serializers


class ActivityLogDayCountSerializer(serializers.Serializer):
    class Meta:
        fields = [
            "id",
            "date",
            "event_type",
            "total",
            "filter_by_actor_user",
            "filter_by_effected_user",
        ]

    id = serializers.SerializerMethodField("get_id")
    date = serializers.SerializerMethodField("get_date")
    total = serializers.SerializerMethodField("get_total")
    filter_by_actor_user = serializers.SerializerMethodField("get_filter_by_actor_user")
    filter_by_effected_user = serializers.SerializerMethodField()
    event_type = serializers.SerializerMethodField("get_event_type")

    def get_id(self, instance):
        values = [
            f"{key}={instance[key]}"
            for key in [
                "date",
                "event_type",
                "filter_by_actor_user",
                "filter_by_effected_user",
            ]
        ]

        return "&".join(values)

    def get_date(self, instance):
        return str(instance["date"])

    def get_total(self, instance):
        return instance["total"]

    def get_filter_by_actor_user(self, instance):
        return instance["filter_by_actor_user"]

    def get_filter_by_effected_user(self, instance):
        return instance["filter_by_effected_user"]

    def get_event_type(self, instance):
        return instance["event_type"]


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventType
        fields = ["id", "name", "description"]


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogEntry
        fields = [
            "id",
            "timestamp",
            "event_type",
            "actor_user",
            "effected_user",
            "object_1_content_type_name",
            "object_1_id",
            "object_2_content_type_name",
            "object_2_id",
        ]

    object_1_content_type_name = serializers.SerializerMethodField(
        "get_object_1_content_type_name"
    )
    object_2_content_type_name = serializers.SerializerMethodField(
        "get_object_2_content_type_name"
    )

    def get_object_1_content_type_name(self, instance):
        return (
            instance.object_1_content_type.app_labeled_name
            if instance.object_1_content_type
            else None
        )

    def get_object_2_content_type_name(self, instance):
        return (
            instance.object_2_content_type.app_labeled_name
            if instance.object_2_content_type
            else None
        )
