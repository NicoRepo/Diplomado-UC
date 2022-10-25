# django
from django.urls import path

# music views
from .views import AgregarFabricante, AgregarSmartPhone, ListarSmartPhones


urlpatterns = [
  path('agregar_fabricante', AgregarFabricante.as_view(), name="AgregarFabricante"),
  path('agregar_smartphone', AgregarSmartPhone.as_view(), name="AgregarSmartPhone"),
  path('listar_smartphones', ListarSmartPhones.as_view(), name="ListarSmartPhones"),
]
