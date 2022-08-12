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
    filter_by_effected_user = serializers.SerializerMethodField(
        "get_filter_by_effected_user"
    )

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


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventType
        fields = ["id", "name", "description"]
