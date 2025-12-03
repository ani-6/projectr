from django.urls import path
from .views import MarkNotificationReadView, MarkAllReadView, SessionStatusView, NotificationListView

app_name = 'common'

urlpatterns = [
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('notifications/read-all/', MarkAllReadView.as_view(), name='mark-all-read'),
    path('session-status/', SessionStatusView.as_view(), name='session-status'),
    
    # New URL for the "View All" page
    path('notifications/', NotificationListView.as_view(), name='notification-list'),
]