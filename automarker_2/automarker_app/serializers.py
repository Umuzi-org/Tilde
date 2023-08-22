from rest_framework import serializers


class MarkProjectInputSerializer(serializers.Serializer):
    content_item_id = serializers.IntegerField()
    flavours = serializers.ListField(child=serializers.CharField())
    url = serializers.CharField()

    class Meta:
        fields = ["content_item_id", "flavours", "url"]


class MarkProjectOutputSerializer(serializers.Serializer):
    status = serializers.CharField()
    comments = serializers.CharField()

    class Meta:
        fields = ["status", "comments"]
