from django import forms
from .models import Smartphone, Manufacturer


class SmartphoneForm(forms.ModelForm):
    class Meta:
        model = Smartphone
        fields = ['manufacturer', 'name', 'ram_gb', 'storage_gb', 'screen_inches', 'release_date']
        exclude = []
        widgets = {
            "release_date": forms.DateInput(format=("%Y-%m-%d"), attrs={"type": "date"})
        }

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Smartphone
        exclude = []




class CompanyNumber(forms.Form):
    quantity = forms.IntegerField(min_value=0, label="N° Compañias")