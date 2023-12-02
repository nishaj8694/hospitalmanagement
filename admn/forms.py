from .models import Product,varient,coupen,Medicine_type
from django import forms
from django.forms import ModelForm
from datetime import datetime,date


class pform(forms.ModelForm):
    class Meta:
        model=Product
        fields='__all__'
        widgets = {
            'medicine_type': forms.Select(attrs={'class': 'form-control', 'id': 'id_category'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}),
        }
    print('koioioio')
    def __init__(self, *args, **kwargs):
        super(pform, self).__init__(*args, **kwargs)

        if self.instance and self.instance.medicine_type and self.instance.medicine_type.subcate.exists():
            print('haiiiii')
            subcategory_choices = [(sub.id, sub.name) for sub in self.instance.medicine_type.subcate.all()]
            self.fields['subcategory'] = forms.ChoiceField(choices=subcategory_choices, widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_subcategory'}))
      

class vform(forms.ModelForm):
    class Meta:
        model=varient
        # fields='__all__'
        exclude=['product']

class dateinput(forms.DateInput):
    input_type='date'

    def __init__(self,*args, **kwargs):
        super().__init__(*args,**kwargs)
        self.attrs['min']=datetime.now().date()
    


class coupenform(forms.ModelForm):
    class Meta:
        model=coupen        
        fields='__all__'
        widgets ={
            'expairy_date': dateinput,

        }

class medicineform(forms.ModelForm):
    class Meta:
        model=Medicine_type
        fields='__all__'
                
MONTH_NAMES = [
    None,
    'January',
    'February',
    'March',
    'April',
    'May',
    'June',
    'July',
    'August',
    'September',
    'October',
    'November',
    'December'
]
class MonthYearWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        widgets = [
            forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Choose Year')] + [(year, year) for year in range(2000, 2100)]),
            forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Choose Month')] + [(month, month) for month in range(1, 13)]),
        ]
        super().__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return [value.year, value.month]
        return [None, None]

class MonthYearField(forms.MultiValueField):
    widget = MonthYearWidget

    def __init__(self, *args, **kwargs):
        fields = (
            forms.IntegerField(),
            forms.IntegerField(),
        )
        super().__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        if data_list[0] and data_list[1]:
            return date(year=data_list[0], month=data_list[1], day=1)
        return None

class MonthYearForm(forms.Form):
    month_year = MonthYearField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['month_year'].widget.months = MONTH_NAMES[1:]
