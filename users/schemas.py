from rest_framework import serializers


class LoginSchema(serializers.Serializer):
    username = serializers.CharField(max_length=255, trim_whitespace=False)
    password = serializers.CharField(
        max_length=255, write_only=True, trim_whitespace=False
    )
