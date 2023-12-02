# from django.urls import path,re_path
# from home.consumers import chatConsumer
# websocket_urlpatterns = [
#     path('hat', chatConsumer.as_asgi())

# ]
from django.urls import re_path,path

from . import consumers

websocket_urlpatterns = [
    re_path(r"ws/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
   
]