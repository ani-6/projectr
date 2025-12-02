import os
from PIL import Image
from django.conf import settings

def generate_thumbnail(profile):
    """
    Creates a thumbnail for the profile picture and returns its URL.
    Stores it in a 'thumbs' directory inside the profile image's directory.
    """
    if not profile.profile_picture:
        return None

    original_path = profile.profile_picture.path
    
    # Check if file exists
    if not os.path.exists(original_path):
        return profile.profile_picture.url

    # Avoid processing default images if they are just static assets
    # Assuming default images might contain 'default.jpg'
    if 'default.jpg' in os.path.basename(original_path):
        return profile.profile_picture.url

    try:
        # Define paths
        dir_name = os.path.dirname(original_path)
        thumbs_dir = os.path.join(dir_name, 'thumbs')

        # Create thumbs directory if not exists
        if not os.path.exists(thumbs_dir):
            os.makedirs(thumbs_dir)

        filename = os.path.basename(original_path)
        thumb_filename = f"thumb_{filename}"
        thumb_path = os.path.join(thumbs_dir, thumb_filename)

        # Generate thumbnail
        img = Image.open(original_path)
        
        # Convert to RGB to ensure compatibility (e.g., if source is RGBA or Palette)
        if img.mode in ('RGBA', 'P'):
            img = img.convert('RGB')
            
        # Resize/Thumbnail (100x100 is sufficient for navbar)
        img.thumbnail((150, 150)) 
        img.save(thumb_path)

        # Return URL relative to MEDIA_URL
        relative_path = os.path.relpath(thumb_path, settings.MEDIA_ROOT)
        # Ensure forward slashes for URLs even on Windows
        relative_path = relative_path.replace('\\', '/')
        return settings.MEDIA_URL + relative_path

    except Exception as e:
        print(f"Error generating thumbnail: {e}")
        # Fallback to original
        return profile.profile_picture.url

def get_thumbnail_url(profile):
    """
    Retrieves the thumbnail URL if it exists, otherwise returns original URL.
    Used for populating the session on login.
    """
    if not profile.profile_picture:
        return ''

    # If it's the default image, just return it
    if 'default.jpg' in os.path.basename(profile.profile_picture.name):
        return profile.profile_picture.url

    try:
        original_path = profile.profile_picture.path
        dir_name = os.path.dirname(original_path)
        thumbs_dir = os.path.join(dir_name, 'thumbs')
        filename = os.path.basename(original_path)
        thumb_filename = f"thumb_{filename}"
        thumb_path = os.path.join(thumbs_dir, thumb_filename)

        if os.path.exists(thumb_path):
            relative_path = os.path.relpath(thumb_path, settings.MEDIA_ROOT)
            relative_path = relative_path.replace('\\', '/')
            return settings.MEDIA_URL + relative_path
    except:
        pass

    # Fallback to original if thumb doesn't exist
    return profile.profile_picture.url