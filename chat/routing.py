from django.urls import path,re_path

from . import consumers

websocket_urlpatterns = [
    path('ws/<str:roomName>/', consumers.ChatConsumer.as_asgi()),
]