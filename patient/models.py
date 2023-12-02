from django.db import models
from django.conf import settings

# Create your models here.
class patientProfile(models.Model):
    choice=(
        ('Male','Male'),
        ('Female','Female')
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='patient_profile')
    contact_number = models.CharField(max_length=15,null=True)
    gender=models.CharField(max_length=100,  choices=choice)
    image=models.ImageField(upload_to='pat')
    is_verify=models.BooleanField(default=False)
    email_verify=models.BooleanField(default=False)
    # address=models.TextField(max_length=200,null=True,blank=True)


    def __str__(self):
        return self.user.username


class wallet(models.Model):
    PatientProfile=models.ForeignKey(patientProfile,on_delete=models.CASCADE,null=True)
    amount=models.PositiveIntegerField(null=True)


class Address(models.Model):
    Patient = models.ForeignKey(patientProfile, on_delete=models.CASCADE, related_name='adres',null=True)
    Name=models.CharField(max_length=30,null=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    district = models.CharField(max_length=50,null=True)
    state = models.CharField(max_length=50)
    country=models.CharField(max_length=100,null=True)
    Pin_code = models.CharField(max_length=10)
    contact=models.PositiveIntegerField(null=True)
    email=models.EmailField(null=True,blank=True)
    # def __str__(self):
    #     return self.user.username


