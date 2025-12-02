from django.urls import path
from apps.dashboard.views import homeView, user_dashboard, manager_dashboard

app_name = 'dashboard'

urlpatterns = [
     # The root path now acts as a dispatcher
     path('', homeView, name='home'),
     
     # Explicit paths for the separate dashboards
     path('user/', user_dashboard, name='user-dashboard'),
     path('manager/', manager_dashboard, name='manager-dashboard'),
]