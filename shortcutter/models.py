from django.db import models

from uuid import uuid4

from .utils import get_short_code


class ShortURLModel(models.Model):
    uuid = models.UUIDField(default=uuid4())
    full_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True, default=get_short_code())

    class Meta:
        verbose_name = "Short URL"
        verbose_name_plural = "Short URL's"


class ClickModel(models.Model):
    click_at = models.DateTimeField(auto_now_add=True)
    short_url = models.ForeignKey(to=ShortURLModel, on_delete=models.CASCADE)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    country = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name = "Information about the click on the short URL"
        verbose_name_plural = "Information about the clicks on the short URL"
        get_latest_by = "click_at"
