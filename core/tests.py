from django.test import TestCase, Client, override_settings
from django.urls import path, reverse
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

from .views import is_staff_user


@user_passes_test(is_staff_user)
def staff_only_dummy_view(request):
    return HttpResponse("Staff only content")


# Define urlpatterns at module level
urlpatterns = [
    path("dummy-view/", staff_only_dummy_view, name="staff_only_dummy_view"),
]


# Only testing custom login requirements as the builtin django logged in is trusted.
@override_settings(ROOT_URLCONF="core.tests")
class IsStaffUserTest(TestCase):
    """Tests to ensure is_staff_user function works as intended."""

    def setUp(self):
        self.client = Client()
        self.staff_user = User.objects.create_user(
            username="staffuser", password="password", is_staff=True
        )
        self.normal_user = User.objects.create_user(
            username="normaluser", password="password"
        )
        self.url = reverse("staff_only_dummy_view")

    def test_is_staff_user_allows_staff_access(self):
        """Staff user should be able to access the protected view."""
        self.client.login(username="staffuser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Staff only content")

    def test_is_staff_user_denies_non_staff_access(self):
        """Non-staff user should get a 403 error trying to access the protected view."""
        self.client.login(username="normaluser", password="password")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 403)
