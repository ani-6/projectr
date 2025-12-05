from django.contrib import admin
from .models import Thread, ChatMessage

class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    extra = 1

@admin.register(Thread)
class ThreadAdmin(admin.ModelAdmin):
    inlines = [ChatMessageInline]
    list_display = ['sender', 'receiver', 'updated', 'timestamp']
    search_fields = ['sender__username', 'receiver__username']