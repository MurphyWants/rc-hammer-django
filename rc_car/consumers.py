from channels.generic.websocket import AsyncWebsocketConsumer
import json

'''
<uuid>/video for video
<uuid>/control for control
<uuid>/data for data
'''

class Video_Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        return 0

    async def disconnect(self, close_code):
        return 0

    async def receive(self, text_data):
        return 0

    async def chat_message(self, event):
        return 0


class Drive_Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['unique_id']
        self.room_group_name = 'rc_car%s' % self.room_name

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
        text_data_json = json.loads(text_data)
        direction = text_data_json['Direction']
        scale = text_data_json['Scale']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'rc_drive_controls',
                'drive': drive,
                'scale': scale,
            }
        )

    async def chat_message(self, event):
        return 0


class Data_Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        return 0

    async def disconnect(self, close_code):
        return 0

    async def receive(self, text_data):
        return 0

    async def chat_message(self, event):
        return 0
