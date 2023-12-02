from django import template
register = template.Library()
from home.models import Cart,CartItem
from admn.models import coupen
from patient.models import wallet

@register.filter
def endswith(value, arg):
    return value.endswith(arg)


@register.filter(name='total')
def total(price,quantity):
    total=price*quantity
   
    return total

@register.filter(name='subtotal')
def subtotal(item):
    stotal=0
    for i in item:
        stotal+=i.quantity*i.price
        
    return stotal


@register.filter(name='totalprice')
def totalprice(item,prom):
    id=int(prom)
    cp=coupen.objects.get(id=id)
    stotal=0
    for i in item:
        stotal+=i.quantity*i.price

    if prom:
        stotal=stotal-cp.discount_price
        return stotal
    else:    
        return stotal

@register.filter(name='totprice')
def totalprice(item):
    stotal=0
    for i in item:
        stotal+=i.quantity*i.price
        
    return stotal    

@register.filter(name='discount')
def discount(prom):
    id=int(prom)
    cp=coupen.objects.get(id=id)
    stotal=cp.discount_price
    return stotal    


@register.filter(name='summery')
def summery(sm,prom):
    id=int(prom)
    cp=coupen.objects.get(id=id)
    stotal=int(sm)-int(cp.discount_price)
    return stotal 

@register.filter(name='walt')
def walt(sm,user,prom):
    id=int(prom)
    print(user,'user')
    cp=coupen.objects.get(id=id)
    stotal=int(sm)-int(cp.discount_price)
    wal=wallet.objects.get(PatientProfile__user_id=user)
    if wal:
          walet=wal.amount
          return walet
    else:
        return 0 

