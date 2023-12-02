from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
import datetime
class Department(models.Model):
    name= models.CharField(max_length=100)
      
    def __str__(self):
        return self.name  

class DoctorProfile(models.Model):
    choice=(
        ('Male','Male'),
        ('Female','Female')
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='doctor_profile')
    specialization = models.CharField(max_length=50)
    gender=models.CharField(max_length=100,  choices=choice)
    image=models.ImageField(upload_to='doc')
    email_verify=models.BooleanField(default=False,null=True)
    is_verify=models.BooleanField(default=False,null=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,null=True)
    address=models.TextField(max_length=200,null=True)
    residence=models.TextField(max_length=200,null=True)
    contact_number = models.CharField(max_length=15,null=True)
    badge_id=models.CharField(max_length=50,null=True)
    is_available=models.BooleanField(default=False)
    consult_start = models.TimeField(default=datetime.time(14, 0))  # Set default time to 2:00 PM
    consult_end = models.TimeField(default=datetime.time(20, 0))
    def __str__(self):
        # return str(self.user)
        # return f"{self.user} ({self.department.name})"
         return f"{self.user} ({self.department.name if self.department else 'No Department'})"
    
