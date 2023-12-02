from django.contrib import admin
from .models import *
from home.models import User
# Register your models here.
admin.site.register(Catagory),
admin.site.register(Product),
admin.site.register(varient),
admin.site.register(Medicine_type),
admin.site.register(Company),
admin.site.register(User),

