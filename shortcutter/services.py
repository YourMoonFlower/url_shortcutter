from django.db.models import Count

from .exceptions import BadRequest
from .models import ClickModel, ShortURLModel
from .utils import get_short_code


class ClickServices:
    @classmethod
    def get_general_statistics(cls, user_uuid):
        short_urls_id = ShortURLModel.objects.filter(author_id=user_uuid).values_list(
            "id", flat=True
        )
        clicks = ClickModel.objects.filter(short_url_id__in=short_urls_id)
        count_of_short_url = clicks.values("short_url").distinct().count()

        count_of_unique_user_agents = clicks.values("user_agent").distinct().count()

        most_popular_user_agent_data = (
            clicks.values("user_agent")
            .annotate(count=Count("user_agent"))
            .order_by("-count")
            .first()
        )
        most_popular_user_agent = (
            most_popular_user_agent_data["user_agent"]
            if most_popular_user_agent_data
            else ""
        )

        rating_country_data = (
            clicks.filter(country__isnull=False)
            .exclude(country="")
            .values("country")
            .annotate(count_of_users=Count("id"))
            .order_by("-count_of_users")
        )

        rating_country = [
            {"country": item["country"], "count_of_users": item["count_of_users"]}
            for item in rating_country_data
        ]

        return {
            "count_of_short_url": count_of_short_url,
            "count_of_unique_user_agents": count_of_unique_user_agents,
            "most_popular_user_agent": most_popular_user_agent,
            "rating_country": rating_country,
        }


class ShortURLServices:
    @classmethod
    def create_short_url(cls, data: dict) -> ShortURLModel:
        short_code = data.get("alias", get_short_code())
        data.pop("alias", None)
        obj = ShortURLModel.objects.create(short_code=short_code, **data)
        return obj

    @classmethod
    def get_full_url(cls, short_code: str) -> str:
        try:
            obj = ShortURLModel.objects.get(short_code=short_code)
        except ShortURLModel.DoesNotExist:
            raise BadRequest(
                detail=f"Doesn't exist short_url with short_code={short_code}"
            )

        return obj.full_url
