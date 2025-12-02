from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path, re_path
from apps.dashboard.views import homeView

app_name = 'dashboard'

urlpatterns = [
     #Account
     path('', homeView, name='home')
]