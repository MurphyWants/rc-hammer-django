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
        drive_direction = text_data_json['drive']
        scale = text_data_json['scale']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'rc_drive_controls',
                'drive': drive_direction,
                'scale': scale,
            }
        )

    async def rc_drive_controls(self, event):
        drive_direction = event['drive']
        scale = event['scale']

        await self.send(text_data=json.dump({
            'drive': drive_direction,
            'scale': scale
        }))


class Data_Consumer(AsyncWebsocketConsumer):
    async def connect(self):
        return 0

    async def disconnect(self, close_code):
        return 0

    async def receive(self, text_data):
        return 0

    async def chat_message(self, event):
        return 0
