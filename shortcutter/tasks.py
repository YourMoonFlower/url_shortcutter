import logging
import requests

from celery import shared_task

from url_shortcutter.settings import GEO_API

from .models import ClickModel, ShortURLModel

logger = logging.getLogger("File_Logging")


@shared_task()
def scrapy_click_data(*args, **kwargs):
    try:
        url = GEO_API + kwargs.get("client_ip")
        response = requests.get(url=url)
    except Exception as e:
        logger.error(f"Error with getting data from geo_api: {str(e)}")

    try:
        short_url = ShortURLModel.objects.get(short_code=kwargs.get("short_code"))
    except ShortURLModel.DoesNotExist:
        logger.error("short_url does not exist")
        raise

    if not response.ok:
        logger.error(f"Error with getting data from geo_api: {response.text}")

    country = response.json().get("country")
    ClickModel.objects.create(
        click_at=kwargs.get("clicked_at"),
        short_url=short_url,
        user_agent=kwargs.get("user_agent"),
        country=country,
    )
    logger.info("Successful getting data from geo_api")


def add_task_to_celery(task, **kwargs):
    task.delay(**kwargs)
