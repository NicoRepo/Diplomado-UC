from django import forms
from .models import FabricanteSmartPhones, SmartPhone 

class FabricanteSmartPhonesForm(forms.ModelForm):
  class Meta:
    model = FabricanteSmartPhones
    fields = ('nombre', 'pais_origen', 'fecha_fundacion', 'link_pagina_web')
    widgets = {
      'nombre': forms.TextInput(attrs={
          'class': 'form-control', 
          'placeholder': 'Nombre Fabricante', 
          'type': 'text'
        }
      ),
      'pais_origen': forms.TextInput(attrs={
          'class': 'form-control', 
          'placeholder': 'Nombre Fabricante', 
          'type': 'text'
        }
      ),
      'fecha_fundacion': forms.DateInput(format=('%d-%m-%y'), attrs={
          'class': 'form-control', 
          'placeholder': 'Fecha de Fundación', 
          'type': 'date'
        }
      ),
      'link_pagina_web': forms.TextInput(attrs={
          'class': 'form-control', 
          'placeholder': 'Nombre Fabricante', 
          'type': 'text'
        }
      ),
    }

class FabricanteChoiceField(forms.ModelChoiceField):
  def label_from_instance(self, obj):
    return obj.nombre

class SmartPhoneForm(forms.ModelForm):
  class Meta:
    model = SmartPhone
    fields = ('nombre', 'fabricante', 'ram', 'almacenamiento', 'tamaño_pantalla')
    widgets = {
      'nombre': forms.TextInput(attrs={
          'class': 'form-control', 
          'placeholder': 'Nombre SmartPhone', 
          'type': 'text'
        }
      ),
      'ram': forms.NumberInput(
        attrs={
         'class': 'form-control', 
         'placeholder': 'RAM', 
         'type': 'number'
        }
      ),
      'almacenamiento': forms.NumberInput(
        attrs={
         'class': 'form-control', 
         'placeholder': 'Almacenamiento', 
         'type': 'number'
        }
      ),
      'tamaño_pantalla': forms.TextInput(attrs={
          'class': 'form-control', 
          'placeholder': 'Tamaño Pantalla (ej: 1600x900)', 
          'type': 'text'
        }
      ),
    }
  fabricante = FabricanteChoiceField(queryset=FabricanteSmartPhones.objects.all(),
      widget=forms.Select(attrs={"class": "form-select"})
    )