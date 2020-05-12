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
            rooms = workspace.room_set.filter(hidden=False, public=True) | workspace.room_set.filter(users=request.user)
            users = workspace.users.all()


            try:
                room.objects.get(users=request.user)
            except Exception as E:
                room.users.add(request.user)

            context = {
                "workspace": workspace,
                "current_room": room,
                "messages": room.last_n_messages(15),
                "rooms_in_workspace": rooms,
                "users": users,
            }
            return render(request, "workspace/room.html", context=context)
        else:
            raise PermissionDenied


class Workspace(LoginRequiredMixin, View):

    def get(self, request, workspace_slug):
        workspace = get_object_or_404(models.Workspace, slug=workspace_slug)

        if workspace.user_has_access_workspace(request.user):
            try:
                workspace.objects.get(users=request.user)

            except Exception as E:
                workspace.users.add(request.user)


            for room in workspace.room_set.all():
                if room.user_has_acces_room(request.user):
                    return redirect(room)

            context = {"workspace": workspace}
            return render(request, "workspace/workspace.html", context=context)
        else:
            raise PermissionDenied

