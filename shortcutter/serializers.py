from rest_framework.serializers import ModelSerializer
from .models import ShortURLModel


class ShortURLSerializers(ModelSerializer):
    class Meta:
        model = ShortURLModel
        fields = "__all__"
        read_only_fields = ["uuid", "short_url"]
