from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
import json
from datetime import datetime, timedelta, timezone
from .models import RC_Car

'''
<uuid>/video for video
<uuid>/control for control
<uuid>/data for data
<uuid>/in_use
'''

"""

Consumer classes for the rc_cars:

Drive_Consumer: <uuid>/control
    - Allow one user at a time to send data to control the car

In_Use_Consumer: <uuid>/in_use
    - Allow users to ping the channel
    - Returns False if nobody is using it
    - If someone is using it, Returns true, current_user id, ping user id
    - TODO Just generally redo this

Data_Consumer: <uuid>/data
    - Only allow the rc_car to post to it
    - Other users can receive data from it
    - TODO

TODO Datas Types:
    - Ratelimit : Defined in the car is the limit of how long it will process each message. Sync this between client and server. Let it be changed.

"""

class Drive_Consumer(AsyncJsonWebsocketConsumer):
    """ Purpose: To handle connections for /ws/<uuid>/control/, to handle data for controlling the car """
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['unique_id']
        self.room_group_name = 'rc_car%s' % self.room_name
        rc_car = RC_Car.objects.get(pk=self.room_name)
        current_user = rc_car.current_user
        user = self.scope["user"]

        if(current_user == None):
            rc_car.current_user = user
            """ Effect: save the current user as the current_user. Sideeffect: If someone is not logged in, it auto closes them. Brilliant. """
            rc_car.save()
        else:
            await self.close()
            """ Ensure that only one connection is open at a time so that random data isn't being thrown around """


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

        """ Free up the car for the next person to use """

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)

        """ Basic data type: rc_drive_controls with fields drive_direction (some number inticating degrees around a circle) """

        drive_direction = text_data_json['drive']
        scale = text_data_json['scale']

        rc_car = RC_Car.objects.get(pk=self.room_name)
        current_user = rc_car.current_user
        user = self.scope["user"]


        if (current_user == None):
            rc_car.current_user = user
            current_user = rc_car.current_user
            """ Somehow if you're allowed to send messages and a current_user hasn't been set, we should fix that """

        if (user == current_user):
            """ Also somehow if you're allowed to send messages and you're not a current_user, we don't want you """
            if (datetime.now(timezone.utc) > (rc_car.last_consumer_ping - timedelta(milliseconds=10))):
                """ Ratelimiting messages so if we get more messages than this, discard them. TODO Write more on Ratelimiting """
                rc_car.last_consumer_ping = datetime.now()
                rc_car.save()

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'rc_drive_controls',
                        'drive': drive_direction,
                        'scale': scale,
                    }
                )
            else:
                await self.close()

    async def rc_drive_controls(self, event):
        drive_direction = event['drive']
        scale = event['scale']

        await self.send_json(
        {
            "type" : control,
            "drive": drive_direction,
            "scale": scale,
        },
        )


class Data_Consumer(AsyncJsonWebsocketConsumer):
    """ Purpose: handles data on /ws/<uuid>/data/, handles connection from the car """
    """ TODO: recieve more data """
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['unique_id']
        self.room_group_name = 'rc_car_login%s' % self.room_name

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
        type = text_data_json['type']
        rc_car = RC_Car.objects.get(pk=self.room_name)

        if(type == "Login"):
            """ Letting cars login over socket """
            """ Note: if this isn't done over ssl/wss it will be plain text """

            if(rc_car.Check_Password(text_data_json['password'])):

                rc_car.last_used = datetime.now()
                rc_car.save()

                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'login_success',
                    }
                )
                """ If the password is correct, add it to the channel that the Drive_Consumer is on """
                await self.channel_layer.group_add(
                    'rc_car%s' % self.room_name,
                    self.channel_name
                )

            else:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'invalid_password',
                    }
                )
                await self.close()
        else:
            """ TODO: This is really just a placeholder """
            rc_car.last_used = datetime.now()
            rc_car.save()

    """ Event/Message handlers """

    async def invalid_password(self, event):
        await self.send_json({
            "type": "Invalid-Password",
            "message": "Invalid Password",
        })

    async def give_password(self, event):
        await self.send_json({
            "type": "Login",
            "message": "Respond with password",
        })

    async def login_success(self, event):
        await self.send_json({
            "type": "Login-Success",
            "message": "Moving to room",
        })

    async def rc_drive_controls(self, event):
        drive_direction = event['drive']
        scale = event['scale']

        await self.send_json(
        {
            "drive": drive_direction,
            "scale": scale,
        },
        )

class In_Use_Consumer(AsyncJsonWebsocketConsumer):
    """ Purpose: handles data on /ws/<uuid>/in_use/, is a nearly open channel for anyone to connect and see if the car is in use """
    """ TODO: Just redo this in general """
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
                    'current_user': "None",
                    'user': "None",
                    'in_use' : False
                })
        else:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'user_data',
                    'current_user': current_user.id,
                    'user': user.id,
                    'in_use' : True
                })


    async def user_data(self, event):
        in_use = event['in_use']
        current_user = event['current_user']
        user = event['user']

        await self.send_json(
        {
            "current_user": current_user,
            "you": user,
            "in_use": in_use
        },
        )
