"""hosp_mng URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))

"""
app_name='home'

from django.contrib import admin
from django.urls import path,include
from home import views

urlpatterns = [
    # path('adm/',include('admn.urls')),
    path('',views.home,name='home'),
    path('contact',views.contact,name='contact'),
    path('about',views.about,name='about'),
    path('docter',views.docter,name='docter'),
    path('department',views.department,name='department'),
    path('signin',views.signin,name='signin'),
    path('lout', views.lout, name='lout'),
    path('item/',views.item,name='item'),
    path('medicine/<str:med>',views.medicine,name='medicine'),
    # path('tablet',views.tablet,name='tablet'),
    # path('capsule',views.capsule,name='capsule'),
    # path('syrup',views.syrup,name='syrup'),
    # path('oiment',views.oiment,name='oiment'),
    # path('powder',views.powder,name='powder'),
    # path('gel',views.gel,name='gel'),
    path('checkout',views.checkout,name='checkout'),
    path('order/<int:item>',views.order,name='order'),
    path('cart',views.cart,name='cart'),
    path('decr/<int:id>',views.decr,name='decr'),
    path('incr/<int:id>',views.incr,name='incr'),
    path('delet_cartItem/<int:id>',views.delet_cartItem,name='delet_cartItem'),
    path('add_cart/<int:id>',views.add_cart,name='add_cart'),
    path('product_page/<int:id>',views.product_page,name='product_page'),
    path('forgotP/',views.forgetP,name='forgotP'),
    path('changeP/<str:token>',views.changeP,name='changeP'),
    path("index", views.index, name="index"),
    path('adres',views.adres,name='adres'),
    path('remark/<int:id>',views.edit_address,name='remark'),
    path('delete_address',views.delete_address,name='delete_address'),
    path('coupon',views.coup,name='coupon'),
    path('delet_session',views.delete_session,name='delet_session'),
    path('high/<str:item>', views.high, name='high'),
    path('low/<str:item>', views.low, name='low'),
    path('success/',views.success,name='success'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('verify_email/<str:id>',views.verify_email,name='verify_email'),
    path('payment_cancel/<int:id>',views.payment_cancel,name='payment_cancel'),
    path('verification',views.verification,name='verification'),
    
    # path('hat',views.message,name='hat'),
     
]
