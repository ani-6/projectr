from .models import DashboardLink

def sidebar_links(request):
    """
    Context processor to fetch dashboard links based on user's group.
    """
    if request.user.is_authenticated:
        user_groups = request.user.groups.all()
        # Fetch links that are active AND associated with any of the user's groups.
        # Use distinct() to avoid duplicates if a user is in multiple groups that share a link.
        links = DashboardLink.objects.filter(
            is_active=True,
            groups__in=user_groups
        ).distinct().order_by('order')
        
        return {'dashboard_links': links}
    return {}