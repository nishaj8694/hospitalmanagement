from .models import DoctorProfile,Department
from django import forms
from django.forms import ModelForm

class doc_form(forms.ModelForm):
    class Meta:
        model=DoctorProfile
        exclude=['user','email_verify','is_verify','is_available','consult_start','consult_end']


class department_form(forms.ModelForm):
    class Meta:
        model=Department
        fields='__all__'        