from django.views import View
from django.urls import reverse

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist

from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from . import models
from .forms import HiddenRoomForm

from django.utils.translation import ugettext_lazy as _
from django.forms import ValidationError


@login_required
def room(request, workspace_slug, room_slug):
    if models.complex_user_acces_room(request.user, workspace_slug, room_slug):
        workspace, room = models.get_workspace_room_based_slug(workspace_slug, room_slug)
        rooms = workspace.room_set.filter(hidden=False, public=True)
        user_rooms = workspace.room_set.filter(users=request.user)
        users = workspace.users.all()
        form = HiddenRoomForm()

        try:
            room.objects.get(users=request.user)
        except Exception as E:
            room.users.add(request.user)

        if request.POST:
            form = HiddenRoomForm(request.POST)
            if form.is_valid():
                room_name = form.cleaned_data.get("name")
                room_password = form.cleaned_data.get("password")
                try:
                    hidden_room = workspace.room_set.get(name=room_name, public=True)

                    if hidden_room.password != room_password:
                        raise ValidationError(_("Password is incorect"))
                    hidden_room.users.add(request.user)
                    return redirect(hidden_room)

                except ObjectDoesNotExist as E:
                    form.add_error(None, "room doesn`t exist")
                except ValidationError as E:
                    form.add_error(None, E.message)

        context = {
            "workspace": workspace,
            "current_room": room,
            "messages": room.last_n_messages(15),
            "rooms_in_workspace": rooms,
            "user_rooms":user_rooms,
            "users": users,
            "form": form,
            "url": room.get_absolute_url
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
