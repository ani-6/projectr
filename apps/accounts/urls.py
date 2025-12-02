from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from apps.accounts.views import (
    RegisterView,
    LoginView,
    LogoutUserView,
    SettingsView,
    DeleteAvatarView,
    ProfileView,
    ChangePasswordView,
    resetPassword
)

app_name = 'account'

urlpatterns = [
    # Authentication
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutUserView.as_view(), name='logout'),
    
    # Profile Management
    path('settings/', SettingsView.as_view(), name='users-settings'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('delete-avatar/', DeleteAvatarView.as_view(), name='delete-avatar'),
    
    # Password Management
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('reset-password/', resetPassword.as_view(), name='reset-password'),
]