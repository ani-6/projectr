from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='index'),
    path('api/recent/', views.get_recent_contacts, name='api-recent'),
    path('api/users/', views.get_user_list, name='api-users'),
    path('api/history/<int:user_id>/', views.get_chat_history, name='api-history'),
    path('api/redis-status/', views.check_redis_status, name='api-redis-status'), # New Check Endpoint
]