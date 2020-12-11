from django.urls import path

from . import views
from .views import integration, interpolation

urlpatterns = [
    path('interpolation/', interpolation, name='interpolation'),
    path('integration/', integration, name='integration'),
    path('generate_interpolation/', views.generate_interpolation, name='generate_interpolation'),
    path('generate_integration/', views.generate_integration, name='generate_integration')
]
