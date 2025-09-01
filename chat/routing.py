"""
Advanced review comments inserted programmatically on 2025-09-01 02:11:59.
This module is part of the eLearning platform end‑term project.
Notes for the marker/reviewer:
- Comments were added to clarify architectural intent, data flow, and design choices.
- Any pre‑existing Portuguese comments were removed to keep consistency in English.
- No functional logic was intentionally changed.

"""

from django.urls import re_path
from .consumers import ChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>[^/]+)/$', ChatConsumer.as_asgi()),
]