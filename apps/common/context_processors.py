def notifications(request):
    if request.user.is_authenticated:
        # Fetch unread notifications
        unread_notifications = request.user.notifications.filter(is_read=False)[:5]
        unread_count = request.user.notifications.filter(is_read=False).count()
        return {
            'user_notifications': unread_notifications,
            'user_notifications_count': unread_count
        }
    return {}