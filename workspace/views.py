from django.shortcuts import render, Http404
from django.http import HttpResponse
from django.views import View
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect

from . import models


class Room(LoginRequiredMixin, View):

    def get(self, request, workspace_slug, room_slug):
        if models.complex_user_acces_room(request.user, workspace_slug, room_slug):
            workspace, room = models.get_workspace_room_based_slug(workspace_slug, room_slug)
            rooms = workspace.room_set.filter(public=True) | workspace.room_set.filter(users=request.user)
            users = workspace.users.all()
            print(workspace, room, rooms, users, sep="\n")
            context = {
                "workspace": workspace,
                "current_room": room,
                "messages": room.message_set.all(),
                "rooms_in_workspace": rooms,
                "users": users,
            }
            return render(request, "workspace/room.html", context=context)
        else:
            raise Http404


class Workspace(LoginRequiredMixin, View):

    def get(self, request, workspace_slug):
        workspace = get_object_or_404(models.Workspace, slug=workspace_slug)

        if workspace.user_has_access_workspace(request.user):


            for room in workspace.room_set.all():
                if room.user_has_acces_room(request.user):
                    return redirect(room)

            context = {"workspace": workspace}
            return render(request, "workspace/workspace.html", context=context)
        else:
            raise PermissionDenied
