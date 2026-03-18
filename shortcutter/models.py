from django.db import models

from uuid import uuid4


class ShortURLModel(models.Model):
    uuid = models.UUIDField(default=uuid4())
    full_url = models.URLField()
    short_url = models.URLField()
