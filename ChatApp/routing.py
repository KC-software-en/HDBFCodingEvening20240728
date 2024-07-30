# https://channels.readthedocs.io/en/latest/tutorial/part_2.html#write-your-first-consumer
from django.urls import re_path

from . import consumers

# call the as_asgi() classmethod to get an ASGI app that instantiates an instance of the consumer for each user-connection
# - similar to Django’s as_view(), which plays the same role for per-request Django view instances
# Note: use re_path() due to limitations in URLRouter https://channels.readthedocs.io/en/latest/topics/routing.html#urlrouter
# verify that the consumer for the /ws/chat/ROOM_NAME/ path works by running migrations to apply database changes
# - (Django’s session framework needs the database). then start the Channels development server
websocket_urlpatterns = [
    re_path(r"ws/ChatApp/(?P<room_name>\w+)/$", consumers.ChatConsumer.as_asgi()),
    re_path(r"ws/presence/(?P<room_name>\w+)/$", consumers.PresenceConsumer.as_asgi()),
    ]