from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import  AuthMiddlewareStack
import workspace.routing


application = ProtocolTypeRouter({

    'websocket': AuthMiddlewareStack(
            URLRouter(workspace.routing.websocket_urlpatterns)
        ),
})