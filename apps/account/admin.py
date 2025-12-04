from django.contrib import admin
from .models import Profile, UserActivityLog

@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'login_time', 'logout_time', 'duration')
    list_filter = ('login_time',)
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('login_time', 'logout_time', 'ip_address', 'session_key')

@admin.register(Profile)
class profile_admin(admin.ModelAdmin):
    fieldsets = (
        ('Select User', {
        'fields': ['user']
        }),
        ('Pictures', {
        'classes': ('wide',),
        'fields': ('profile_picture', 'cover_picture'),
        }),
        ('Other Details', {
        'classes': ('wide',),
        'fields': ('gender','headline','bio'),
        }),
        )
    list_display = ['user','gender']
