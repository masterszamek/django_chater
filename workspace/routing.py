# chat/routing.py
from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'workspace/(?P<workspace_slug>[-\w]+)/(?P<room_slug>[-\w]+)/$', consumers.ChatConsumer),
]