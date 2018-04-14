from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/(?P<unique_id>[^/]+)/control/$', consumers.Drive_Consumer),
    url(r'^ws/<unique_id>/data/', consumers.Data_Consumer),
    url(r'^ws/(?P<unique_id>[^/]+)/in_use/$', consumers.In_Use_Consumer),
]
