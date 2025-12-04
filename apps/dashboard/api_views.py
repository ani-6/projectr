from rest_framework import generics, permissions
from .models import DashboardLink
from .serializers import DashboardLinkSerializer

class DashboardLinkListAPIView(generics.ListAPIView):
    """
    API endpoint to list dashboard links (Quick Access) available to the current user.
    """
    serializer_class = DashboardLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        user_groups = user.groups.all()
        # Fetch links that are active AND associated with any of the user's groups.
        # Uses distinct() to handle cases where a user is in multiple groups assigned to the same link.
        return DashboardLink.objects.filter(
            is_active=True,
            groups__in=user_groups
        ).distinct().order_by('order')