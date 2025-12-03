import os
import mimetypes
from urllib.parse import unquote
from django.conf import settings
from django.core import signing
from django.http import Http404, HttpResponseForbidden, FileResponse, JsonResponse
from django.views import View
from django.views.generic import ListView # Added ListView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Notification

# --- Existing SecureMediaView ---
class SecureMediaView(LoginRequiredMixin, View):
    raise_exception = False
    def get(self, request, path):
        path = unquote(path)
        file_path_rel = None
        if getattr(settings, 'SECURE_MEDIA_ENCRYPTION', True):
            try:
                file_path_rel = signing.loads(path, salt='secure-media')
            except signing.BadSignature:
                raise Http404("Invalid media URL")
        else:
            file_path_rel = path
        file_path = os.path.join(settings.MEDIA_ROOT, file_path_rel)
        try:
            full_path = os.path.abspath(file_path)
            media_root = os.path.abspath(settings.MEDIA_ROOT)
            if not full_path.startswith(media_root):
                raise Http404("Invalid file path")
        except Exception:
            raise Http404("Invalid file path")
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            raise Http404("Media file does not exist")
        content_type, encoding = mimetypes.guess_type(full_path)
        content_type = content_type or 'application/octet-stream'
        return FileResponse(open(full_path, 'rb'), content_type=content_type)

# --- Notification & Session Views ---

class MarkNotificationReadView(LoginRequiredMixin, View):
    def post(self, request, pk):
        notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success', 'link': notification.link if notification.link else None})

class MarkAllReadView(LoginRequiredMixin, View):
    def post(self, request):
        request.user.notifications.filter(is_read=False).update(is_read=True)
        return JsonResponse({'status': 'success'})

class SessionStatusView(View):
    def get(self, request):
        if request.user.is_authenticated:
            return JsonResponse({'status': 'active'})
        else:
            return JsonResponse({'status': 'inactive'}, status=401)

# --- New Notification List View ---
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'common/notifications.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        # Return strictly the last 5 notifications (read or unread)
        return self.request.user.notifications.all().order_by('-created_at')[:5]