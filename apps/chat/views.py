from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import JsonResponse
from .models import Thread, ChatMessage

@login_required
def chat_view(request):
    """
    Main view for the chat interface.
    """
    return render(request, 'chat/index.html')

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

        data.append({
            'id': other_user.id,
            'username': other_user.username,
            'full_name': f"{other_user.first_name} {other_user.last_name}".strip() or other_user.username,
            'role': role,
            'avatar': avatar,
            'last_message': preview,
            'timestamp': timestamp
        })
    
    return JsonResponse({'users': data})

@login_required
def get_user_list(request):
    """
    API to search ALL users to start a NEW chat.
    """
    query = request.GET.get('q', '').strip()
    
    # If no query, return empty list (since we only show recent contacts by default now)
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
            'last_message': 'Start a new conversation', # Placeholder for search results
            'timestamp': ''
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