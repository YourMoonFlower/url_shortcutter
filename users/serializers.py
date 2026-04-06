import jwt
from datetime import datetime
from rest_framework import serializers

from url_shortcutter.settings import SIMPLE_JWT
from shortcutter.models import ShortURLModel
from shortcutter.serializers import ShortURLSerializers

from .models import User


class UserSerializer(serializers.ModelSerializer):
    short_urls = serializers.SerializerMethodField("get_short_urls")

    class Meta:
        model = User
        exclude = ["groups", "user_permissions"]

    def get_short_urls(self, obj):
        short_url_list_by_user = ShortURLModel.objects.filter(author=obj)
        return ShortURLSerializers(short_url_list_by_user, many=True).data


class RegistrationUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "password", "email"]

    def create(self, data: dict) -> User:
        password = data.pop("password")
        user = super().create(data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255, trim_whitespace=False)
    password = serializers.CharField(
        max_length=255, write_only=True, trim_whitespace=False
    )


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate_token(self, token):
        if not token:
            serializers.ValidationError(detail="token is None")

        try:
            token = jwt.decode(token, options={"verify_signature": False})
        except jwt.exceptions.DecodeError:
            serializers.ValidationError(detail="token is not valid")

        token_exp = token.get("exp")
        if not token_exp:
            raise serializers.ValidationError("token is not valid")
        if datetime.fromtimestamp(token_exp) < (
            datetime.now() - SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
        ):
            raise serializers.ValidationError("token is not expired")

        return token
