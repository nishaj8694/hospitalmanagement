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
app_name='patient'

from django.contrib import admin
from django.urls import path,include
from patient import views

urlpatterns = [
    # path('adm/',include('admn.urls')),
    path('Pat_signup',views.Pat_signup,name='Pat_signup'),
    path('Pat_dashboard',views.Pat_dashboard,name='Pat_dashboard'),
    path('appoiment/<int:id>',views.appoiment,name='appoiment'),
    path('Patient_appoiment',views.Patient_appointment,name='Patient_appoiment'),
    path('treatment',views.treat,name='treatment'),
    path('get_available_time_slots/', views.get_available_time_slots, name='get_available_time_slots'),
    path('pat_chat',views.pat_chat,name='pat_chat'),
    path('adres/<int:id>',views.adres,name='adres'),
    path('edit_adres/<int:id>/<int:item>',views.edit_adres,name='edit_adres'),
    path('delete_adres/<int:id>/<int:item>',views.delete_adres,name='delete_adres'),
    path('check/<int:id>',views.check,name='check'),
    path('copn/<int:id>',views.copn,name='copn'),
    path('d_order/<int:id>',views.d_order,name='d_order'),
    path('invoice/<int:id>',views.invoice,name='invoice'),
    path('ord',views.ord,name='ord'),
    path('ord_hys',views.ord_hys,name='ord_hys'),
    path('cancel_order',views.cancel_order,name='cancel_order'),
    path('refund/<int:id>',views.refund,name='refund'),
    path('p_profile',views.p_profile,name='p_profile'),
    path('ord_success/',views.ord_success,name='ord_success'),
    path('pay_cancel/<int:id>/<int:item>',views.pay_cancel,name='pay_cancel'),
    path('delet_coupen/<int:id>',views.delete_coupen,name='delet_coupen'),
    path('exam',views.exam,name='exam'),

   







    

]
