from . import models
from rest_framework import serializers


class ActivityLogDayCountSerializer(serializers.Serializer):
    class Meta:
        fields = ["id", "date", "total"]

    id = serializers.SerializerMethodField("get_id")
    date = serializers.SerializerMethodField("get_date")
    total = serializers.SerializerMethodField("get_total")

    def get_id(self, instance):
        result = f"date={str(instance['date'])}"
        if instance["filters"]:
            return f"{result}&{instance['filters']}"
        return result

    def get_date(self, instance):
        return str(instance["date"])

    def get_total(self, instance):
        return instance["total"]


class EventTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.EventType
        fields = ["name"]


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.LogEntry
        fields = ["id", "timestamp", "event_type", "actor_user", "effected_user"]


class ActivityLogEventTypeSerializer(serializers.Serializer):
    class Meta:
        fields = ["event_type", "actor_user", "effected_user"]

    timestamp = serializers.DateTimeField(auto_now_add=True)
    event_type = EventTypeSerializer(read_only=True, many=True)
    log_entry = LogEntrySerializer(many=True)
