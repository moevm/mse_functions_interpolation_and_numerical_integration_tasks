from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path(r'generate_interpolation/', views.generate_interpolations, name='generate_interpolations')
]
