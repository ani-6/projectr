from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from django.urls import reverse_lazy
from .models import Profile, UserActivityLog
from apps.common.utils import send_notification_to_user, send_notification_to_group

# --- Existing Profile Signals (Updated with Notifications) ---
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # 1. Create the Profile
        Profile.objects.create(user=instance)

        # 2. Notification 1: Welcome Message
        send_notification_to_user(
            user=instance,
            message=f"Welcome to ProjectR, {instance.username}! We are excited to have you on board.",
            type='success'
        )

        # 3. Notification 2: Update Profile Reminder
        # We use reverse_lazy to get the URL for the settings page
        settings_url = reverse_lazy('account:users-settings')
        send_notification_to_user(
            user=instance,
            message="Don't forget to complete your profile (add a photo and bio)!",
            link=str(settings_url),
            type='info'
        )

        # 4. Notification to 'Manager' Group
        send_notification_to_group(
            group_name='Manager',
            message=f"New User Registration: {instance.username} ({instance.email}) joined the platform.",
            link=f"/admin/auth/user/{instance.id}/change/",  # Link to Django Admin for quick review
            type='info'
        )

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    if hasattr(instance, 'user_profile'):
        instance.user_profile.save()

# --- Login/Logout Tracking Signals ---

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    """
    1. Close any previous stale sessions for this user.
    2. Create a new session log.
    """
    # Close stale sessions
    stale_logs = UserActivityLog.objects.filter(user=user, logout_time__isnull=True)
    for log in stale_logs:
        log.logout_time = log.last_activity
        log.save()

    # Create new log
    ip = get_client_ip(request)
    session_key = request.session.session_key
    
    UserActivityLog.objects.create(
        user=user,
        ip_address=ip,
        session_key=session_key
    )

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    """
    Logs the explicit logout time.
    """
    if user:
        try:
            # Find the active log for this session
            log = UserActivityLog.objects.filter(
                user=user, 
                logout_time__isnull=True
            ).latest('login_time')
            
            log.logout_time = timezone.now()
            log.save()
        except UserActivityLog.DoesNotExist:
            pass