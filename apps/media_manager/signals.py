from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import MediaFile, MediaStat

# 3. Auto-create MediaStat when MediaFile is created
@receiver(post_save, sender=MediaFile)
def create_media_stat_signal(sender, instance, created, **kwargs):
    if created:
        MediaStat.objects.create(media_file=instance)