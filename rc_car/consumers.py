from channels.generic.websocket import WebsocketConsumer
import json

class Car_Consumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        message = text_data_json['message']
        print("Message: ", message)
