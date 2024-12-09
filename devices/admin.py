from django.contrib import admin
from .models import Device

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('device_type', 'manufacturer', 'operating_system', 'model')
    search_fields = ('manufacturer', 'model')
