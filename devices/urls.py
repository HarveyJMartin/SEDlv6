from django.urls import path
from .views import device_view

urlpatterns = [
    path('devices/', device_view, name='devices'),
]
