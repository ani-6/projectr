from django.contrib import admin
from .models import (
    ErrorCode, Folder, SubredditList, ModelName, 
    MediaFile, MediaStat, ModelRecord, VideoCategory, VideoLink
)

@admin.register(ErrorCode)
class ErrorCodeAdmin(admin.ModelAdmin):
    list_display = ('code', 'description', 'last_updated_at')
    search_fields = ('code', 'description')
    readonly_fields = ('created_at', 'last_updated_at')

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent', 'files_count', 'deleted')
    list_filter = ('deleted', 'parent')
    search_fields = ('name',)

@admin.register(SubredditList)
class SubredditListAdmin(admin.ModelAdmin):
    list_display = ('subreddit_name', 'is_active', 'last_updated_at')
    list_filter = ('is_active',)
    search_fields = ('subreddit_name',)
    actions = ['mark_active', 'mark_inactive']

    def mark_active(self, request, queryset):
        queryset.update(is_active=True)
    
    def mark_inactive(self, request, queryset):
        queryset.update(is_active=False)

@admin.register(ModelName)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'img_preview', 'is_active', 'files_count', 'drive_no')
    list_filter = ('is_active', 'drive_no')
    search_fields = ('name', 'title', 'search_text')
    readonly_fields = ('img_preview', 'created_at', 'last_updated_at')

class MediaStatInline(admin.StackedInline):
    model = MediaStat
    can_delete = False
    verbose_name_plural = 'Media Statistics'

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'media_type', 'downloaded', 'synced', 'starred', 'get_tags_display', 'created_at')
    list_filter = ('media_type', 'downloaded', 'synced', 'starred', 'subreddit', 'model', 'tags') # Taggit supports filtering by tags
    search_fields = ('file_name', 'original_url', 'description')
    
    # REMOVED: filter_horizontal = ('tags',) 
    # Taggit uses a simple text input widget (comma-separated), not a horizontal filter box.
    
    autocomplete_fields = ['model', 'subreddit', 'folder']
    
    inlines = [MediaStatInline]
    
    readonly_fields = ('img_preview', 'created_at', 'last_updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('file_name', 'media_type','img_preview', 'original_url', 'secondary_url', 'thumbnail_url')
        }),
        ('Status', {
            'fields': ('downloaded', 'synced', 'starred', 'error_code')
        }),
        ('Post Details', {
            'fields': ('post_title', 'post_id', 'post_url', 'description')
        }),
        ('Relationships', {
            'fields': ('model', 'subreddit', 'folder', 'tags') # 'tags' here renders as a text input
        }),
        ('Drive Info', {
            'fields': ('drive_file_id', 'drive_id', 'thumbnail_drive', 'filesize', 'filesize_bytes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_updated_at')
        }),
    )

    # Helper to display tags in the list view
    def get_tags_display(self, obj):
        return ", ".join(o.name for o in obj.tags.all())
    get_tags_display.short_description = 'Tags'

    # Optimization: Prefetch tags to prevent N+1 queries in list view
    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

@admin.register(ModelRecord)
class ModelRecordAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
    search_fields = ('story',)
    filter_horizontal = ('associated_models',) 

@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(VideoLink)
class VideoLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'original_url', 'comment')