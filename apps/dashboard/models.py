from django.db import models
from django.contrib.auth.models import Group

# Create your models here.
class DashboardLink(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255, blank=True, null=True, help_text="Short description displayed on the dashboard card")
    url = models.CharField(max_length=200, help_text="Internal path (e.g., /dashboard/) or external URL (https://google.com)")
    icon = models.CharField(max_length=50, default="fa-solid fa-link", help_text="FontAwesome class (e.g., fa-solid fa-file)")
    groups = models.ManyToManyField(Group, related_name='dashboard_links', help_text="Select user roles that can see this link")
    order = models.PositiveIntegerField(default=0, help_text="Lower numbers appear first")
    open_in_new_tab = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']
        verbose_name = "Dashboard Link"
        verbose_name_plural = "Dashboard Links"

    def __str__(self):
        return self.title