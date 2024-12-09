from django.urls import path
from .views import device_view, add_device_view, edit_device_view, delete_device_view

urlpatterns = [
    path('devices/', device_view, name='devices'),
    path('devices/add/', add_device_view, name='add_device'),
    path('edit/<int:pk>/', edit_device_view, name='edit_device'),
    path('delete/<int:pk>/', delete_device_view, name='delete_device'),
]
