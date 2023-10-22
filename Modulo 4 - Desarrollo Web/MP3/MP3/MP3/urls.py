"""MP3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.routers import DefaultRouter
from phones import views as phone_views

router = DefaultRouter()
router.register('phones', phone_views.SmarthPoneViewSet)

schema_view = get_schema_view(
    openapi.Info(
        title='Phones API',
        default_version='v1',
        description="API for Phones APP"
    ),
    public=True
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('phones/', include('phones.urls')),
    path("api/v1/", include(router.urls)),
    re_path(r"^api/v1/swagger/(?P<format>\.json\.yaml)$", schema_view.without_ui(cache_timeout=0), name="schema-json"),
    re_path(r"^api/v1/swagger/$", schema_view.with_ui(cache_timeout=0), name="schema-swagger-ui"),
    re_path(r"^api/v1/redoc/$", schema_view.with_ui(cache_timeout=0), name="schema-redoc")
]
