from django.urls import path
from .views import Room, Workspace


app_name = "workspace"
urlpatterns = [
    path("<slug:workspace_slug>/", Workspace.as_view(), name="workspace"),
    path("<slug:workspace_slug>/<slug:room_slug>/", Room.as_view(), name="room"),


]