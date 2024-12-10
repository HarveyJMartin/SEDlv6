from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import DeviceForm
from devices.models import Device
from django.core.exceptions import PermissionDenied

import logging

logger = logging.getLogger(__name__)


def is_staff_user(user):
    if not user.is_staff:
        raise PermissionDenied  # Raises a 403 Forbidden response
    return True


@login_required
def device_view(request):
    if request.user.is_staff:
        devices = Device.objects.all()
        return render(request, "devices/device_list.html", {"devices": devices})
    else:
        return render(
            request, "devices/my_devices.html"
        )  # Path relative to the templates folder


@user_passes_test(is_staff_user)
@login_required
def add_device_view(request):
    if request.method == "POST":
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            logger.info("Device added successfully")
            print("Device added successfully")
            return redirect("devices")
        else:
            logger.warning("Form is invalid: %s", form.errors)
            print("Form is invalid:", form.errors)
    else:
        form = DeviceForm()
        print("Rendering empty form")

    return render(request, "devices/add_device.html", {"form": form})


@user_passes_test(is_staff_user)
@login_required
def edit_device_view(request, pk):
    try:
        device = Device.objects.get(pk=pk)
    except Device.DoesNotExist:
        logger.error(f"Device with id {pk} does not exist.")
        return redirect("devices")

    if request.method == "POST":
        form = DeviceForm(request.POST, instance=device)
        if form.is_valid():
            form.save()
            logger.info(f"Device with id {pk} updated successfully.")
            return redirect("devices")
        else:
            logger.warning(f"Form is invalid for device id {pk}: {form.errors}")
    else:
        form = DeviceForm(instance=device)

    return render(request, "devices/edit_device.html", {"form": form, "device": device})


@user_passes_test(is_staff_user)
@login_required
def delete_device_view(request, pk):
    try:
        device = Device.objects.get(pk=pk)
    except Device.DoesNotExist:
        logger.error(f"Device with id {pk} does not exist.")
        return redirect("devices")

    if request.method == "POST":
        device.delete()
        logger.info(f"Device with id {pk} deleted successfully.")
        return redirect("devices")

    return render(request, "devices/confirm_delete.html", {"device": device})
