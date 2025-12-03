from django.utils import timezone
from apps.account.models import UserActivityLog

class UserActivityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Only track authenticated users
        if request.user.is_authenticated and request.session.session_key:
            try:
                # Update the log entry for the current session
                # We filter by session_key to ensure we update the correct device/browser log
                UserActivityLog.objects.filter(
                    user=request.user,
                    session_key=request.session.session_key,
                    logout_time__isnull=True
                ).update(last_activity=timezone.now())
            except Exception:
                pass

        return response