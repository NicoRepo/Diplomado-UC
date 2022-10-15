# django
from django.urls import path

# music views
from .views import IndexView


urlpatterns = [
    path('', IndexView.as_view()),
]
