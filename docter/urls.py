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
app_name='docter'

from django.contrib import admin
from django.urls import path,include
from docter import views

urlpatterns = [

 path('doc_dashboard',views.doc_dashboard,name='doc_dashboard'),
 path('doc_appointment',views.doc_appointment,name='doc_appointment'),
 path('today_appointment',views.today_appointment,name='today_appointment'),
 path('update_is_available',views.update_is_available,name='update_is_available'),
 path('docno',views.doc_Product,name='docno'),
 path('doc_Profile',views.doc_profile,name='doc_Profile'),
 path('doc_edit_profile',views.doc_edit_profile,name='doc_edit_profile'),
 path('appointment_status/<int:id>/<str:keyword>',views.appointment_status,name='appointment_status'),
 path('priscribe/<int:id>',views.prescribe,name='prescribe'),
 path('myPatient',views.myPatient,name='myPatient'),
 path('today_Patient',views.today_Patient,name='today_Patient'),
 path('doc_chat',views.doc_chat,name='doc_chat'),
 path('doc_Password',views.doc_Password,name='doc_Password'),
#  path('incr/<int:id>',views.incr,name='incr'),
#  path('pre2/<int:id>',views.pre2,name='pre2'),
 path('changeTime',views.changeTime,name='changeTime'),
 path('exam',views.exam,name='exam'),

 







 
]
