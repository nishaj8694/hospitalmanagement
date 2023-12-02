# """
# ASGI config for hosp_mng project.

# It exposes the ASGI callable as a module-level variable named ``application``.

# For more information on this file, see
# https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
# """

# import os
# import home.routing
# from django.core.asgi import get_asgi_application
# from channels.routing import ProtocolTypeRouter,URLRouter
# from  channels.auth import AuthMiddlewareStack

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hosp_mng.settings')

# application = ProtocolTypeRouter({
#     'http':get_asgi_application(),
#     'websocket':AuthMiddlewareStack(
#             URLRouter(
#                         home.routing.websocket_urlpatterns
#                 )
#     )
# })
"""
ASGI config for chat project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from channels.security.websocket import AllowedHostsOriginValidator
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hosp_mng.settings')
import home.routing

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
                        AuthMiddlewareStack(URLRouter(home.routing.websocket_urlpatterns))
              ),
        # Just HTTP for now. (We can add other protocols later.)
    }
)

