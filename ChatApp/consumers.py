# import json to encode and decode JSON data
# - messages received from the WebSocket and sent to the WebSocket are formatted as JSON strings
import json

# https://channels.readthedocs.io/en/latest/tutorial/part_2.html#write-your-first-consumer
# write a basic consumer that accepts WebSocket connections on the path /ws/ChatApp/ROOM_NAME/,
# - takes messages received on the WebSocket and echos it back to the same WebSocket.
# comment out imports because the ChatConsumer will now be rewritten below asynchronously
## from channels.generic.websocket import WebsocketConsumer

# after configuring a channel layer, import async_to_sync
# comment out import async_to_sync - it's no longer needed when calling methods on the channel layer
# - because the ChatConsumer will now be rewritten below as asynchronous
## from asgiref.sync import async_to_sync

# https://channels.readthedocs.io/en/latest/tutorial/part_3.html#tutorial-part-3-rewrite-chat-server-as-asynchronous
# rewrite ChatConsumer to be asynchronous
# import AsyncWebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer

# https://channels.readthedocs.io/en/stable/topics/channel_layers.html#using-outside-of-consumers
# import get_channel_layer because...
from channels.layers import get_channel_layer

# when Channels accepts a WebSocket connection, it consults the root routing configuration to lookup a consumer,
# - and then calls various functions on the consumer to handle events from the connection.
# https://channels.readthedocs.io/en/latest/tutorial/part_2.html#enable-a-channel-layer
# - When a user posts a message, a JavaScript function will transmit the message over WebSocket to a ChatConsumer. 
# - The ChatConsumer will receive that message and forward it to the group corresponding to the room name. 
# - Every ChatConsumer in the same group (and thus in the same room) receives the message from the group and
# - forwards it over WebSocket back to JavaScript, where it's appended to the chat log.
# https://channels.readthedocs.io/en/latest/tutorial/part_3.html#rewrite-the-consumer-to-be-asynchronous
# the ChatConsumer class inherits from AsyncWebsocketConsumer now instead of WebsocketConsumer
# change all methods from just def to async def 
# change async_to_sync to await when joining, leaving & sending messages in a room
# - because it's used to call asynchronous functions that perform network I/O (Involves sending/receiving data over a network)
class ChatConsumer(AsyncWebsocketConsumer):
    """Create a ChatConsumer class.

    :param AsyncWebsocketConsumer: The ChatConsumer class inherits from AsyncWebsocketConsumer 
    :type AsyncWebsocketConsumer: Class
    """
    # connect to WebSocket    
    async def connect(self):
        """An asynchronous method to connect to WebSocket. 
        """
        # https://channels.readthedocs.io/en/latest/tutorial/part_2.html#enable-a-channel-layer
        # Obtain the 'room_name' parameter from the URL route in chat/routing.py that opened the WebSocket connection to the consumer.
        # Every consumer has a scope that contains information about its connection, 
        # including any positional or keyword arguments from the URL route and the currently authenticated user if any.
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
                
        # Construct a Channels group name directly from the user-specified room name, without any quoting or escaping.
        # NOTE: Group names may only contain alphanumerics, hyphens, underscores, or periods, 
        # - with a max length of 100 char according to the default backend.        
        # - code will fail if the room name contains any invalid characters or exceeds the length limit
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        # Asynchronously join the WebSocket connection to a group.
        # add the current WebSocket connection (identified by its channel name) to a group (identified by room_group_name).
        # This allows the WebSocket connection to receive messages sent to this group.
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection.
        # If you do not call accept() within the connect() method then the connection will be rejected and closed. 
        # (*but you can reject a connection if the requesting user is not authorised to perform the requested action.)
        # It is recommended that accept() be called as the last action in connect() if you choose to accept the connection.
        await self.accept()

        # send a message to the presence consumer that there is a new user online
        await self.channel_layer.send(
            "presence_channel",
            {
                "type":"add_user",
                "room_group_name": self.room_group_name,
                "username":self.scope["user"].username,
            }
        )

    # disconnect from WebSocket
    async def disconnect(self, close_code):
        """An asynchronous method to disconnect from the WebSocket.

        :param close_code: A numerical code indicating the reason for the WebSocket connection closure.
        :type close_code: int
        """
        # Leave room group
        # Asynchronously remove the current WebSocket connection (id by its channel name) from a group (id by room_group_name)
        # - ensures that the WebSocket connection will no longer receive messages sent to this group.
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

        # send a message to the presence consumer that a user disconnected from the chat app & to remove user 
        await self.channel_layer.send(
            "presence_channel",
            {
                "type":"remove_user",
                "room_group_name": self.room_group_name,
                "username":self.scope["user"].username,
            }
        )

    # Receive messages from WebSocket
    async def receive(self, text_data):
        """An asynchronous method that receives messages from the WebSocket.

        :param text_data: The message received from the WebSocket as a JSON-formatted string.
        :type text_data: str
        """
        # convert/parse the JSON-formatted string received from the WebSocket into a Python dictionary with the loads method,
        # e.g. "{key:value}" => {key:value}
        # - allowing for the extraction and use of the message content.
        text_data_json = json.loads(text_data)

        # retrieve the value associated with the key "message" from the text_data_json dictionary
        # - it's the actual message content sent through the WebSocket.
        # retrieve the value associated with the key "username" from the text_data_json dictionary
        message = text_data_json["message"]
        username = text_data_json["username"]

        # Send message to room group
        # send the message to all WebSocket connections that are part of the specified group (room_group_name).
        # send the message as a dictionary with a type identifier "chat.message" & the actual message content.
        # Django Channels uses this type identifier to call the corresponding method in the consumer that handles chat messages
        # - messages will route to chat_message()
        # send the username associated with the message to all WebSocket connections
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message, "username": username}
        )

    # Receive message from room group
    async def chat_message(self, event):
        """An asynchronous method that processes a message from the room group and sends it to the WebSocket.

        :param event: The event dictionary containing the type identifier and message content from the async def receive(self, text_data) method.
        :type event: dict
        """
        # retrieve the message content sent to the room group by extracting the value for the key "message" in the event dict
        # retrieve the username which sent the message content
        # - needed to ensure display of username in chat log
        message = event["message"]
        username = event["username"]

        # Send message to WebSocket
        # send username to WebSocket to ensure display in chat log
        # convert the Python dictionary into a JSON-formatted string for transmission to the WebSocket with dumps method
        await self.send(text_data=json.dumps({"message": message, "username": username}))

