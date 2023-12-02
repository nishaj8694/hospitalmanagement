from django.db import models
from django.contrib.auth.models import AbstractUser,User
from django.db.models.signals import post_save
from django.dispatch import receiver
from docter.models import DoctorProfile
from patient.models import patientProfile,Address
from django.conf import settings
from admn.models import Product,varient,coupen 
from asgiref.sync import sync_to_async
  


user=settings.AUTH_USER_MODEL

class User(AbstractUser):
    is_patient=models.BooleanField(default=False)
    is_docter=models.BooleanField(default=False)
    block=models.BooleanField(default=False)
    online=models.BooleanField(default=False)
    f_passw=models.CharField(max_length=1000,null=True,blank=True)
    
    

class Cart(models.Model):
    user=models.OneToOneField(User,on_delete=models.SET_NULL ,null=True)
    created= models.DateTimeField(auto_now_add=True)
    
     
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    Varient=models.ForeignKey(varient,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    
    def __str__(self):
         return str(self.product)

class Order(models.Model):
    data=(
          ('pending','pending'),
          ('shiped','shiped'),
          ('deliverd','deliverd'),
          ('cancel','cancel'),
          ('revoke','revoke')
     )
    user=models.ForeignKey(User,on_delete=models.SET_NULL ,null=True)
    Total_Price = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    address=models.ForeignKey(Address,on_delete=models.CASCADE,null=True)
    Pay_option=models.CharField(max_length=10,null=True)
    order_date= models.DateTimeField(auto_now_add=True)
    delivery_date= models.DateTimeField(blank=True,null=True)
    cancel_date= models.DateTimeField(blank=True,null=True)
    status=models.CharField(max_length=10,choices=data,default="pending",null=True,blank=True) 
    discount=models.ForeignKey(coupen,on_delete=models.SET_NULL,null=True) 
    razor_payid=models.CharField(max_length=200,null=True,blank=True)
    razor_orderid=models.CharField(max_length=200,null=True,blank=True) 
    razor_signature=models.CharField(max_length=200,null=True,blank=True) 
        

       
    def __str__(self):
         return str(self.user)
    
     
class orderItem(models.Model):
    order = models.ForeignKey(Order, related_name='order_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,null=True)
    Varient =models.ForeignKey(varient,on_delete=models.CASCADE,null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(default=0,max_digits=10, decimal_places=2)
    
    def __str__(self):
         return str(self.product)


class Refund(models.Model):
    data=(
          ('pending','pending'),
          ('Process' ,'Process'),
          ('cancel','cancel'),
          ('completed','completed'),
     )
    mony=(
          ('bank','bank'),
          ('wallet','wallet'),
     )
    user=(
          ('admin','admin'),
          ('user','user'),
     )
    order= models.ForeignKey(Order, related_name='order_refund',on_delete=models.CASCADE,null=True,blank=True)
    refund_option=models.CharField(max_length=10,choices=mony,default="wallet",null=True,blank=True) 
    refund_reason=models.CharField(max_length=200,null=True,blank=True)
    status=models.CharField(max_length=10,choices=data,default="pending",null=True,blank=True) 
    cancelby=models.CharField(max_length=100,choices=user,default="none",null=True,blank=True)
    refund_amount=models.PositiveIntegerField(null=True,blank=True)

    def __str__(self):
         return str(self.pk)

class Appointment(models.Model):
     data=(
          ('Pending','Pending'),
          ('accept','accept'),
          ('reject','reject'),
          ('finish','finish'),
     )
     patient=models.ForeignKey(patientProfile,on_delete=models.CASCADE,null=True,blank=True)
     docter=models.ForeignKey(DoctorProfile,on_delete=models.CASCADE,null=True,blank=True)
     appointment_date=models.DateField(null=True,blank=True)
     appointment_time=models.TimeField(null=True,blank=True)
     reason=models.TextField(max_length=500)
     status=models.CharField(max_length=10,choices=data,default="pending",null=True,blank=True)    
     created_at= models.DateTimeField(auto_now_add=True)
      
     def __str__(self):
          # doctor = sync_to_async(lambda: self.doctor)()
          # return str(doctor)
          return str(self.docter)      
 

                                              
class treatment(models.Model):
     appointment=models.ForeignKey(Appointment,on_delete=models.CASCADE,related_name='OP')
     symtems=models.TextField(max_length=500)
     ordstatus=models.BooleanField(default=False)

     def __str__(self):
          return str(self.appointment)   


class TreatMedicine(models.Model):
        Treatment=models.ForeignKey(treatment , on_delete=models.CASCADE,related_name='treat',null=True)
        medicine = models.ForeignKey(varient, on_delete=models.CASCADE,related_name='sup')
        quantity = models.PositiveIntegerField(default=0) 
        
            