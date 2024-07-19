from django.urls import path, include
# import views
from . import views

# set a path to the index function in views.py
# add a name for the index view
# set a path to the chat_room function in views.py & name it
# - NOTE: include ChatApp to explicitly match URLs that start with /ChatApp/ followed by a dynamic room name, 
# - matching the pathname the JavaScript in index.html was set to redirect 
urlpatterns = [
    path("", views.index, name="index"),
    path("ChatApp/<str:room_name>/", views.chat_room, name="chat_room"),
    ]
