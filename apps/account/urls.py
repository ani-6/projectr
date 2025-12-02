# apps/account/urls.py

from django.urls import path
from apps.account.views import (
    RegisterView, LoginView, LogoutUserView, SettingsView, 
    DeleteAvatarView, ProfileView, ChangePasswordView, resetPassword
)
# Import the new API views
from apps.account.api_views import RegisterAPIView, LoginAPIView, LogoutAPIView, UserProfileAPIView

app_name = 'account'

urlpatterns = [
    # --- Existing Web Views ---
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    path('settings/', SettingsView.as_view(), name='users-settings'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete-avatar/', DeleteAvatarView.as_view(), name='delete-avatar'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', resetPassword.as_view(), name='reset-password'),

    # --- New REST API Endpoints ---
    path('api/register/', RegisterAPIView.as_view(), name='api-register'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('api/profile/', UserProfileAPIView.as_view(), name='api-profile'),
]