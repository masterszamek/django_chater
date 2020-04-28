import json
from channels.generic.websocket import AsyncWebsocketConsumer, AsyncJsonWebsocketConsumer
from .models import complex_user_acces_room
from channels.db import database_sync_to_async

ONLINE_USERS = {}


class ChatConsumer(AsyncJsonWebsocketConsumer):

    async def fetch_messages(self, data):
        pass

    async def connect(self):

        self.user = self.scope['user']
        self.workspace_slug = self.scope['url_route']['kwargs']['workspace_slug']
        self.room_slug = self.scope['url_route']['kwargs']['room_slug']

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
            "user_status-{}-".format(self.workspace_slug),
            {
                "type": "set.user.status",
                "username": self.user.username,
                "status": "offline",
            }
        )

    async def receive_json(self, text_data=None, bytes_data=None):
        print(dir(self))
        print(self.scope)
        print(text_data)

    async def get_users_status(self):
        content = {
            "command": "get_users_status",
            "args": [ONLINE_USERS[self.workspace_slug]]
        }

        await self.send_json(content)



    async def after_connect(self):
        if self.workspace_slug not in ONLINE_USERS.keys():
            ONLINE_USERS[self.workspace_slug] = {}
        ONLINE_USERS[self.workspace_slug][self.user.username] = "active"

        await self.send_json({"command": "username", "args": [self.user.username]})
        await self.channel_layer.group_add("user_status-{}-".format(self.workspace_slug), self.channel_name)
        await self.channel_layer.group_add("messages-{}-{}-".format(self.workspace_slug, self.room_slug), self.channel_name)
        await self.channel_layer.group_send(

            "user_status-{}-".format(self.workspace_slug),
            {
                "type": "set.user.status",
                "username": self.user.username,
                "status": "active",
            }
        )
        await self.get_users_status()


    async def set_user_status(self, event):
        content = {
            "command": "set_user_status",
            "args": [event["status"], event["username"]]
        }
        await self.send_json(content)

    # async def set_user_status(self, user, status):
    # """status: possible choices online, away, offline"""
    #     pass
