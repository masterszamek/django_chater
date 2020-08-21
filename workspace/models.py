from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse
from django.core.validators import RegexValidator

import uuid
import re


from permissions import models as permission_models

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


# def special_match(str, search=re.compile('^[a-zA-Z0-9_ ]+$')):
#     """
#         True -> string contain correct chars
#         False -> string contain incorret chars
#     """
#     return bool(search.match(str))


# def complex_user_acces_room(user, workspace_slug, room_slug):
#     try:
#         workspace, room = get_workspace_room_based_slug(workspace_slug, room_slug)
#     except Exception as e:
#         print(e)
#         return False

#     if workspace.user_has_access_workspace(user) and room.user_has_acces_room(user):
#         return True
#     else:
#         return False


class Workspace(models.Model):
    """
        If public field is FALSE user has access workspace only by invite workspace admin.
        Otherwise user has also access by password
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        validators=[RegexValidator(regex='^[a-zA-Z0-9_]+$', message="Invalid tag name")]
    )
    users = models.ManyToManyField(User, blank=True)
    public = models.BooleanField(default=False)
    password = models.CharField(blank=True, max_length=50)
    hidden = models.BooleanField(default=True)


    def user_has_access_workspace(self, user):
        if (self.public == True and self.password == "") or self.users.filter(username=user.username):
            return True

        else:
            print("user nie nalezy od workspace lub workspace nie jest publiczny")
            return False

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['id']),
        ]

class PermissionUserWorkspaceInstance(permission_models.PermissionUserInstance):

    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'workspace', 'permission'], name="unique_permission_workspace_user")
        ]

    
class Room(models.Model):
    """
            If public field is FALSE user has access room only by invite workspace admin.
            Otherwise user has also access by password
    """
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=30,
        unique=True,
        blank=False,
        validators=[RegexValidator(regex='^[a-zA-Z0-9_]+$', message="Invalid tag name")]
    )
    users = models.ManyToManyField(User, blank=True)
    workspace = models.ForeignKey(Workspace, blank=False, on_delete=models.CASCADE)
    public = models.BooleanField(default=False)
    password = models.CharField(blank=True, max_length=50)
    hidden = models.BooleanField(default=True)


    def last_n_messages(self, n=20):

        messages = self.message_set.all()
        if messages.__len__() < n:
            return messages
        else:
            return messages[messages.__len__() - n:]

    def user_has_acces_room(self, user):
        if (self.public == True and self.password == "") or self.users.filter(username=user.username):
            return True
        else:
            print("user nie nalezy do tego roomu lub nie jest publiczny")
            return False



    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=['workspace', 'name'], name="unique_room_ws")
        ]
        indexes = [
            models.Index(fields=['id']),
        ]

class PermissionUserRoomInstance(permission_models.PermissionUserInstance):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'room', 'permission'], name="unique_permission_room_user")
        ]

class LevelPermissionUserRoomInstance(permission_models.PermissionUserInstance):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'room'], name="unique_level_permission_room_user")
        ]


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    text = models.TextField(blank=False)
    author = models.ForeignKey(User, blank=False, on_delete=models.SET(get_sentinel_user))
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    send_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.text.isspace():
            super(Message, self).save(*args, **kwargs)
     
    class Meta:
        ordering = ['send_date']
        indexes = [
            models.Index(fields=['id']),
        ]