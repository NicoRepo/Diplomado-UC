from django.db import models
import datetime

class FabricanteSmartPhones(models.Model):
  nombre = models.CharField(max_length=255)
  pais_origen = models.CharField(max_length=255)
  fecha_fundacion = models.DateField(default=datetime.date.today)
  link_pagina_web = models.URLField(default=None)


class SmartPhone(models.Model):
  nombre = models.CharField(max_length=255)
  fabricante = models.ForeignKey(FabricanteSmartPhones, on_delete=models.CASCADE)
  ram = models.IntegerField()
  almacenamiento = models.IntegerField()
  tamaño_pantalla = models.CharField(max_length=255)