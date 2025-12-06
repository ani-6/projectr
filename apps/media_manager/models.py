from django.db import models
from taggit.managers import TaggableManager

# 1. REMOVED Custom Tag Model (Replaced by django-taggit)

class ErrorCode(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='Error Code')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated At')

    class Meta:
        db_table = 'error_codes'
        verbose_name = 'Error Code'
        verbose_name_plural = 'Error Codes'

    def __str__(self):
        return f"{self.code}"


class Folder(models.Model):
    name = models.CharField(max_length=255, verbose_name='Folder Name')
    parent = models.IntegerField(null=True, blank=True,default=None, verbose_name='Parent Folder')
    files_count = models.IntegerField(default=0, verbose_name='Files Count')
    deleted = models.BooleanField(default=False, verbose_name='Is Deleted')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated At')

    class Meta:
        db_table = 'folders'
        verbose_name = 'Folder'
        verbose_name_plural = 'Folders'

    def __str__(self):
        return self.name


class SubredditList(models.Model):
    subreddit_name = models.CharField(max_length=255, verbose_name='Subreddit Name')
    is_active = models.BooleanField(default=False, verbose_name='Is Active')
    subreddit_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='Subreddit URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated At')
    class Meta:
        db_table = 'subreddits_list'
        verbose_name = 'Subreddit'
        verbose_name_plural = 'Subreddits List'

    def __str__(self):
        return self.subreddit_name


class ModelName(models.Model):
    name = models.CharField(max_length=255, verbose_name='Model Name')
    suffix = models.CharField(max_length=255, null=True, blank=True, verbose_name='Suffix')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Title')
    picture = models.CharField(max_length=512, null=True, blank=True, verbose_name='Picture')
    search_text = models.CharField(max_length=255, null=True, blank=True, verbose_name='Search Text')
    
    # Relationships
    folder = models.IntegerField(null=True, blank=True, verbose_name='Folder')
    uploads_folder = models.IntegerField(null=True, blank=True, verbose_name='Uploads Folder')
    
    files_count = models.IntegerField(null=True, blank=True, verbose_name='Files Count')
    drive_no = models.IntegerField(default=0, verbose_name='Drive Number')
    drive_folder_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='Drive Folder ID')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated At')

    class Meta:
        db_table = 'model_names'
        verbose_name = 'Model Name'
        verbose_name_plural = 'Model Names'

    def __str__(self):
        return self.name


class MediaFile(models.Model):
    file_name = models.CharField(max_length=255, null=True, blank=True, verbose_name='File Name')
    original_url = models.CharField(max_length=1200, unique=True, verbose_name='Original URL')
    secondary_url = models.CharField(max_length=2500, null=True, blank=True, verbose_name='Secondary URL')
    thumbnail_url = models.CharField(max_length=500, null=True, blank=True, verbose_name='Thumbnail URL')
    thumbnail_drive = models.CharField(max_length=500, null=True, blank=True, verbose_name='Thumbnail Drive')
    media_type = models.CharField(max_length=255, null=True, blank=True, verbose_name='Media Type')
    post_url = models.CharField(max_length=255, null=True, blank=True, verbose_name='Post URL')
    
    filesize_bytes = models.BigIntegerField(null=True, blank=True, verbose_name='Filesize Bytes')
    filesize = models.CharField(max_length=50, null=True, blank=True, verbose_name='Filesize')
    
    post_title = models.CharField(max_length=255, null=True, blank=True, verbose_name='Post Title')
    post_id = models.CharField(max_length=20, null=True, blank=True, verbose_name='Post ID')
    description = models.TextField(null=True, blank=True, verbose_name='Description')
    
    downloaded = models.BooleanField(default=False, verbose_name='Downloaded')
    synced = models.BooleanField(default=False, verbose_name='Synced')
    error_code = models.IntegerField(default=0, verbose_name='Error Code')
    starred = models.BooleanField(default=False, verbose_name='Starred')
    
    drive_file_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='Drive File ID')
    drive_id = models.CharField(max_length=255, null=True, blank=True, verbose_name='Drive ID')
    
    # Relationships
    model = models.ForeignKey(ModelName, on_delete=models.SET_NULL, null=True, blank=True, related_name='media_files')
    subreddit = models.ForeignKey(SubredditList, on_delete=models.SET_NULL, null=True, blank=True, related_name='media_files')
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='media_files')
    
    # 2. Replaced Custom ManyToManyField with TaggableManager
    tags = TaggableManager(blank=True, verbose_name='Tags')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated At')

    class Meta:
        db_table = 'media_files'
        verbose_name = 'Media File'
        verbose_name_plural = 'Media Files'

    def __str__(self):
        return self.file_name or f"File {self.id}"


class MediaStat(models.Model):
    # OneToOne relationship with MediaFile, sharing the same Primary Key
    media_file = models.OneToOneField(MediaFile, on_delete=models.CASCADE, primary_key=True, related_name='stats', verbose_name='Media File')
    total_views = models.IntegerField(default=0, verbose_name='Total Views')
    duration = models.IntegerField(default=0, verbose_name='Duration')
    last_visited = models.DateTimeField(null=True, blank=True, verbose_name='Last Visited')

    class Meta:
        db_table = 'media_stats'
        verbose_name = 'Media Stat'
        verbose_name_plural = 'Media Stats'

    def __str__(self):
        return f"Stats for {self.media_file}"


class ModelRecord(models.Model):
    associated_models = models.ManyToManyField(
        'ModelName', 
        blank=True, 
        related_name='records', 
        verbose_name='Models'
    )
    
    story = models.TextField(null=True, blank=True, verbose_name='Story')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')

    class Meta:
        db_table = 'model_records'
        verbose_name = 'Model Record'
        verbose_name_plural = 'Model Records'

    def __str__(self):
        names = ", ".join([str(m) for m in self.associated_models.all()])
        return f"Record for {names}"


class VideoCategory(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Category Name')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Video Category'
        verbose_name_plural = 'Video Categories'

    def __str__(self):
        return self.name

class VideoLink(models.Model):
    title = models.CharField(max_length=500, null=True, blank=True, verbose_name='Video Title')
    original_url = models.CharField(max_length=2000, unique=True, verbose_name='Original URL')
    thumbnail_url = models.CharField(max_length=1200, null=True, blank=True, verbose_name='Thumbnail URL')
    category = models.ForeignKey(
        VideoCategory, 
        on_delete=models.SET_NULL,
        null=True, 
        blank=True, 
        verbose_name='Category'
    )
    comment = models.TextField(null=True, blank=True, verbose_name='Comment')
    is_active = models.BooleanField(default=True, verbose_name='Is Active')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created At')
    last_updated_at = models.DateTimeField(auto_now=True, verbose_name='Last Updated At')

    class Meta:
        db_table = 'video_links'
        verbose_name = 'Video Link'
        verbose_name_plural = 'Video Links'

    def __str__(self):
        return self.title or self.original_url
