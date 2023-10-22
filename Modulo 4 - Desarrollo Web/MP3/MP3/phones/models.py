from django.db import models
from datetime import date

class Manufacturer(models.Model):
    name = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    date_founded = models.DateField('Foundation date')
    webpage = models.URLField()

    def __str__(self):
        return self.name


class Smartphone(models.Model):
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    ram_gb = models.DecimalField('RAM memory in GB', max_digits=4, decimal_places=2)
    storage_gb = models.DecimalField('Storage in GB', max_digits=6, decimal_places=2)
    screen_inches = models.DecimalField('Screen size in inches', max_digits=4, decimal_places=2)
    release_date = models.DateField(default=date.today)

    def __str__(self):
        return self.manufacturer.name + ' ' + self.name
