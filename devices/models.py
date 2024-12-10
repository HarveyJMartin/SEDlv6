from django.db import models


class Device(models.Model):
    DEVICE_TYPE_CHOICES = [
        ("laptop", "Laptop"),
        ("mobile", "Mobile"),
        ("desktop", "Desktop"),
        ("tablet", "Tablet"),
    ]
    OPERATING_SYSTEM_CHOICES = [
        ("windows_11", "Windows 11"),
        ("windows_10", "Windows 10"),
        ("macos", "macOS"),
        ("ios", "iOS"),
        ("linux", "Linux"),
    ]

    device_type = models.CharField(max_length=20, choices=DEVICE_TYPE_CHOICES)
    manufacturer = models.CharField(max_length=50)
    operating_system = models.CharField(max_length=20, choices=OPERATING_SYSTEM_CHOICES)
    model = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.manufacturer} {self.model} ({self.device_type}) ({self.operating_system})"
