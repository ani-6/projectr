import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Thread, ChatMessage

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope['user']
        # The other user's ID is passed in the URL
        self.other_user_id = self.scope['url_route']['kwargs']['id']
        
        # Determine the unique thread group name
        # We sort IDs to ensure consistent group naming regardless of who initiates
        user_ids = sorted([self.user.id, int(self.other_user_id)])
        self.room_group_name = f'chat_{user_ids[0]}_{user_ids[1]}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        
        # Save message to database
        await self.save_message(message, self.other_user_id)

        # Broadcast message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': self.user.username,
                'avatar': await self.get_user_avatar_url(self.user)
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        avatar = event['avatar']

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'avatar': avatar
        }))

    @database_sync_to_async
    def save_message(self, message, other_user_id):
        other_user = User.objects.get(id=other_user_id)
        # ThreadManager handles getting or creating
        thread, created = Thread.objects.get_or_new(self.user, other_user.username)
        return ChatMessage.objects.create(thread=thread, user=self.user, message=message)

    @database_sync_to_async
    def get_user_avatar_url(self, user):
        if hasattr(user, 'user_profile') and user.user_profile.profile_picture:
            return user.user_profile.profile_picture.url
        return '/media/Account/profile_images/default.jpg'