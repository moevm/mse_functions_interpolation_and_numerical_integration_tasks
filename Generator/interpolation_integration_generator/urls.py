from django.conf.urls import url
from django.urls import path

from . import views
from .views import index

urlpatterns = [
    path('', index, name='index'),
    path('generate_interpolation/', views.generate_interpolations, name='generate_interpolations'),
    path('generate_integration/', views.generate_integration, name='generate_integration')
]
