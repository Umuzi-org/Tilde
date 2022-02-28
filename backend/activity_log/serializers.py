from . import models
from rest_framework import serializers


class ActivityLogDayCountSerializer(serializers.Serializer):
    class Meta:
        fields = [
            "id",
            "date",
            "total",
        ]

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
        model = EventType


class LogEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = LogEntry


class ActivityLogEventTypeSerializer(serializers.Serializer):
    class Meta:
        fields = [
            "id",
            "event_type",
            "timestamp"
        ]
    
    id = serializers.SerializerMethodField("get_id")
    event_type = EventTypeSerializer(read_only=True, many=True)
    activity_log = ArticleSerializer(read_only=True, many=True)

    def get_id(self, instance):
        result = f"timestamp={str(instance['timestamp'])}"
        if instance["filters"]:
            return f"{result}&{instance['filters']}"
        return result