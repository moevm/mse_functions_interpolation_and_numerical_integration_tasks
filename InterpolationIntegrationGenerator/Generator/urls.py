from django.urls import path, include

urlpatterns = [
    path('', include('interpolation_integration_generator.urls')),
]
