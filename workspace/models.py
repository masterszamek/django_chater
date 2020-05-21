from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

import re


def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


def special_match(str, search=re.compile('^[a-zA-Z0-9_ ]+$')):
    """
        True -> string contain correct chars
        False -> string doesnt contain corret chars
    """
    return bool(search.match(str))


def get_workspace_room_based_slug(workspace_slug, room_slug):
    workspace = Workspace.objects.get(slug=workspace_slug)
    room = workspace.room_set.get(slug=room_slug)

    return workspace, room


def complex_user_acces_room(user, workspace_slug, room_slug):
    try:
        workspace, room = get_workspace_room_based_slug(workspace_slug, room_slug)
    except Exception as e:
        print(e)
        return False

    if workspace.user_has_access_workspace(user) and room.user_has_acces_room(user):
        return True
    else:
        return False


class Workspace(models.Model):
    """
        If public field is FALSE user has access workspace only by invite workspace admin.
        Otherwise user has also access by password
    """
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(blank=True)
    users = models.ManyToManyField(User, blank=True)
    public = models.BooleanField(default=False)
    password = models.CharField(blank=True, max_length=50)
    hidden = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("workspace:workspace", args=[self.slug])

    def user_has_access_workspace(self, user):
        if (self.public == True and self.password == "") or self.users.filter(username=user.username):
            return True

        else:
            print("user nie nalezy od workspace lub workspace nie jest publiczny")
            return False

    def clean(self):
        if not special_match(self.name):
            raise ValidationError({"name": _("Name workspace isn`t correct")})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Workspace, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Room(models.Model):
    """
            If public field is FALSE user has access room only by invite workspace admin.
            Otherwise user has also access by password
    """
    name = models.CharField(max_length=30)
    users = models.ManyToManyField(User, blank=True)
    workspace = models.ForeignKey(Workspace, blank=True, on_delete=models.CASCADE)
    slug = models.SlugField(blank=True)
    public = models.BooleanField(default=False)
    password = models.CharField(blank=True, max_length=50)
    hidden = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse("workspace:room", args=[self.workspace.slug, self.slug])

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

    def clean(self):
        if not special_match(self.name):
            raise ValidationError({"name": _("Name room isn`t correct")})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Room, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["name"]
        constraints = [
            models.UniqueConstraint(fields=['workspace', 'name'], name="unique_room_ws")
        ]


class Message(models.Model):
    text = models.TextField(blank=False)
    author = models.ForeignKey(User, blank=False, on_delete=models.SET(get_sentinel_user))
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE)
    send_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.text.isspace():
            super(Message, self).save(*args, **kwargs)
     
    class Meta:
        ordering = ['send_date']
