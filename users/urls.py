from rest_framework.routers import DefaultRouter

from .views import RegistrationUserViewSet, UserViewSet, LoginViewSet, LogoutViewSet

router = DefaultRouter()

router.register(
    "registration", viewset=RegistrationUserViewSet, basename="registration"
)
router.register("user", viewset=UserViewSet, basename="user")
router.register("auth", viewset=LoginViewSet, basename="login")
router.register("auth", viewset=LogoutViewSet, basename="logout")

urlpatterns = router.urls
