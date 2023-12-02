from django import template
register = template.Library()

@register.filter(name='rate')
def rat(quantity,price):
    total=price/quantity
    return total