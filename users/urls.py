from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import RegisterView, LoginView, UserViewSet, ProfileViewSet

profile_detail = ProfileViewSet.as_view(
    {"get": "retrieve", "put": "update", "delete": "destroy"}
)
profile_town_detail = ProfileViewSet.as_view({"put": "town_update"})

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users-v1")
# urlpatterns = router.urls
urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("profile", profile_detail, name="profile-v1"),
    path("profile/town", profile_town_detail, name="profile-v1-town"),
] + router.urls
