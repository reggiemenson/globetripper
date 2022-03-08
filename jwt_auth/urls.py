from django.urls import path
from .views import RegisterView, LoginView, ProfileView, UserListView, EditDetailView, UserView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view()),
    path('profile', ProfileView.as_view()),
    path('profile/edit/all', EditDetailView.as_view()),
    path('profile/<int:pk>/', UserView.as_view()),
    path('users', UserListView.as_view())
]
