from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from .models import User
from .serializers import (
    LoginSerializer,
    LogoutSerializer,
    RegistrationUserSerializer,
    UserSerializer,
)
from .authentication import AuthenticationMixin


class RegistrationUserViewSet(GenericViewSet):
    serializer_class = RegistrationUserSerializer
    authentication_classes = []
    permission_classes = []

    @extend_schema(request=RegistrationUserSerializer)
    @action(methods=["POST"], detail=False, url_path="registration_user")
    def registration(self, request, *args, **kwargs):
        serialiser = self.serializer_class(data=request.data)
        serialiser.is_valid()
        serialiser.save()

        return Response(
            data={"msg": "successfull user creation"}, status=status.HTTP_201_CREATED
        )


class UserViewSet(GenericViewSet, RetrieveModelMixin):
    lookup_field = "username"
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginViewSet(GenericViewSet, AuthenticationMixin):
    permission_classes = []
    serializer_class = LoginSerializer

    @extend_schema(request=LoginSerializer)
    @action(methods=["POST"], detail=False, url_path="login")
    def login(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        try:
            user = User.objects.get(username=username, password=password)
        except User.DoesNotExist:
            raise ValidationError(detail={"err": "wrong password or username"})

        data = self.for_user(user)

        return Response(data=data, status=status.HTTP_200_OK)


class LogoutViewSet(GenericViewSet, AuthenticationMixin):
    permission_classes = []
    serializer_class = LogoutSerializer

    @extend_schema(request=LogoutSerializer)
    @action(methods=["POST"], detail=False, url_path="logout")
    def logout(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data["token"]

        self.blacklist(token)
        return Response(data="Successful logout", status=status.HTTP_200_OK)