# create a class for the consumer that tracks the users who are online
class PresenceConsumer(AsyncWebsocketConsumer):
    # connect to WebSocket    
    async def connect(self):
        """An asynchronous method to connect to WebSocket. 
        """
        # https://channels.readthedocs.io/en/latest/tutorial/part_2.html#enable-a-channel-layer
        # Obtain the 'room_name' parameter from the URL route in chat/routing.py that opened the WebSocket connection to the consumer.
        # Every consumer has a scope that contains information about its connection, 
        # including any positional or keyword arguments from the URL route and the currently authenticated user if any.
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
                
        # Construct a Channels group name directly from the user-specified room name, without any quoting or escaping.
        # NOTE: Group names may only contain alphanumerics, hyphens, underscores, or periods, 
        # - with a max length of 100 char according to the default backend.        
        # - code will fail if the room name contains any invalid characters or exceeds the length limit
        # extract the room name from the URL and create a group name for online users
        self.room_group_name = f"{self.room_name}_online_users"

        # Join room group
        # Asynchronously add the WebSocket connection to a online users group.
        # add the current WebSocket connection (identified by its channel name) to a group (identified by room_group_name).
        # This allows the WebSocket connection to receive messages about who is online in the room.
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        # Accept the WebSocket connection.
        # If you do not call accept() within the connect() method then the connection will be rejected and closed. 
        # (*but you can reject a connection if the requesting user is not authorised to perform the requested action.)
        # It is recommended that accept() be called as the last action in connect() if you choose to accept the connection.
        await self.accept()
        print(f"Connected to presence channel: {self.room_group_name}") ##        

    # disconnect from WebSocket
    async def disconnect(self, close_code):
        """An asynchronous method to disconnect from the WebSocket.

        :param close_code: A numerical code indicating the reason for the WebSocket connection closure.
        :type close_code: int
        """
        # remove user from online users group
        # Asynchronously remove the current WebSocket connection (id by its channel name) from a group (id by room_group_name)
        # - ensures that the WebSocket connection will no longer receive messages sent to this group.
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)
        
        print(f"Disconnected from presence channel: {self.room_group_name}") ##

    # Receive messages from WebSocket
    async def receive(self, text_data):
        """An asynchronous method that receives messages from the WebSocket.

        :param text_data: The message received from the WebSocket as a JSON-formatted string.
        :type text_data: str
        """
        # convert/parse the JSON-formatted string received from the WebSocket into a Python dictionary with the loads method,
        # e.g. "{key:value}" => {key:value}
        # - allowing for the extraction and use of the message content.
        text_data_json = json.loads(text_data)
        
        # retrieve the value associated with the key "username" from the text_data_json dictionary        
        username = text_data_json["username"]
        
        # retrieve the value associated with the key "connection_type" from the text_data_json dictionary        
        # -  indicates whether the user is connecting ("open") or disconnecting ("close")
        # used to determine the appropriate action for updating the user's online status
        connection_type = text_data_json["connection_type"]
        print(connection_type) ##

        # Send online status to room group
        # send the online status to all WebSocket connections that are part of the specified group (room_group_name)        
        await self.change_online_status(username, connection_type)

    # method to send online status update to websocket
    async def send_onlineStatus(self, event):
        # parse event data from json format
        # extract username & status
        data = json.loads(event.get('value'))
        username = data['username']
        online_status = data['status']

        # send online status update to websocket
        await self.send(text_data=json.dumps({
            'username': username,
            'online_status': online_status
        }))

    # send a message to the WebSocket group about an online user
    # - all clients connected to this group will receive the message
    async def notify_online_status(self, username, is_online):
        await self.channel_layer.group_send(
            self.room_group_name, {"type": 'send_online_status',
                                   "username": username,
                                   "status": is_online
                                   }
                                   )

    # method to change status of users from Redis
    async def change_online_status(self, username, connection_type):
        # Use Redis directly to get the members of the group
        redis = self.channel_layer._get_client()
        if connection_type == 'open':
            await redis.sadd('online_users', username)
        else:
            await redis.srem('online_users', username)

        # call the method to send the online status notification to websocket.
        # connection_type == 'open' results in True or False, which represents whether the user is online or offline
        await self.notify_online_status(username, connection_type == 'open')
        