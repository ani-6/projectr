from django.contrib import admin
from .models import Profile, UserActivityLog

class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'ip_address', 'login_time', 'logout_time', 'duration')
    list_filter = ('login_time',)
    search_fields = ('user__username', 'ip_address')
    readonly_fields = ('login_time', 'logout_time', 'ip_address', 'session_key')

admin.site.register(Profile)
admin.site.register(UserActivityLog, UserActivityLogAdmin)