from django.urls import path
from .views import RegisterView, LoginView, ProfileView, UserListView, EditDetailView, UserView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('profile/edit/all', EditDetailView.as_view(), name='edit-user'),
    path('profile/<int:pk>/', UserView.as_view(), name='single-user'),
    path('users', UserListView.as_view(), name='users')
]
