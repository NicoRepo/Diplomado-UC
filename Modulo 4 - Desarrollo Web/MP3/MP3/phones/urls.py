from django.urls import path, re_path, include
from . import views


urlpatterns = [
    path('manufacturers/', views.manufacturers_index, name='manufacturers'),
    path('manufacturers/get', views.GetCompanies.as_view(), name='get_manufacturers'),
    path('smartphones/create/', views.smartphone_create, name='smartphone_create'),

]
