import logging
import hashlib
from datetime import datetime

from django.shortcuts import redirect
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from drf_spectacular.utils import extend_schema
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status
from redis.exceptions import ConnectionError

from shortcutter.tasks import scrapy_click_data, add_task_to_celery

from .models import ShortURLModel, ClickModel
from .schemas import ShortURLSchema, ClickModelGeneralStatisticsResponse
from .serializers import ShortURLSerializers
from .services import ClickServices, ShortURLServices

logger = logging.getLogger("loggers")


class ShortURLViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    lookup_field = "uuid"
    serializer_class = ShortURLSerializers
    queryset = ShortURLModel.objects.all()

    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return super().get_permissions()

    @extend_schema(request=ShortURLSchema())
    def create(self, request, *args, **kwargs):
        serializer = ShortURLSchema(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if type(request.user) is not AnonymousUser:
            data["author"] = request.user
        response = ShortURLSerializers(ShortURLServices.create_short_url(data))
        return Response(response.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(author__uuid=request.user.uuid)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ClickViewSet(GenericViewSet):
    queryset = ClickModel.objects.all()

    @extend_schema(responses=ClickModelGeneralStatisticsResponse)
    @action(methods=["GET"], url_path="get_genetal_statistics", detail=False)
    def get_general_statistics(self, request, *args, **kwargs):
        user_uuid = request.user.uuid
        data = ClickServices.get_general_statistics(user_uuid=user_uuid)
        serializer = ClickModelGeneralStatisticsResponse(data)
        return Response(data=serializer.data)


@extend_schema(methods=["GET"])
def get_redirect_url(request, short_code: str):
    try:
        cache_key = hashlib.sha256(short_code.encode("utf-8")).hexdigest()
        full_url = cache.get(cache_key)
    except ConnectionError:
        full_url = None
        logging.error(msg="Error with Redis connection")

    if not full_url:
        full_url = ShortURLServices.get_full_url(short_code=short_code)

    try:
        add_task_to_celery(
            scrapy_click_data,
            client_ip=request.client_ip,
            clicked_at=datetime.now(),
            short_code=short_code,
            user_agent=request.headers.get("user_agent"),
        )
    except Exception as e:
        logger.error(msg=f"Error with celery task: {e!s}")
    try:
        cache.add(key=cache_key, value=full_url)
    except ConnectionError:
        logger.error(msg="Error with Redis connection")

    return redirect(to=full_url, permanent=False, preserve_request=False)
