from datetime import datetime

from django.shortcuts import redirect, get_object_or_404
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
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


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
