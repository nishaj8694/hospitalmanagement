from .models import Address,patientProfile
from django import forms
from django.forms import ModelForm
from datetime import datetime

class adrs_form(forms.ModelForm):
    class Meta:
        model=Address
        exclude=['Patient']
        

class patient_form(forms.ModelForm):
    class Meta:
        model=patientProfile
        exclude=['user','is_verify','email_verify']
                