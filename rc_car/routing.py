from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/chat/$', consumers.Car_Consumer),
    url('test', consumers.Car_Consumer),
]