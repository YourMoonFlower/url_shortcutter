from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import status

from .models import ShortURLModel
from .serializers import ShortURLSerializers
from .utils import get_short_url


class ShortURLViewSet(ModelViewSet):
    lookup_field = "uuid"
    serializer_class = ShortURLSerializers
    queryset = ShortURLModel.objects.all()

    def create(self, request, *args, **kwargs):
        short_url_data = request.data
        short_url_data.update({"short_url": get_short_url()})
        serializer = self.get_serializer(data=short_url_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )
