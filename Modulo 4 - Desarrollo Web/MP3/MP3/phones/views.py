from .models import Manufacturer, Smartphone
from django.shortcuts import render, redirect
from django.views import View
from django.http import JsonResponse
from rest_framework import viewsets
from .forms import SmartphoneForm, CompanyNumber, ManufacturerForm
from .models import Manufacturer
from .serializers import SmarphoneSerializer
from requests import get
from datetime import date

class SmarthPoneViewSet(viewsets.ModelViewSet):
    queryset = Smartphone.objects.all()
    serializer_class = SmarphoneSerializer

def manufacturers_index(request):
    manufacturers = Manufacturer.objects.all()
    context = {'manufacturers': manufacturers}
    return render(request, 'phones/manufacturers.html', context)

def smartphone_create(request):
    if request.method == 'POST':
        form = SmartphoneForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manufacturers')
    else:
        form = SmartphoneForm()
    context = {'form': form}
    return render(request, 'phones/smartphone_create.html', context)

class GetCompanies(View):
    form_class = CompanyNumber
    manufacturer_class = ManufacturerForm
    template_name = "phones/get_manufacturers.html"
    companies_ep = "https://fakerapi.it/api/v1/companies?_quantity={}"

    def get(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        return render(request, self.template_name, context={"form": form})

    def post(self, request, *args, **kwargs):
        try:
            form = self.form_class(request.POST)
            if form.is_valid():
                companies_amount = form.data.get('quantity', 0)
                r = get(self.companies_ep.format(companies_amount), headers={"Content-Type": "application/json"})
                if r.status_code >= 200 and r.status_code <= 300 or not companies_amount:
                    data = r.json()
                    companies = data.get("data", [])
                    for company in companies:                
                        #NOTE: JSON Company Object does not contain date_founded attribute so date.today() will be used instead
                        m = Manufacturer(
                            name=company.get("name"), country=company.get("name"), webpage=company.get('website'), date_founded=date.today())
                        m.save()
                    return redirect('manufacturers')
                else:
                    return JsonResponse({"STATUS": "KO"})
        except Exception as e:
            return JsonResponse({"STATUS": "KO", "REASON": e})
       