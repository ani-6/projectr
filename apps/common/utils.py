import time
import platform
from datetime import timedelta
from django.utils import timezone
from django.db import connection
from django.contrib.auth.models import User, Group
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
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
        
        if not users.exists():
            print(f"DEBUG: Group '{group_name}' has no users. No notifications sent.")
            return False

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
        print(f"DEBUG: Successfully sent '{message}' to {len(notifications)} users in group '{group_name}'.")
        return True
    except Group.DoesNotExist:
        print(f"DEBUG: Group '{group_name}' does not exist.")
        return False

def mark_all_as_read(user):
    """Marks all notifications as read for a user"""
    user.notifications.filter(is_read=False).update(is_read=True)

# --- System Health Utilities ---

def check_service_status():
    """
    Performs the raw checks for Database and Redis.
    Returns a dict with status strings and latency numbers.
    """
    # 1. Database Check
    db_status = 'Offline'
    db_latency = 0
    try:
        start = time.time()
        connection.ensure_connection()
        if connection.is_usable():
            db_status = 'Online'
        end = time.time()
        db_latency = round((end - start) * 1000, 2)
    except Exception as e:
        print(f"DEBUG: DB Check Failed: {e}")

    # 2. Redis Check
    redis_status = 'Offline'
    redis_latency = 0
    try:
        layer = get_channel_layer()
        start = time.time()
        # Simple ping operation to Redis channel layer
        async_to_sync(layer.group_add)("health_check", "health_check_channel")
        redis_status = 'Online'
        end = time.time()
        redis_latency = round((end - start) * 1000, 2)
    except Exception as e:
        print(f"DEBUG: Redis Check Failed: {e}")

    return {
        'db_status': db_status,
        'db_latency': db_latency,
        'redis_status': redis_status,
        'redis_latency': redis_latency,
    }

def notify_if_offline(service_name, status):
    """
    Sends notifications if a service is Offline, with rate limiting.
    """
    if status == 'Online':
        print(f"DEBUG: {service_name} is Online. Notification skipped.")
        return

    # Define messages
    manager_msg = f"Critical Alert: {service_name} Service is Offline"
    user_msg = "System Alert: You may experience system slowness or malfunctioning."

    # Anti-Spam: Check if a similar alert was sent in the last 30 minutes
    recent_notification = Notification.objects.filter(
        message=manager_msg,
        created_at__gte=timezone.now() - timedelta(minutes=30)
    ).exists()

    if not recent_notification:
        print(f"DEBUG: {service_name} is Offline. Sending notifications...")
        # Notify Managers
        send_notification_to_group(
            group_name='Managers', 
            message=manager_msg, 
            link='/common/system/health/', 
            type='danger'
        )
        
        # Notify All Users
        send_notification_to_group(
            group_name='Users', 
            message=user_msg, 
            type='warning'
        )
    else:
        print(f"DEBUG: Alert for {service_name} suppressed due to rate limiting (alert sent < 30 mins ago).")

def perform_health_check_and_notify():
    """
    Orchestrates the check and notification process.
    Returns metrics dict for use in views.
    """
    metrics = check_service_status()
    
    # Trigger Notifications
    notify_if_offline('Database', metrics['db_status'])
    notify_if_offline('Redis', metrics['redis_status'])
    
    # Add Server Info
    metrics['server_info'] = {
        'status': 'Online',
        'system': platform.system(),
        'node': platform.node(),
        'release': platform.release(),
        'python': platform.python_version(),
        'machine': platform.machine()
    }
    metrics['api_status'] = 'Online'
    
    return metrics