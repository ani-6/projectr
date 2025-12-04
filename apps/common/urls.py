from django.urls import path
from .views import MarkNotificationReadView, MarkAllReadView, SessionStatusView, NotificationListView
from .api_views import NotificationListAPIView

app_name = 'common'

urlpatterns = [
    # --- Existing Web Views ---
    path('notifications/<int:pk>/read/', MarkNotificationReadView.as_view(), name='mark-notification-read'),
    path('notifications/read-all/', MarkAllReadView.as_view(), name='mark-all-read'),
    path('session-status/', SessionStatusView.as_view(), name='session-status'),
    path('notifications/', NotificationListView.as_view(), name='notification-list'),

    # --- New REST API Endpoints ---
    path('api/notifications/', NotificationListAPIView.as_view(), name='api-notification-list'),
]