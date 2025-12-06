import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Thread, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        
        # 1. Check if user is authenticated
        if not self.user.is_authenticated:
            await self.close()
            return

        # The other user's ID is passed in the URL
        self.other_user_id = self.scope['url_route']['kwargs']['id']
        
        # Determine the unique thread group name
        user_ids = sorted([self.user.id, int(self.other_user_id)])
        self.room_group_name = f'chat_{user_ids[0]}_{user_ids[1]}'

        try:
            # 2. Try to connect to the Channel Layer (Redis)
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
        except Exception as e:
            # If Redis is down, this will catch the error and close the socket
            print(f"WebSocket Connection Error (Likely Redis): {e}")
            await self.close(code=1011) # Internal Error

    async def disconnect(self, close_code):
        # Only try to discard if we successfully determined the group name
        if hasattr(self, 'room_group_name'):
            await self.channel_layer.group_discard(
                self.room_group_name,
                self.channel_name
            )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        # Save message to database
        msg = await self.save_message(message, self.other_user_id)
        
        # Get formatted timestamp for the response
        timestamp = await self.get_formatted_timestamp(msg)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'avatar': await self.get_user_avatar_url(self.user),
                'timestamp': timestamp
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        avatar = event['avatar']
        timestamp = event.get('timestamp', '')

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'avatar': avatar,
            'timestamp': timestamp
        }))

    @database_sync_to_async
    def save_message(self, message, other_user_id):
        other_user = User.objects.get(id=other_user_id)
        # ThreadManager handles getting or creating
        thread, created = Thread.objects.get_or_new(self.user, other_user.username)
        # FORCE UPDATE: Explicitly save thread to update the 'updated' timestamp
        thread.save()
        msg = ChatMessage.objects.create(thread=thread, user=self.user, message=message)
        
        # --- Notification Logic ---
        from apps.common.utils import send_notification_to_user
        from apps.common.models import Notification
        
        # Define the standard notification message
        notification_msg = f"New message from {self.user.first_name or self.user.username}"
        
        # Anti-Spam: Check if there is already an UNREAD notification from this user
        has_unread_notification = Notification.objects.filter(
            recipient=other_user,
            is_read=False,
            message=notification_msg
        ).exists()
        
        if not has_unread_notification:
            send_notification_to_user(
                user=other_user,
                message=notification_msg,
                link='/chat/',
                type='info'
            )
            
        return msg

    @database_sync_to_async
    def get_formatted_timestamp(self, msg):
        local_time = timezone.localtime(msg.timestamp)
        return local_time.strftime('%I:%M %p').lstrip('0').lower()

    @database_sync_to_async
    def get_user_avatar_url(self, user):
        if hasattr(user, 'user_profile') and user.user_profile.profile_picture:
            return user.user_profile.profile_picture.url
        return '/media/Account/profile_images/default.jpg'