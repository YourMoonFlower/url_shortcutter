from rest_framework import serializers


class ShortURLSchema(serializers.Serializer):
    full_url = serializers.URLField()
