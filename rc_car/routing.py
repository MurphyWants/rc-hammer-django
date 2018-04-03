from chanels.routing import route
from rc_car.consumers import ws_connect, ws_disconenct, ws_recieve

'''channel_routing = [
    route('websocket.connect', ws_connect),
    route('websocket.recieve', ws_recieve),
    route('websocket.disconnect', ws_disconnect),
]'''

ASGI_APPLICATION = "rc_car.routing.application"

def message_handler(message):
    print(message['text'])

channel_routing = [
    route('websocket.recieve', message_handler)
]
