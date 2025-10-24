# accounts/urls.py
from django.urls import path
from .views import RegisterView, UserDetailView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('me/', UserDetailView.as_view(), name='auth_user_detail'),
    path('logout/', LogoutView.as_view(), name='auth_logout'),
]