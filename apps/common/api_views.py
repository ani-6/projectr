from rest_framework import generics, permissions
from rest_framework.pagination import PageNumberPagination
from .models import Notification
from .serializers import NotificationSerializer

class StandardResultsSetPagination(PageNumberPagination):
    """
    Custom pagination to return 10 items per page.
    """
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100

class NotificationListAPIView(generics.ListAPIView):
    """
    API endpoint that allows authenticated users to view their notifications.
    Supports pagination (10 items per page).
    """
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_queryset(self):
        # Return only notifications belonging to the current user, newest first
        return Notification.objects.filter(recipient=self.request.user).order_by('-created_at', '-id')