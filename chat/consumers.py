import json
from .models import Room,Message
from django.contrib.auth import get_user_model
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        self.name = self.scope['url_route']['kwargs']['roomName']
        email1 = self.name.split('-')[0]
        email2 = self.name.split('-')[1]
        room_name = f'{min(email1,email2)}-{max(email1,email2)}'.replace('@','')
        self.room_name = room_name
        self.room_group_name = 'chat_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self,code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        print(data)
        message = data['message']
        email = data['email']
        print('rec12',email)
        room = data['room']

        await self.save_message(self.name,email, room, message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'email': email
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        email = event['email']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'email': email
        }))

    @sync_to_async
    def save_message(self,name, email, room, message):
        # print('12email',email)
        user = User.objects.get(email=email)
        room = Room.objects.get(name=name)
        print('mes1',message)
        if message:
            Message.objects.create(user=user, room=room, content=message)

