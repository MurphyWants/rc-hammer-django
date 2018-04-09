'''
https://gearheart.io/blog/creating-a-chat-with-django-channels/
https://codyparker.com/django-channels-with-react/2/
http://channels.readthedocs.io/en/latest/tutorial/part_2.html
'''

# mysite/routing.py
# http://channels.readthedocs.io/en/latest/tutorial/part_1.html

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            rc_car.routing.websocket_urlpatterns
        )
    ),
})
