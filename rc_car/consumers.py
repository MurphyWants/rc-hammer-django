from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
import json
from datetime import datetime
from .models import RC_Car

'''
<uuid>/video for video
<uuid>/control for control
<uuid>/data for data
<uuid>/in_use
'''

class Video_Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        return 0

    async def disconnect(self, close_code):
        return 0

    async def receive(self, text_data):
        return 0

    async def message_handler(self, event):
        return 0


class Drive_Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['unique_id']
        self.room_group_name = 'rc_car%s' % self.room_name
        rc_car = RC_Car.objects.get(pk=self.room_name)
        current_user = rc_car.current_user
        user = self.scope["user"]

        if(current_user == None):
            rc_car.current_user = user
            rc_car.save()

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        rc_car = RC_Car.objects.get(pk=self.room_name)
        current_user = rc_car.current_user
        user = self.scope["user"]

        if(current_user == user):
            rc_car.current_user = None
            rc_car.save()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        drive_direction = text_data_json['drive']
        scale = text_data_json['scale']

        rc_car = RC_Car.objects.get(pk=self.room_name)
        current_user = rc_car.current_user
        user = self.scope["user"]

        if (current_user == None):
            rc_car.current_user = user
            current_user = rc_car.current_user

        if (user == current_user):

            rc_car.last_ping = datetime.now()
            rc_car.last_used = datetime.now()
            rc_car.save()

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

        await self.send_json(
        {
            "drive": drive_direction,
            "scale": scale,
        },
        )


class Data_Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        return 0

    async def disconnect(self, close_code):
        return 0

    async def receive(self, text_data):
        return 0

    async def message_handler(self, event):
        return 0

class In_Use_Consumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['unique_id']
        self.room_group_name = 'rc_car_is_in_use%s' % self.room_name

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
        rc_car = RC_Car.objects.get(pk=self.room_name)
        current_user = rc_car.current_user
        user = self.scope["user"]
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        if current_user == None:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_data',
                    'in_use' : False
                })
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_data',
                    'in_use' : True
                })


    async def user_data(self, event):
        in_use = event['in_use']

        await self.send_json(
        {
            "in_use": in_use
        },
        )
