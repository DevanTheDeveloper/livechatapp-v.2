from channels.generic.websocket import AsyncWebsocketConsumer
import json
import time

class ChatRoomConsumer(AsyncWebsocketConsumer):

	http_user = True


	async def connect(self):
		self.roomName = self.scope['url_route']['kwargs']['roomName']
		self.room_group_name = 'chat_%s' % self.roomName 
		self.user = self.scope['user'].username
		
	


		
		await self.channel_layer.group_add(
				self.room_group_name,
				self.channel_name
			)


		await self.accept()

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type':'broadcastJoined',
				'username':self.user
			})

	async def broadcastJoined(self,event):
		username = event['username']

		await self.send(text_data=json.dumps({'username':username,
												'message':'has joined the room.'}))




	async def disconnect(self, close_code):

		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type':'broadcastDisconnect',
				'username':self.user
			})


		await self.channel_layer.group_discard(
				self.room_group_name,
				self.channel_name
			)


	async def broadcastDisconnect(self,event):
		username = event['username']

		await self.send(text_data=json.dumps({'username':username,
												'message':'has left the room.'}))

	async def receive(self,text_data):
		text_data_json = json.loads(text_data)
		message = text_data_json.get('message','')
		username = text_data_json.get('username','')
		status = text_data_json.get('status','')

	
		await self.channel_layer.group_send(
			self.room_group_name,
			{
				'type':'chatroom_message',
				'message':message,
				'username':username
			})


	async def chatroom_message(self,event):
		message = event['message']
		
		username = event['username'] 

		await self.send(text_data=json.dumps({
			'message':message,
			'username':username,
			}))




	pass 