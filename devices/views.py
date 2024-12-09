from django.core.paginator import Paginator
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Device

@login_required
def device_view(request):
    if request.user.is_staff:
        return render(request, 'devices/device_list.html')  # Path relative to the templates folder
    else:
        return render(request, 'devices/my_devices.html')  # Path relative to the templates folder


@login_required
def device_list_view(request):
    devices = Device.objects.all().order_by('manufacturer')  # Retrieve all devices
    paginator = Paginator(devices, 15)  # 15 devices per page
    page_number = request.GET.get('page')  # Get current page number from the query parameter
    page_obj = paginator.get_page(page_number)  # Get devices for the current page

    return render(request, 'devices/device_list.html', {'page_obj': page_obj})