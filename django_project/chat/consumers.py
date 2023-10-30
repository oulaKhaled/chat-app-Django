from channels.generic.websocket import AsyncWebsocketConsumer
import json
from asgiref.sync import async_to_sync


class ChatRoomConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        # to know which group we should send to

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        messege = text_data_json["messege"]
        username = text_data_json["username"]
        await self.channel_layer.group_send(
            self.room_group_name,
            {"type": "chatroom_messege", "messege": messege, "username": username},
        )

    async def chatroom_messege(self, event):
        messege = event["messege"]
        username = event["username"]
        await self.send(
            text_data=json.dumps({"messege": messege, "username": username})
        )
