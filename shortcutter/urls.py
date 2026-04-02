from rest_framework.routers import DefaultRouter

from .views import ClickViewSet, ShortURLViewSet

router = DefaultRouter()

router.register("short_url", viewset=ShortURLViewSet, basename="short_url")
router.register("click_statistics", viewset=ClickViewSet, basename="click_statistics")

urlpatterns = router.urls
