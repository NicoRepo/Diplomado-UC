from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .models import SmartPhone, FabricanteSmartPhones
from .forms import FabricanteSmartPhonesForm, SmartPhoneForm

class AgregarFabricante(View):
  form_class = FabricanteSmartPhonesForm
  template_name = 'agregar_fabricante.html'

  def get(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    return render(request, self.template_name, {'form': form})

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    if form.is_valid():
      action = form.save()
      return JsonResponse({"STATUS": "OK"})
    
class AgregarSmartPhone(View):
  form_class = SmartPhoneForm
  template_name = 'agregar_smartphone.html'

  def get(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    return render(request, self.template_name, {'form': form})

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    if form.is_valid():
      action = form.save()
      return JsonResponse({"STATUS": "OK"})
    return JsonResponse({"STATUS": "KO"})

class AgregarSmartPhone(View):
  form_class = SmartPhoneForm
  template_name = 'agregar_smartphone.html'

  def get(self, request, *args, **kwargs):
    form = self.form_class()
    return render(request, self.template_name, {'form': form})

  def post(self, request, *args, **kwargs):
    form = self.form_class(request.POST)
    if form.is_valid():
      action = form.save()
      return JsonResponse({"STATUS": "OK"})
    else: return JsonResponse({"STATUS": "KO"})

class ListarSmartPhones(View):
  template_name = 'listar_smartphones.html'

  def get(self, request, *args, **kwargs):
    smartphones = SmartPhone.objects.all()
    fabricantes = FabricanteSmartPhones.objects.all()
    grouped_data = {
      fabricante.id: {"nombre": fabricante.nombre, "equipos": []} for fabricante in fabricantes
    }
    data = [
      {
        "nombre": smartphone.nombre,
        "fabricante": smartphone.fabricante.nombre,
        "ram": f"{smartphone.ram} GB",
        "almacenamiento": f"{smartphone.almacenamiento} GB",
        "group_key": smartphone.fabricante.id,
        "tamaño_pantalla": smartphone.tamaño_pantalla,
      }
      for smartphone in smartphones
    ]
    for d in data:
      if grouped_data.get(d['group_key']):
        grouped_data[d['group_key']]['equipos'].append(d)
    #return JsonResponse(grouped_data, safe=False)
    return render(request, self.template_name, context={'fabricantes': grouped_data.values()})