from rest_framework import serializers


class ShortURLSchema(serializers.Serializer):
    full_url = serializers.URLField()
    alias = serializers.CharField(required=False, max_length=10)


class CountUsersFromCountries(serializers.Serializer):
    country = serializers.CharField()
    count_of_users = serializers.IntegerField()


class ClickModelGeneralStatisticsResponse(serializers.Serializer):
    count_of_short_url = serializers.IntegerField()
    count_of_unique_user_agents = serializers.IntegerField()
    most_popular_user_agent = serializers.CharField()
    rating_country = serializers.ListField(child=CountUsersFromCountries())
