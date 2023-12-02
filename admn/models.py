from django.db import models


class Company(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    

class Medicine_type(models.Model):
    name=models.CharField(max_length=100)
    medicine_type=models.ForeignKey('self',on_delete=models.CASCADE,related_name='subcate', blank=True,null=True)

    def __str__(self):
        return self.name

class Catagory(models.Model):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(max_length=500)
    is_available=models.BooleanField(default=False,null=True,blank=True)
    image=models.ImageField(upload_to='media',null=True)
    catagory=models.ForeignKey(Catagory,on_delete=models.CASCADE,null=True,blank=True)
    medicine_type=models.ForeignKey(Medicine_type,on_delete=models.CASCADE,null=True,blank=True,limit_choices_to={'medicine_type': None})
    company=models.ForeignKey(Company,on_delete=models.CASCADE,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True) 
    def __str__(self):
        return self.name



class varient(models.Model):
    data=(
        ('10ml','10ml'),
        ('20ml','20ml'),
        ('30ml','30ml'),
        ('50ml','50ml'),
        ('60ml','60ml'),
        ('100ml','100ml'),
        ('150ml','150ml'),
        ('200ml','200ml'),
        ('250ml','250ml'),
        ('500ml','500ml'),
        ('750ml','750ml'),
        ('1000ml','100ml'),
        ('500gm','500gm'),
        ('650gm','650gm'),
        ('1100gm','1100gm'),
        ('1600gm','1600gm'),         
    )
    product=models.ForeignKey(Product,on_delete=models.CASCADE,blank=True,null=True,related_name='item')
    size=models.CharField(max_length=100,choices=data,blank=True,null=True)
    price=models.IntegerField(blank=True,null=True)
    stock=models.PositiveBigIntegerField(max_length=None,blank=True,null=True)
 
 
    def __str__(self):
        return f'{self.product.name}({self.size})'

class coupen(models.Model):
    name=models.CharField(max_length=100)
    discount_price=models.PositiveBigIntegerField()
    expairy_date=models.DateField(null=True)    
    def __str__(self):
        return self.name
 

