# from django.contrib.auth.models import AbstractUser,User
from django.db.models.signals import post_save
from django.dispatch import receiver
from docter.models import DoctorProfile
from patient.models import patientProfile
from home.models import Cart,User,CartItem
from django.conf import settings
import json
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#         if created:
#             print(instance.is_patient,
#                   instance.is_docter,
#                   instance.is_active,
#                   instance.username)
            
#             if instance.is_docter:
#                 print('created docter before')
#                 DoctorProfile.objects.create(user=instance)
#                 print('created docter after')


#             if  instance.is_patient :
#                 print('created patient before')
#                 sampl=patientProfile.objects.create(user=instance)
#                 sampl.save()
#                 child=Cart.objects.create(user=instance)
#                 child.save()                
#                 print('created patient afte')

# @receiver(post_save, sender=User)
# def send_onlineStatus(sender, instance, created, **kwargs):
#     if not created:
#         channel_layer = get_channel_layer()
#         user = instance.username
#         user_status = instance.online

#         data = {
#             'username':user,
#             'status':user_status
#         }
#         async_to_sync(channel_layer.group_send)(
#             'user', {
#                 'type':'send_onlineStatus',
#                 'value':json.dumps(data)
#             }
#         )



# post_save.connect(create_user,sender=CartItem ,dispatch_uid="create_user")              