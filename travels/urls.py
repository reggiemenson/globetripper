from django.urls import path
from .views import BadgesView, IndividualBadgeView, GroupsView, IndividualGroupView, GroupMembershipView, TripsView, IndividualTripView, TownsView

urlpatterns = [
    path('towns/', TownsView.as_view()),
    # path('countries/', CountriesView.as_view()),
    path('groups/', GroupsView.as_view()),
    path('groups/<int:pk>/', IndividualGroupView.as_view()),
    path('groups/<int:pk>/membership/', GroupMembershipView.as_view()),
    path('badges/', BadgesView.as_view()),
    path('badges/<int:pk>/', IndividualBadgeView.as_view()),
    path('trips/', TripsView.as_view()),
    path('trips/<int:pk>/', IndividualTripView.as_view())
]
