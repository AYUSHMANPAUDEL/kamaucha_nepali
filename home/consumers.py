from channels.consumer import SyncConsumer , AsyncConsumer
from channels.exceptions import StopConsumer
from asgiref.sync import async_to_sync
from home.models import Donation
import json

class alert_consumer(AsyncConsumer):
     async def websocket_connect(self, event):
        print("WebSocket connected...")
        self.user_id = self.scope['url_route']['kwargs']['userId']
        self.group_name = f'user_{self.user_id}'  # Define a group name
        origin = self.get_origin()
        print(origin)
        allowed_origins = [
            'https://www.your-website.com',
            'http://127.0.0.1:8000',
            'http://127.0.0.1:8001',  # Corrected localhost entry
            'http://localhost:8000',   # Added another common way to access localhost
            'http://away-peers.gl.at.ply.gg:5318',  # Another allowed origin
        ]
        if origin in allowed_origins:
            # Add the channel to the group
            await self.channel_layer.group_add(self.group_name, self.channel_name)  
            await self.send({
            "type": "websocket.accept"  # Accept the WebSocket connection
        })  # Accept the WebSocket connection
        else:
          print("user form another origin (url)")
          raise StopConsumer

     async def websocket_receive(self, event):
        data = json.loads(event['text'])  # Load the JSON data
        print(f"Received donation data: {data}")

        # Broadcast the data to all connected clients
        await self.channel_layer.group_send(
            self.group_name, 
            {
                "type": "send_alert",
                "data": data
            }
        )
     def get_origin(self):
        # Extract the 'Origin' header from the list of headers
        for header in self.scope['headers']:
            if header[0] == b'origin':
                return header[1].decode('utf-8')  # Decode bytes to string
        return None

     async def send_alert(self, event):
        data = event["data"]  # Get the data from the event
        await self.send({
           'type': 'websocket.send',
           'text': json.dumps(data)})  # Send the data back to the client

     async def websocket_disconnect(self, event):
        print("WebSocket disconnected...")
        await self.channel_layer.group_discard(self.group_name, self.channel_name)