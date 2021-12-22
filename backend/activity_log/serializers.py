from rest_framework import serializers
from . import models


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
        # breakpoint()
        return "foo"

    def get_date(self, instance):
        # breakpoint()
        return str(instance["date"])
        # 2021-03-21

    def get_total(self, instance):
        return instance["total"]
