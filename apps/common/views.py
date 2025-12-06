import os
import mimetypes
import platform
import time
from urllib.parse import unquote
from django.conf import settings
from django.core import signing
from django.http import Http404, HttpResponseForbidden, FileResponse, JsonResponse
from django.views import View
from django.views.generic import ListView, TemplateView
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import connection
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notification

# --- Existing SecureMediaView (Updated) ---
class SecureMediaView(LoginRequiredMixin, View):
    raise_exception = False
    
    def get(self, request, path):
        path = unquote(path)
        file_path_rel = None

        # 1. Whitelist Default Images: Allow them without signature
        if 'default.jpg' in path or '_default.jpg' in path or 'default.svg' in path:
            file_path_rel = path
            
        # 2. For all other files, enforce encryption if enabled
        elif getattr(settings, 'SECURE_MEDIA_ENCRYPTION', True):
            try:
                file_path_rel = signing.loads(path, salt='secure-media')
            except signing.BadSignature:
                raise Http404("Invalid media URL")
        else:
            file_path_rel = path

        # 3. Serve the file
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

# --- System Health View (New) ---
class SystemHealthView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'common/system_health.html'

    def test_func(self):
        # Only allow users in the 'Managers' group
        return self.request.user.groups.filter(name='Managers').exists()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
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
        except Exception:
            pass

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
        except Exception:
            pass

        # 3. Server Info
        server_info = {
            'status': 'Online',
            'system': platform.system(),
            'node': platform.node(),
            'release': platform.release(),
            'python': platform.python_version(),
            'machine': platform.machine()
        }

        context.update({
            'db_status': db_status,
            'db_latency': db_latency,
            'redis_status': redis_status,
            'redis_latency': redis_latency,
            'server_info': server_info,
            'api_status': 'Online' # If we rendered this view, Django is serving requests
        })
        return context