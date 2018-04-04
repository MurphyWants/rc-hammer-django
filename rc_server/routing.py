'''from channels import route

# This function will display all messages received in the console
def message_handler(message):
    print(message['text'])


channel_routing = [
    route("websocket.receive", message_handler)  # we register our message handler
]'''

'''
https://gearheart.io/blog/creating-a-chat-with-django-channels/
https://codyparker.com/django-channels-with-react/2/
'''


# mysite/routing.py
# http://channels.readthedocs.io/en/latest/tutorial/part_1.html
from channels.routing import ProtocolTypeRouter

application = ProtocolTypeRouter({
    # (http->django views is added by default)
})
