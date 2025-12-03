from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.utils import timezone
from .models import Profile, UserActivityLog

# --- Existing Profile Signals ---
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

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
    # Close stale sessions:
    # Any log for this user that doesn't have a logout_time is considered stale.
    # We set logout_time = last_activity so duration is accurate.
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