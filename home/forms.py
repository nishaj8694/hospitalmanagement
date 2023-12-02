from .models import Appointment,Refund
from django import forms
from django.forms import ModelForm
from datetime import datetime


class dateinput(forms.DateInput):
    input_type='date'
    
    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.attrs['min']=datetime.now().date()
        self.attrs['style'] = 'background-color: transparent;'

class timeinput(forms.TimeInput):  
    input_type='time'


# class texti(forms.Select):
#     attrs='background-color:black'
    
class texti(forms.Select):
    def __init__(self, attrs=None):
        attrs = attrs or {}
        attrs['style'] = 'color-yellow;background-color: transparent'
        super().__init__(attrs)

class Patient_form(forms.ModelForm):
    class Meta:
        model=Appointment
        exclude=['created_at','status','appointment_time','patient']
        widgets ={
            'appointment_date': dateinput,
            'docter':texti,
            'reason':forms.Textarea(attrs={'style': 'background-color: transparent;'})
            # 'appointment_time':timeinput

        }

# class Patient_form(forms.ModelForm):
#     class Meta:
#         model=Appointment
#         exclude=['created_at','status','patient']
        

class refund_form(forms.ModelForm):
    class Meta:
        model=Refund
        exclude=['order' , 'status' , 'cancelby' , 'refund_amount']