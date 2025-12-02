from django.contrib.auth.models import User, Group
from .models import Notification

def send_notification_to_user(user, message, link=None, type='info'):
    """
    Sends a notification to a specific user.
    """
    Notification.objects.create(
        recipient=user,
        message=message,
        link=link,
        notification_type=type
    )

def send_notification_to_group(group_name, message, link=None, type='info'):
    """
    Sends a notification to all members of a specific group (e.g., 'Managers').
    """
    try:
        group = Group.objects.get(name=group_name)
        users = group.user_set.all()
        
        notifications = []
        for user in users:
            notifications.append(
                Notification(
                    recipient=user, 
                    message=message, 
                    link=link, 
                    notification_type=type
                )
            )
        
        # Bulk create for performance
        Notification.objects.bulk_create(notifications)
        return True
    except Group.DoesNotExist:
        print(f"Group '{group_name}' does not exist.")
        return False

def mark_all_as_read(user):
    """Marks all notifications as read for a user"""
    user.notifications.filter(is_read=False).update(is_read=True)