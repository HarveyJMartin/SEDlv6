from django import forms
from .models import Device


class DeviceForm(forms.ModelForm):
    class Meta:
        model = Device
        fields = ["device_type", "manufacturer", "operating_system", "model"]
        widgets = {
            "device_type": forms.Select(attrs={"class": "form-select"}),
            "manufacturer": forms.TextInput(attrs={"class": "form-control"}),
            "operating_system": forms.Select(attrs={"class": "form-select"}),
            "model": forms.TextInput(attrs={"class": "form-control"}),
        }
