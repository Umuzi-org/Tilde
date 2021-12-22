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
        return "foo"

    def get_date(self, instance):
        return str(instance["date"])

    def get_total(self, instance):
        return instance["total"]
