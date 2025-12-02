import os
import mimetypes
from urllib.parse import unquote  # Import unquote
from django.conf import settings
from django.core import signing
from django.http import Http404, HttpResponseForbidden, FileResponse
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

class SecureMediaView(LoginRequiredMixin, View):
    """
    View to serve media files only to authenticated users.
    Decodes signed URLs to hide the directory structure.
    """
    raise_exception = False

    def get(self, request, path):
        # 1. URL Decode the path
        # Browsers might encode ':' as '%3A', which breaks the signature check.
        # unquote() fixes this.
        path = unquote(path)

        # 2. Decode the signed path
        try:
            # This reverses the signing done in SecureFileSystemStorage.url()
            file_path_rel = signing.loads(path, salt='secure-media')
        except signing.BadSignature:
            # Debugging: Print to console if signature fails
            print(f"SecureMediaView: BadSignature for path: {path}")
            raise Http404("Invalid media URL")

        # 3. Construct the full path
        file_path = os.path.join(settings.MEDIA_ROOT, file_path_rel)
        
        # 4. Security: Prevent directory traversal
        try:
            full_path = os.path.abspath(file_path)
            media_root = os.path.abspath(settings.MEDIA_ROOT)
            if not full_path.startswith(media_root):
                print(f"SecureMediaView: Path traversal attempt: {full_path}")
                raise Http404("Invalid file path")
        except Exception:
            raise Http404("Invalid file path")

        # 5. Check if file exists
        if not os.path.exists(full_path) or not os.path.isfile(full_path):
            print(f"SecureMediaView: File not found: {full_path}")
            raise Http404("Media file does not exist")

        # 6. Serve the file
        content_type, encoding = mimetypes.guess_type(full_path)
        content_type = content_type or 'application/octet-stream'

        return FileResponse(open(full_path, 'rb'), content_type=content_type)