from django.urls import path
from .views import device_view, add_device_view

urlpatterns = [
    path('devices/', device_view, name='devices'),
    path('devices/add/', add_device_view, name='add_device'),
]
