from django.urls import path
from .views import MarkNotificationReadView, MarkAllReadView, SessionStatusView

app_name = 'common'

urlpatterns = [
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('notifications/read-all/', MarkAllReadView.as_view(), name='mark-all-read'),
    
    # New Session Check Endpoint
    path('session-status/', SessionStatusView.as_view(), name='session-status'),
]