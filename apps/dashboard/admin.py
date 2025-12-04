from django.contrib import admin
from .models import DashboardLink

@admin.register(DashboardLink)
class DashboardLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'description', 'url', 'order', 'is_active')
    list_filter = ('is_active', 'groups')
    search_fields = ('title', 'description', 'url')
    list_editable = ('order', 'is_active')
    filter_horizontal = ('groups',)