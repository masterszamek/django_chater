from django.urls import path, include
from .views import room, Workspace

from rest_framework_nested import routers

app_name = "workspace"

router = routers.SimpleRouter()
router.register(r'workspace', workspace_viewset)

workspace_router = routers.NestedSimplerouter(router, r'workspace', lookup="workspace")
workspace_router.register(r'room', room_viewset)

room_router = routers.NestedSimpleRouter(workspace_router, r'room', lookup="room")
room_router = router.register(r'messages', message_viewset)


api_urlpatterns = [
    path("", include(router.urls)),
    path("", include(workspace_router.urls)),
    path("", include(room_router.urls)),
]