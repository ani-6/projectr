import os
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

class Profile(models.Model):
    GENDER =(
        ('Male','Male'),
        ('Female','Female'),
        ('Other','Other')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name="user_profile")
    profile_picture = models.ImageField(default='Account/profile_images/default.jpg', upload_to='Account/profile_images',null=True,blank=True,verbose_name="Profile Picture")
    cover_picture = models.ImageField(default='Account/cover_images/_default.jpg', upload_to='Account/cover_images',null=True,blank=True,verbose_name="Cover Picture")
    gender = models.CharField(max_length=50, null=True,choices=GENDER)
    headline = models.CharField(max_length=80,null=True, blank=True)
    bio = models.TextField(null=True, blank=True,verbose_name='About me')

    def __str__(self):
        return self.user.username

    @property
    def thumbnail_url(self):
        if self.profile_picture and os.path.basename(self.profile_picture.name) != 'default.jpg':
            thumbnail_path = settings.LOGIN_REDIRECT_URL + 'secure_media/Account/profile_images/thumbnail_' + os.path.basename(self.profile_picture.name)
            return thumbnail_path
        else:
            return settings.LOGIN_REDIRECT_URL + 'secure_media/' + self.profile_picture.name

# --- Updated UserActivityLog ---
class UserActivityLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activity_logs')
    session_key = models.CharField(max_length=40, null=True, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    login_time = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)  # New field to track last move
    logout_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.login_time}"

    @property
    def duration(self):
        # If logged out, calculate full duration
        if self.logout_time:
            return self.logout_time - self.login_time
        
        # If still active (or crashed), calculate up to last activity
        if self.last_activity:
            return self.last_activity - self.login_time
            
        return None