from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from .models import Thread, ChatMessage

# Imports for Redis Check
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import time

@login_required
def chat_view(request):
    """
    Main view for the chat interface.
    """
    return render(request, 'chat/index.html')

@login_required
def check_redis_status(request):
    """
    Checks if the Channel Layer (Redis) is accessible.
    """
    try:
        layer = get_channel_layer()
        # Perform a simple operation to verify connection
        async_to_sync(layer.group_add)("health_check", "health_check_channel")
        return JsonResponse({'status': 'active', 'message': 'Redis connection established.'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': f'Redis connection failed: {str(e)}'}, status=503)

@login_required
def get_recent_contacts(request):
    """
    API to fetch only users with whom the current user has an existing thread.
    Ordered by most recently updated thread.
    """
    threads = Thread.objects.by_user(request.user).order_by('-updated')
    
    data = []
    for thread in threads:
        # Determine the "other" user in the thread
        other_user = thread.receiver if thread.sender == request.user else thread.sender
        
        # Skip if user is deleted or inactive
        if not other_user or not other_user.is_active:
            continue

        # Get primary group/role
        group = other_user.groups.first()
        role = group.name if group else 'User'
        
        avatar = '/media/Account/profile_images/default.jpg'
        if hasattr(other_user, 'user_profile') and other_user.user_profile.profile_picture:
            avatar = other_user.user_profile.profile_picture.url
            
        # Get last message preview
        last_msg = ChatMessage.objects.filter(thread=thread).order_by('-timestamp').first()
        preview = last_msg.message[:30] + '...' if last_msg else 'No messages yet'
        timestamp = last_msg.timestamp.strftime('%H:%M') if last_msg else ''
        
        # Count unread messages sent BY the other user
        unread_count = ChatMessage.objects.filter(
            thread=thread, 
            user=other_user, 
            is_read=False
        ).count()

        data.append({
            'id': other_user.id,
            'username': other_user.username,
            'full_name': f"{other_user.first_name} {other_user.last_name}".strip() or other_user.username,
            'role': role,
            'avatar': avatar,
            'last_message': preview,
            'timestamp': timestamp,
            'unread_count': unread_count # Add to response
        })
    
    return JsonResponse({'users': data})

@login_required
def get_user_list(request):
    """
    API to search ALL users to start a NEW chat.
    """
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({'users': []})

    users = User.objects.filter(is_active=True).exclude(id=request.user.id)
    
    users = users.filter(
        Q(username__icontains=query) | 
        Q(first_name__icontains=query) | 
        Q(last_name__icontains=query)
    )
    
    # Limit results
    users = users[:20]

    data = []
    for user in users:
        group = user.groups.first()
        role = group.name if group else 'User'
        
        avatar = '/media/Account/profile_images/default.jpg'
        if hasattr(user, 'user_profile') and user.user_profile.profile_picture:
            avatar = user.user_profile.profile_picture.url

        data.append({
            'id': user.id,
            'username': user.username,
            'full_name': f"{user.first_name} {user.last_name}".strip() or user.username,
            'role': role,
            'avatar': avatar,
            'last_message': 'Start a new conversation',
            'timestamp': '',
            'unread_count': 0
        })
    
    return JsonResponse({'users': data})

@login_required
def get_chat_history(request, user_id):
    """
    Fetch history between current user and selected user_id
    """
    try:
        other_user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    thread, created = Thread.objects.get_or_new(request.user, other_user.username)
    
    if not thread:
         return JsonResponse({'messages': []})

    # 1. Mark unread CHAT messages from this user as read
    ChatMessage.objects.filter(
        thread=thread, 
        user=other_user, 
        is_read=False
    ).update(is_read=True)

    # 2. Also mark the associated SYSTEM Notification as read
    # This clears the bell icon alert automatically when you open the chat
    from apps.common.models import Notification
    notification_msg = f"New message from {other_user.first_name or other_user.username}"
    Notification.objects.filter(
        recipient=request.user,
        is_read=False,
        message=notification_msg
    ).update(is_read=True)

    messages = ChatMessage.objects.filter(thread=thread).order_by('timestamp')
    data = []
    
    for msg in messages:
        avatar = '/media/Account/profile_images/default.jpg'
        if hasattr(msg.user, 'user_profile') and msg.user.user_profile.profile_picture:
            avatar = msg.user.user_profile.profile_picture.url

        data.append({
            'message': msg.message,
            'username': msg.user.username,
            'is_me': msg.user == request.user,
            'avatar': avatar,
            'timestamp': msg.timestamp.strftime('%H:%M')
        })
    
    return JsonResponse({'messages': data, 'other_user': other_user.username})