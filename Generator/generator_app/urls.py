from django.urls import path

from . import views
from .views import integration, interpolation, index, custom_variants, splines

urlpatterns = [
    path('', index, name='index'),
    path('interpolation/', interpolation, name='interpolation'),
    path('integration/', integration, name='integration'),
    path('splines/', splines, name='splines'),
    path('custom_variants/', custom_variants, name='custom_variants'),
    path('generate_interpolation/', views.generate_interpolation, name='generate_interpolation'),
    path('generate_integration/', views.generate_integration, name='generate_integration'),
    path('generate_splines/', views.generate_splines, name='generate_splines')
]
