from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    BadgeViewSet,
    GroupsView,
    IndividualGroupView,
    GroupMembershipView,
    TripsView,
    IndividualTripView,
    TownViewSet,
)

router = DefaultRouter()
router.register(r"towns", TownViewSet, basename="towns-v1")
router.register(r"badges", BadgeViewSet, basename="badges-v1")

urlpatterns = [
    path("groups/", GroupsView.as_view()),
    path("groups/<int:pk>/", IndividualGroupView.as_view()),
    path("groups/<int:pk>/membership/", GroupMembershipView.as_view()),
    path("trips/", TripsView.as_view()),
    path("trips/<int:pk>/", IndividualTripView.as_view()),
] + router.urls
