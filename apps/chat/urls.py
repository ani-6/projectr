from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='index'),
    path('api/recent/', views.get_recent_contacts, name='api-recent'), # New endpoint
    path('api/users/', views.get_user_list, name='api-users'),
    path('api/history/<int:user_id>/', views.get_chat_history, name='api-history'),
]