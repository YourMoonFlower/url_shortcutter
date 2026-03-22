import logging
import requests

from celery import shared_task

from url_shortcutter.settings import GEO_API

from .models import ClickModel, ShortURLModel

logger = logging.getLogger("")


@shared_task()
def scrapy_click_data(data: dict):
    try:
        url = GEO_API + data.get("client_ip")
        response = requests.get(url=url)
    except Exception as e:
        logger.error(f"Error with getting data from geo_api: {str(e)}")

    try:
        short_url = ShortURLModel.objects.get(short_code=data.get("short_code"))
    except ShortURLModel.DoesNotExist:
        logger.error("short_url does not exist")
        raise

    if not response.ok:
        logger.error(f"Error with getting data from geo_api: {response.text}")

    country = response.json().get("country")
    ClickModel.objects.create(
        click_at=data.get("clicked_at"),
        short_url=short_url,
        user_agent=data.get("user_agent"),
        country=country,
    )
    logger.info("Successful getting data from geo_api")
