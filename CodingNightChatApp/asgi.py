"""
ASGI config for CodingNightChatApp project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# https://channels.readthedocs.io/en/latest/installation.html#installation
# adjust the project’s asgi.py file, e.g. CodingNightChatApp/asgi.py, to wrap the Django ASGI application
# import ProtocolTypeRouter & URLRouter
# https://channels.readthedocs.io/en/latest/tutorial/part_2.html#write-your-first-consumer
# URLRouter will examine the HTTP path of the connection to route it to a particular consumer, based on the provided url patterns
from channels.routing import ProtocolTypeRouter, URLRouter

# import AuthMiddlewareStack to populate the connection’s scope with a reference to the currently authenticated user, 
# -(similar to how Django’s AuthenticationMiddleware populates the request object of a view with the currently authenticated user) 
# - then the connection will be given to the URLRouter
from channels.auth import AuthMiddlewareStack

# import routing
from ChatApp.routing import websocket_urlpatterns

# import Middleware to ensure WebSocket connections are only accepted from allowed hosts defined in ALLOWED_HOSTS,
# - preventing Cross-Site WebSocket Hijacking (CSWSH) by verifying the request's origin.
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodingNightChatApp.settings')

# https://channels.readthedocs.io/en/latest/installation.html#installation
# initialise Django ASGI application early to ensure the AppRegistry is populated
# - before importing code that may import ORM models.
# changed application to django_asgi_app
# application = get_asgi_application() -> this initialises a standard ASGI application that can handle HTTP requests.
django_asgi_app = get_asgi_application()

# Now, create a more flexible ASGI application that uses ProtocolTypeRouter to route different types of protocols (e.g., HTTP, WebSocket).
# add websocket to ProtocolTypeRouter list
# when connecting to the Channels development server, the ProtocolTypeRouter will first inspect the type of connection
# - if it is a WebSocket connection (ws:// or wss://), the connection will be given to the AuthMiddlewareStack
application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
        ),
    }
)


