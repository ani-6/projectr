from rest_framework import generics, permissions
from .models import Notification
from .serializers import NotificationSerializer

class NotificationListAPIView(generics.ListAPIView):
    """
    API endpoint that allows authenticated users to view their notifications.
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Return only notifications belonging to the current user, newest first
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at')