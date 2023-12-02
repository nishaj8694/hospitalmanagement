
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from asgiref.sync import sync_to_async
from channels.generic.websocket import WebsocketConsumer
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from home.models import User,Appointment
from docter.models import DoctorProfile
from patient.models import patientProfile


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        username = str(self.scope["user"])
        self.room_name =a=self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        
        user_id = self.scope['user'].id
        user_qs = await sync_to_async(User.objects.filter)(id=user_id)
        await sync_to_async(user_qs.update)(online=True)
        username = str(self.scope["user"])
        
        user_s = await sync_to_async(User.objects.filter)(id=user_id)
        user = await sync_to_async(user_s.first)()
        me_online = user.online if user else False
        
        if user.is_docter:
            op = await sync_to_async(Appointment.objects.get)(id=int(self.room_name))
            details = await sync_to_async(patientProfile.objects.get)(id=op.patient_id)
            other = await sync_to_async(User.objects.get)(id=details.user_id)
            image_url = details.image.url if details.image else ''
            online = other.online if other else False

        if user.is_patient:
            op = await sync_to_async(Appointment.objects.get)(id=int(self.room_name))
            images = await sync_to_async(DoctorProfile.objects.get)(id=op.docter_id)            
            other = await sync_to_async(User.objects.get)(id=images.user_id)
            image_url = images.image.url if images.image else ''
            online = other.online if other else False


        await self.channel_layer.group_add(
            self.room_group_name, self.channel_name
        )

          

        await self.accept()


        await self.channel_layer.group_send(
            self.room_group_name,
        {
            'type': 'chat_join',
            'username': username,
            'online':online,
            'me_online':me_online,
            'images':image_url,
            'profile':other.username  
            # 'details':deteils 
        }
    )


    async def disconnect(self, close_code):
        user_id = self.scope['user'].id
        user_qs = await sync_to_async(User.objects.filter)(id=user_id)
        await sync_to_async(user_qs.update)(online=False)
        username = str(self.scope["user"])
        
        user_s = await sync_to_async(User.objects.filter)(id=user_id)
        user = await sync_to_async(user_s.first)()
        me_online = user.online if user else False

        await self.channel_layer.group_send(
            self.room_group_name,
        {
            'type': 'chat_leave',
            'username':username,
            'me_online':me_online 
        }
    )

    
        
        await self.channel_layer.group_discard(
            self.room_group_name, self.channel_name
            
        )


        

    async def receive(self, text_data):
       
          text_data_json = json.loads(text_data)
          message = text_data_json['message']
          username = str(self.scope["user"])

          await self.channel_layer.group_send(
             self.room_group_name,
             {
                'type': 'chat_message',
                'message': message,
                'username': username,
            }
        )
          


    async def chat_message(self, event):
        message = event['message']
        username = event["username"]
        
        css_class = 'current-user' if username == self.scope["user"].username else 'other-user'

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'css_class':css_class,

            

     }))
        
    async def chat_leave(self, event):
    
        username = event["username"]
        me_online = event['me_online']
        

        await self.send(text_data=json.dumps({

            'username': username,
            'me_online': me_online,

            

     })) 

    async def chat_join(self, event):
    
        username = event["username"]
        online = event['online']
        me_online = event['me_online']
        images = event['images']
        profile= event['profile']
        # details = event['details']


        await self.send(text_data=json.dumps({

            'username': username,
            'is_online': online,
            'me_online': me_online,
            'images' : images,
            'profile': profile

            # 'details': details

            

     }))        

   

# class OnlineConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         username = str(self.scope["user"])
#         self.room_name =a=self.scope["url_route"]["kwargs"]["room_name"]
#         self.room_group_name = "chat_%s" % self.room_name
        
#         user_id = self.scope['user'].id
#         user_qs = await sync_to_async(User.objects.filter)(id=user_id)
#         await sync_to_async(user_qs.update)(online=True)
#         username = str(self.scope["user"])
        
#         user_s = await sync_to_async(User.objects.filter)(id=user_id)
#         user = await sync_to_async(user_s.first)()
#         online = user.online if user else False

        
       
#         await self.channel_layer.group_add(
#             self.room_group_name, self.channel_name
#         )

          

#         await self.accept()


#         await self.channel_layer.group_send(
#             self.room_group_name,
#         {
#             'type': 'chat_join',
#             'username': 'username',
#             'online':online 
#         }
#     )


#     async def disconnect(self, close_code):
#         user_id = self.scope['user'].id
#         user_qs = await sync_to_async(User.objects.filter)(id=user_id)
#         await sync_to_async(user_qs.update)(online=False)
#         username = str(self.scope["user"])
        
#         user_s = await sync_to_async(User.objects.filter)(id=user_id)
#         user = await sync_to_async(user_s.first)()
#         online = user.online if user else False

#         await self.channel_layer.group_send(
#             self.room_group_name,
#         {
#             'type': 'chat_leave',
#             'username': 'username',
#             'online':online 
#         }
#     )

    
        
#         await self.channel_layer.group_discard(
#             self.room_group_name, self.channel_name
            
#         )

    
#     async def chat_leave(self, event):
    
#         username = event["username"]
#         online = event['online']
        

#         await self.send(text_data=json.dumps({

#             'username': username,
#             'is_online': online,

            

#      })) 

    # async def chat_join(self, event):
    
    #     username = event["username"]
    #     online = event['online']
        

    #     await self.send(text_data=json.dumps({

    #         'username': username,
    #         'is_online': online,

            

    #  }))        