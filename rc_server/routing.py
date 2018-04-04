from channels import route
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import rc_car.routing

'''
https://gearheart.io/blog/creating-a-chat-with-django-channels/
https://codyparker.com/django-channels-with-react/2/
'''

# mysite/routing.py
# http://channels.readthedocs.io/en/latest/tutorial/part_1.html

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket' : AuthMiddlewareStack(
        URLRouter{
            rc_car.routing.websocket_urlpatterns
        }
    )
})
