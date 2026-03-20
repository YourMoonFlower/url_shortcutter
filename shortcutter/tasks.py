from celery import shared_task

from .models import ClickModel


@shared_task
def scrapy_data(data: dict):
    country = ...
    ClickModel.objects.create(
        clicked_at=data.get("clicked_at"),
        short_url=data.get("short_url"),
        user_agent=data.get("user_agent"),
        country=country,
    )
