from rest_framework.routers import DefaultRouter

from .views import ShortURLViewSet

router = DefaultRouter()

router.register("short_url", viewset=ShortURLViewSet, basename="short_url")

urlpatterns = router.urls
