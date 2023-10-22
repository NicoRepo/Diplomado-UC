from dataclasses import field
from pyexpat import model
from rest_framework import serializers
from .models import Manufacturer, Smartphone

class SmarphoneSerializer(serializers.ModelSerializer):
  class Meta:
    model = Smartphone
    fields = [
      "manufacturer",
      "name",
      "ram_gb",
      "storage_gb",
      "screen_inches",
    ]