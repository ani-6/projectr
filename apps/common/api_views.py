from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q
from django.contrib.auth.models import User
from .models import Notification
from .serializers import NotificationSerializer
from apps.account.serializers import UserSerializer # Reusing UserSerializer

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

class UserSearchAPIView(APIView):
    """
    API to search users for the notification form.
    Returns top 10 active users if no query provided.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        query = request.GET.get('q', '').strip()
        
        users = User.objects.filter(is_active=True).exclude(id=request.user.id)

        if query:
            users = users.filter(
                Q(username__icontains=query) | 
                Q(first_name__icontains=query) | 
                Q(last_name__icontains=query)
            )
        
        # Limit to 10 results for performance
        users = users[:10]
        
        data = [{'id': u.id, 'text': f"{u.get_full_name()} ({u.username})"} for u in users]
        return Response(data)