from django.db import models

from uuid import uuid4

from url_shortcutter.settings import AUTH_USER_MODEL
from .utils import get_short_code

User = AUTH_USER_MODEL


class ShortURLModel(models.Model):
    uuid = models.UUIDField(default=uuid4, unique=True)
    full_url = models.URLField()
    short_code = models.CharField(max_length=6, unique=True, default=get_short_code)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        to_field="uuid",
        related_name="user",
        null=True,
    )

    class Meta:
        verbose_name = "Short URL"
        verbose_name_plural = "Short URL's"


class ClickModel(models.Model):
    click_at = models.DateTimeField()
    short_url = models.ForeignKey(to=ShortURLModel, on_delete=models.CASCADE)
    user_agent = models.TextField()
    country = models.CharField(max_length=200, null=True)

    class Meta:
        verbose_name = "Information about the click on the short URL"
        verbose_name_plural = "Information about the clicks on the short URL"
        get_latest_by = "click_at"
