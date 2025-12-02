from django.core.files.storage import FileSystemStorage
from django.core import signing
from django.conf import settings
import os

class SecureFileSystemStorage(FileSystemStorage):
    """
    Custom storage that obfuscates the file URL by signing the file path.
    This prevents exposing the directory structure (e.g., Account/profile_images/).
    """
    def url(self, name):
        # We sign the 'name' which is the relative path (e.g., 'Account/profile.jpg')
        # The salt must match the one used in the view.
        # We assume MEDIA_URL is /media/
        signed_path = signing.dumps(name, salt='secure-media')
        
        # We manually construct the URL because super().url() might encode characters
        # that we need to remain intact for the signature to be valid, or vice-versa.
        # However, standard Django usage is to append to MEDIA_URL.
        return settings.MEDIA_URL + signed_path