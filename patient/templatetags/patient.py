from django import template
register = template.Library()
from home.models import Cart,CartItem
from datetime import datetime, timedelta

@register.filter(name='ttl')
def ttl(price,quantity):
    total=price*quantity
    return total


@register.filter(name='expaire')
def expaire(date):
    exp=date+timedelta(days=15)
    today=datetime.now().date()
    if exp>today:
        return True
    else:
        return False