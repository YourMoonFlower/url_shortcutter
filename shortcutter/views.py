from datetime import datetime

from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.models import AnonymousUser
from drf_spectacular.utils import extend_schema
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin
from rest_framework.response import Response
from rest_framework import status

from .models import ShortURLModel
from .schemas import ShortURLSchema
from .serializers import ShortURLSerializers, ShortURLListSerializers
from .tasks import scrapy_click_data


class ShortURLViewSet(GenericViewSet, CreateModelMixin, ListModelMixin):
    lookup_field = "uuid"
    serializer_class = ShortURLSerializers
    queryset = ShortURLModel.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return ShortURLListSerializers
        return ShortURLSerializers

    @extend_schema(request=ShortURLSchema())
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if request.user is not AnonymousUser:
            kwargs["author"] = request.user
        self.perform_create(serializer, **kwargs)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer, **kwargs):
        obj = serializer.save(**kwargs)
        return obj

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset().filter(author__uuid=request.user.uuid)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


@extend_schema(methods=["GET"])
def get_redirect_url(request, short_code: str):
    obj = get_object_or_404(ShortURLModel, short_code=short_code)
    scrapy_data = {
        "client_ip": request.client_ip,
        "clicked_at": datetime.now(),
        "short_code": obj.short_code,
        "user_agent": request.headers.get("user_agent"),
    }
    scrapy_click_data.delay(scrapy_data)
    return redirect(to=obj.full_url, permanent=False, preserve_request=False)
