import logging
import requests

from celery import shared_task

from url_shortcutter.settings import GEO_API

from .models import ClickModel

logger = logging.getLogger("")


@shared_task()
def scrapy_click_data(data: dict):
    try:
        url = GEO_API + data.get("client_ip")
        response = requests.get(url=url)
    except Exception as e:
        logger.error(f"Error with getting data from geo_api: {str(e)}")

    if not response.ok:
        logger.error(f"Error with getting data from geo_api: {response.text}")

    country = response.json().get("country")
    ClickModel.objects.create(
        clicked_at=data.get("clicked_at"),
        short_url=data.get("short_url"),
        user_agent=data.get("user_agent"),
        country=country,
    )
    logger.info("Successful getting data from geo_api")
