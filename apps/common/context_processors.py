def notifications(request):
    if request.user.is_authenticated:
        # Fetch unread notifications
        unread_notifications = request.user.notifications.filter(is_read=False)[:5]
        unread_count = request.user.notifications.filter(is_read=False).count()
        
        return {
            'user_notifications': unread_notifications,
            'user_notifications_count': unread_count,
        }
    return {}

def system_health(request):
    """
    Context processor specifically for System Health dashboard access/metrics.
    """
    if request.user.is_authenticated:
        # Check if user is a Manager to see the sidebar link
        is_manager = request.user.groups.filter(name='Managers').exists()
        return {'is_manager': is_manager}
    return {}