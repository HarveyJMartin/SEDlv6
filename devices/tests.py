from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Device
from django.urls import reverse


class DeviceViewsTest(TestCase):
    def setUp(self):
        # Set up a test client, users, and devices
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username="staffuser", password="password", is_staff=True
        )
        self.non_staff_user = User.objects.create_user(
            username="regularuser", password="password", is_staff=False
        )
        self.device = Device.objects.create(
            device_type="laptop",
            manufacturer="Dell",
            operating_system="windows_11",
            model="Latitude 5570",
        )
        # Adjust these URL names based on your actual URL patterns
        self.device_url = reverse("devices")
        self.add_device_url = reverse("add_device")
        self.edit_device_url = reverse("edit_device", kwargs={"pk": self.device.pk})
        self.delete_device_url = reverse("delete_device", kwargs={"pk": self.device.pk})

    def test_device_view_as_staff(self):
        # Login as staff user
        self.client.login(username="staffuser", password="password")
        response = self.client.get(self.device_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "devices/device_list.html")

        # Check that the device appears in the rendered list
        self.assertContains(response, "laptop")
        self.assertContains(response, "Dell")
        self.assertContains(response, "Latitude 5570")
        self.assertContains(response, "windows_11")

    def test_device_view_as_non_staff(self):
        # Login as a regular (non-staff) user
        self.client.login(username="regularuser", password="password")
        response = self.client.get(self.device_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "devices/my_devices.html")

    def test_add_device_view_get(self):
        # Only staff should access this page
        self.client.login(username="staffuser", password="password")
        response = self.client.get(self.add_device_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "devices/add_device.html")

    def test_add_device_view_post_valid_data(self):
        # Post valid data as staff
        self.client.login(username="staffuser", password="password")
        data = {
            "device_type": "mobile",
            "manufacturer": "Apple",
            "operating_system": "ios",
            "model": "iPhone 14",
        }
        response = self.client.post(self.add_device_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.device_url)
        self.assertTrue(Device.objects.filter(model="iPhone 14").exists())

    def test_add_device_view_post_invalid_data(self):
        # Post invalid data as staff
        self.client.login(username="staffuser", password="password")
        data = {
            "device_type": "",  # Missing required field
            "manufacturer": "Apple",
            "operating_system": "ios",
            "model": "iPhone 14",
        }
        response = self.client.post(self.add_device_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "devices/add_device.html")
        self.assertContains(response, "This field is required.")

    def test_edit_device_view_get(self):
        # Access edit page as staff
        self.client.login(username="staffuser", password="password")
        response = self.client.get(self.edit_device_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "devices/edit_device.html")

    def test_edit_device_view_post_valid_data(self):
        # Edit device as staff
        self.client.login(username="staffuser", password="password")
        data = {
            "device_type": "desktop",
            "manufacturer": "HP",
            "operating_system": "windows_10",
            "model": "Dev Spec",
        }
        response = self.client.post(self.edit_device_url, data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.device_url)
        self.device.refresh_from_db()
        self.assertEqual(self.device.device_type, "desktop")
        self.assertEqual(self.device.manufacturer, "HP")
        self.assertEqual(self.device.operating_system, "windows_10")
        self.assertEqual(self.device.model, "Dev Spec")

    def test_edit_device_view_post_invalid_data(self):
        # Post invalid data as staff
        self.client.login(username="staffuser", password="password")
        data = {
            "device_type": "",  # Missing required field
            "manufacturer": "HP",
            "operating_system": "windows_10",
            "model": "Dev Spec",
        }
        response = self.client.post(self.edit_device_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "devices/edit_device.html")
        self.assertContains(response, "This field is required.")

    def test_delete_device_view_get(self):
        # Access delete confirmation page as staff
        self.client.login(username="staffuser", password="password")
        response = self.client.get(self.delete_device_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "devices/confirm_delete.html")

    def test_delete_device_view_post(self):
        # Delete device as staff
        self.client.login(username="staffuser", password="password")
        response = self.client.post(self.delete_device_url)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, self.device_url)
        self.assertFalse(Device.objects.filter(pk=self.device.pk).exists())

    def test_unauthorized_access(self):
        # Accessing staff-only pages as non-staff should result in 403
        self.client.login(username="regularuser", password="password")

        response = self.client.get(self.add_device_url)
        self.assertEqual(response.status_code, 403)

        response = self.client.get(self.edit_device_url)
        self.assertEqual(response.status_code, 403)

        response = self.client.get(self.delete_device_url)
        self.assertEqual(response.status_code, 403)
