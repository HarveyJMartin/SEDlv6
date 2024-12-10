from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


# User creation form extending the default djanog user creation form and adding requirement for email
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    # This is what is being created by the form, the user.
    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]
