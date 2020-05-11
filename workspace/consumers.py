import json
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from .models import complex_user_acces_room, Message, Room, Workspace
from channels.db import database_sync_to_async

ONLINE_USERS = {}


GROUP_NAMES = {
    # "w-slug" mean workspace slug
    # "r-slug" mean room slug
    "user_status": lambda w_slug, sep="-": "user_status{sep}{w_slug}{sep}".format(sep=sep, w_slug=w_slug),
    "messages": lambda w_slug, r_slug, sep="-": "messages{sep}{w_slug}{sep}{r_slug}{sep}".format(sep=sep, r_slug=r_slug, w_slug=w_slug),
}


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        self.user = self.scope["user"]
        self.workspace_slug = self.scope["url_route"]["kwargs"]["workspace_slug"]
        self.room_slug = self.scope["url_route"]["kwargs"]["room_slug"]

        if self.user.is_anonymous:
            print("annonymous won")
            await self.close()
        if await database_sync_to_async(complex_user_acces_room)(self.user,
                                                                 self.workspace_slug,
                                                                 self.room_slug
                                                                 ):
            await self.accept()
            await self.after_connect()

        else:
            await self.disconnect(code="no chyba nie")

    async def disconnect(self, code):
        del ONLINE_USERS[self.workspace_slug][self.user.username]
        await self.channel_layer.group_send(
            GROUP_NAMES["user_status"](w_slug=self.workspace_slug),
            {
                "type": "set.user.status",
                "username": self.user.username,
                "status": "offline",
            }
        )

    async def receive_json(self, text_data=None, bytes_data=None):
        command = text_data["command"]
        args = tuple(text_data["args"])
        print(command)

        # await self.__dict__[command](*args)
        await self.new_message(*args)
        print(dir(self))
        print(self.scope)
        print(self.user, text_data)


    async def after_connect(self):
        if self.workspace_slug not in ONLINE_USERS.keys():
            ONLINE_USERS[self.workspace_slug] = {}
        ONLINE_USERS[self.workspace_slug][self.user.username] = "active"

        await self.send_json({"command": "username", "args": [self.user.username]})
        await self.channel_layer.group_add(GROUP_NAMES["user_status"](w_slug=self.workspace_slug), self.channel_name)
        await self.channel_layer.group_add(GROUP_NAMES["messages"](w_slug=self.workspace_slug, r_slug=self.room_slug),
                                           self.channel_name)

        await self.channel_layer.group_send(

            GROUP_NAMES["user_status"](w_slug=self.workspace_slug),
            {
                "type": "set.user.status",
                "username": self.user.username,
                "status": "active",
            }
        )
        await self.get_users_status()

    async def new_message(self, text):
        try:
            def f(text):
                workspace = Workspace.objects.get(slug=self.workspace_slug)
                room = workspace.room_set.get(slug=self.room_slug)
                message = Message(text=text, room=room, workspace=workspace, author=self.user)

                message.save()
                return message

            message = await database_sync_to_async(f)(text)

            await self.channel_layer.group_send(
                GROUP_NAMES["messages"](w_slug=self.workspace_slug, r_slug=self.room_slug),
                {
                    "type": "broadcast.message",
                    "username": self.user.username,
                    "text": message.text,

                }
            )
        except Exception as e:
            print(e)

    async def broadcast_message(self, event):
        content = {
            "command": "new_message",
            "args": [event["username"], event["text"]]
        }

        await self.send_json(content)

    async def get_users_status(self):
        content = {
            "command": "get_users_status",
            "args": [ONLINE_USERS[self.workspace_slug]]
        }

        await self.send_json(content)

    async def set_user_status(self, event):
        content = {
            "command": "set_user_status",
            "args": [event["status"], event["username"]]
        }
        await self.send_json(content)
