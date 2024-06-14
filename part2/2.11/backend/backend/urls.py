"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from django_api.views import ua_frontlines_geojson
from django_api.views import upload_geojson
from django_api.views import fetch_and_upload_bbg_data
from django_api.views import blackbird_group_geojson

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/ua_frontlines/', ua_frontlines_geojson, name='ua_frontlines_geojson'),
    path('api/upload_geojson/', upload_geojson, name='upload_geojson'),
    path('api/fetch_and_upload_bbg_data/', fetch_and_upload_bbg_data, name='fetch_and_upload_bbg_data'),
    path('api/blackbird_group/', blackbird_group_geojson, name='blackbird_group_geojson'),
] 