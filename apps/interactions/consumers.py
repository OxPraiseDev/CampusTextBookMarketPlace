import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Message, ChatRoom

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope["user"]
        
        new_msg = await self.save_message(user, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message', 
                'message': message, 
                'username': user.username, 
                'msg_id': str(new_msg.id),
                'file_url': '',
                'message_type': 'text'
            }
        )

        recipient_id, book_title = await self.get_room_details(user)

        await self.channel_layer.group_send(
            f"user_{recipient_id}",
            {
                'type': 'send_notification',
                'sender': user.username,
                'room_id': str(self.room_id),
                'content': message,
                'book_title': book_title
            }
        )

    @database_sync_to_async
    def save_message(self, user, content):
        room = ChatRoom.objects.get(id=self.room_id)
        return Message.objects.create(room=room, sender=user, content=content)

    @database_sync_to_async
    def get_room_details(self, user):
        room = ChatRoom.objects.select_related('buyer', 'seller', 'listing__book').get(id=self.room_id)
        recipient = room.seller if user == room.buyer else room.buyer
        return recipient.id, room.listing.book.title

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event.get('message', ''),
            'username': event['username'],
            'msg_id': event['msg_id'],
            'file_url': event.get('file_url', ''),
            'message_type': event.get('message_type', 'text')
        }))

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
        else:
            self.group_name = f"user_{self.user.id}"
            await self.channel_layer.group_add(self.group_name, self.channel_name)
            await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, 'group_name'):
            await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            'sender': event['sender'],
            'room_id': event['room_id'],
            'content': event['content'],
            'book_title': event['book_title']
        }))