from rest_framework import serializers


class OAuthOneTimeTokenSerialiser(serializers.Serializer):
    code = serializers.CharField(required=True, max_length=100)
    provider = serializers.CharField(required=True, max_length=50)
