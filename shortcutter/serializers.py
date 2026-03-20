from rest_framework import serializers
from .models import ShortURLModel

from url_shortcutter.settings import DOMAIN_NAME


class ShortURLSerializers(serializers.ModelSerializer):
    class Meta:
        model = ShortURLModel
        fields = "__all__"
        read_only_fields = ["uuid", "short_code"]


class ShortURLListSerializers(ShortURLSerializers):
    short_url = serializers.SerializerMethodField(method_name="get_short_url")

    def get_short_url(self, obj: ShortURLModel):
        return DOMAIN_NAME + obj.short_code
