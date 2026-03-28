import logging
from rest_framework_simplejwt.tokens import BlacklistMixin, Token
# from rest_framework_simplejwt.models import O

from url_shortcutter.settings import SIMPLE_JWT
from .models import User


class CustomToken(Token):
    @classmethod
    def for_user(cls, user):
        token = super().for_user(user)
        token["uuid"] = str(user.uuid)
        token["username"] = user.username
        return token


class CustomAccessToken(CustomToken):
    token_type = "access"
    lifetime = SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"]


class CustomRefreshToken(BlacklistMixin, CustomToken):
    token_type = "refresh"
    lifetime = SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"]
    no_copy_claims = ("exp", "jti", "token_type")

    access_token_class = CustomAccessToken

    @property
    def access_token(self) -> CustomAccessToken:
        access = self.access_token_class()
        access.set_exp(from_time=self.current_time)

        no_copy = self.no_copy_claims
        for claim, value in self.payload.items():
            if claim in no_copy:
                continue
            access[claim] = value

        return access


class AuthenticationMixin:
    @classmethod
    def for_user(cls, user: User) -> CustomRefreshToken:
        token = CustomRefreshToken.for_user(user)

        return {
            "refresh_token": str(token),
            "access_token": str(token.access_token),
            "username": user.username,
        }

    @classmethod
    def blacklist(cls, token):
        try:
            CustomRefreshToken(token).blacklist()
        except Exception as e:
            logging.error(msg=f"Error with logout user: {e!s}")
            raise Exception
