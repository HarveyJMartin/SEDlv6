from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def device_view(request):
    if request.user.is_staff:
        return render(request, 'devices/device_list.html')  # Path relative to the templates folder
    else:
        return render(request, 'devices/my_devices.html')  # Path relative to the templates folder
