from django.urls import path, include

urlpatterns = [
    path('', include('generator_app.urls')),
]
