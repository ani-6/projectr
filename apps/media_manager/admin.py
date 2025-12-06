from django.contrib import admin
from .models import (
    Tag, ErrorCode, Folder, SubredditList, ModelName, 
    MediaFile, MediaStat, ModelRecord, VideoCategory, VideoLink
)

# 1. Tag Admin
@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'tag_type', 'slug', 'created_at')
    list_filter = ('tag_type',)
    search_fields = ('name', 'slug')
    # Helps auto-fill the slug field in the UI as you type the name/type
    prepopulated_fields = {'slug': ('tag_type', 'name')} 


# 2. Reference Models (Simple Lists)
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
    autocomplete_fields = ['parent'] # Helpful if you have many folders

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
    list_display = ('name', 'is_active', 'files_count', 'drive_no')
    list_filter = ('is_active', 'drive_no')
    search_fields = ('name', 'title', 'search_text')
    readonly_fields = ('created_at', 'last_updated_at')


# 3. Media Files & Stats (Complex Relationship)

# Inline allows editing Stats inside the MediaFile page
class MediaStatInline(admin.StackedInline):
    model = MediaStat
    can_delete = False
    verbose_name_plural = 'Media Statistics'

@admin.register(MediaFile)
class MediaFileAdmin(admin.ModelAdmin):
    list_display = ('file_name', 'media_type', 'downloaded', 'synced', 'starred', 'created_at')
    list_filter = ('media_type', 'downloaded', 'synced', 'starred', 'subreddit', 'model')
    search_fields = ('file_name', 'original_url', 'description')
    
    # This creates the nice double-box UI for selecting tags
    filter_horizontal = ('tags',) 
    
    # This allows searching for related keys instead of a dropdown list (good for performance)
    autocomplete_fields = ['model', 'subreddit', 'folder']
    
    inlines = [MediaStatInline]
    
    readonly_fields = ('created_at', 'last_updated_at')
    fieldsets = (
        ('Basic Info', {
            'fields': ('file_name', 'media_type', 'original_url', 'secondary_url', 'thumbnail_url')
        }),
        ('Status', {
            'fields': ('downloaded', 'synced', 'starred', 'error_code')
        }),
        ('Post Details', {
            'fields': ('post_title', 'post_id', 'post_url', 'description')
        }),
        ('Relationships', {
            'fields': ('model', 'subreddit', 'folder', 'tags')
        }),
        ('Drive Info', {
            'fields': ('drive_file_id', 'drive_id', 'thumbnail_drive', 'filesize', 'filesize_bytes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_updated_at')
        }),
    )


# 4. Model Records
@admin.register(ModelRecord)
class ModelRecordAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
    search_fields = ('story',)
    # Use filter_horizontal for the ManyToMany field 'associated_models'
    filter_horizontal = ('associated_models',) 


# 5. Video Links
@admin.register(VideoCategory)
class VideoCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')
    search_fields = ('name',)

@admin.register(VideoLink)
class VideoLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_active', 'created_at')
    list_filter = ('is_active', 'category')
    search_fields = ('title', 'original_url', 'comment')