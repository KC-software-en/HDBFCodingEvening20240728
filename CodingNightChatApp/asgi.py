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
# import ProtocolTypeRouter
from channels.routing import ProtocolTypeRouter

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CodingNightChatApp.settings')

# https://channels.readthedocs.io/en/latest/installation.html#installation
# initialise Django ASGI application early to ensure the AppRegistry is populated
# - before importing code that may import ORM models.
# changed application to django_asgi_app
# application = get_asgi_application() -> this Iinitialises a standard ASGI application that can handle HTTP requests.
# Now, create a more flexible ASGI application that uses ProtocolTypeRouter to route different types of protocols (e.g., HTTP, WebSocket).
django_asgi_app = get_asgi_application()
application = ProtocolTypeRouter({
    "http": django_asgi_app,
    # Just HTTP for now. (We can add other protocols later.)
})


