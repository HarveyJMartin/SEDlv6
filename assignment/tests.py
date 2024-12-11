from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

from .models import Assignment
from devices.models import Device


class AssignDeviceViewTest(TestCase):
    """Tests for the assign_device view."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("assign_device")

        # Create staff and normal user
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="normal", password="password"
        )

        # Create a device for assignment
        self.device = Device.objects.create(
            device_type="laptop",
            manufacturer="Dell",
            operating_system="windows_11",
            model="Latitude 5570",
        )

    def test_assign_device_view_staff_user(self):
        """Staff user can access and use the assign_device view."""
        self.client.login(username="staff", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignment/new_assignment.html")

        post_data = {
            "device_type": self.device.id,
            "user": self.staff_user.id,
            "status": "assigned",
        }
        response = self.client.post(self.url, data=post_data)
        self.assertRedirects(response, reverse("all_assignments"))
        self.assertTrue(
            Assignment.objects.filter(
                device_type=self.device, user=self.staff_user
            ).exists()
        )

    def test_assign_device_view_non_staff_user(self):
        """
        Non-staff user should be unable to access assign_device view
        due to is_staff_user restriction.
        """
        self.client.login(username="normal", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class AllAssignmentsViewTest(TestCase):
    """Tests for the all_assignments view."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("all_assignments")

        # Create staff user and login
        self.staff_user = User.objects.create_user(
            username="staff", password="password", is_staff=True
        )
        self.client.login(username="staff", password="password")

        # Create a device and an assignment
        self.device = Device.objects.create(
            device_type="desktop",
            manufacturer="HP",
            operating_system="windows_10",
            model="EliteDesk",
        )
        self.assignment = Assignment.objects.create(
            device_type=self.device, user=self.staff_user
        )

    def test_all_assignments_accessible_by_staff(self):
        """Staff user should be able to access and see all assignments."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignment/all_assignments.html")
        self.assertIn(self.assignment, response.context["assignments"])

    def test_all_assignments_inaccessible_to_non_staff(self):
        """Non-staff user should get 403 when trying to access."""
        self.client.logout()
        normal_user = User.objects.create_user(username="normal", password="password")
        self.client.login(username="normal", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)


class UserAssignmentsViewTest(TestCase):
    """Tests for the user_assignments view."""

    def setUp(self):
        self.client = Client()
        self.url = reverse("assignments")
        self.user = User.objects.create_user(username="user", password="password")

        # Create a device and an assignment for this user
        self.device = Device.objects.create(
            device_type="tablet",
            manufacturer="Apple",
            operating_system="ios",
            model="iPad",
        )
        self.assignment = Assignment.objects.create(
            device_type=self.device, user=self.user
        )

    def test_user_assignments_accessible_by_logged_in_user(self):
        """A logged in user can access their assignments."""
        self.client.login(username="user", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "assignment/user_assignments.html")
        self.assertIn(self.assignment, response.context["assignments"])
