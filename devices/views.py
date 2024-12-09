from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import DeviceForm
from devices.models import Device

import logging

logger = logging.getLogger(__name__)

def is_staff_user(user):
    return user.is_staff

@login_required
def device_view(request):
    if request.user.is_staff:
            from django.db import connection
            devices = Device.objects.all()
            return render(request, 'devices/device_list.html', {'devices': devices})
    else:
        return render(request, 'devices/my_devices.html')  # Path relative to the templates folder


# # @user_passes_test(is_staff_user)
# # @login_required
# def device_list_view(request):



@user_passes_test(is_staff_user)
@login_required
def add_device_view(request):
    if request.method == 'POST':
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("Device added successfully")
            print("Device added successfully")
            return redirect('devices')
        else:
            logger.warning("Form is invalid: %s", form.errors)
            print("Form is invalid:", form.errors)
    else:
        form = DeviceForm()
        print("Rendering empty form")

    return render(request, 'devices/add_device.html', {'form': form})