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


class ActivityLogEventTypeSerializer(serializers.Serializer):
    class Meta:
        fields = ["id", "timestamp"]

    id = serializers.IntegerField(read_only=True)
    timestamp = serializers.DateTimeField()
