from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing, name="landing"),
    path("home", views.home, name="home"),
    path("sign-up", views.sign_up, name="sign_up"),
    path("landing", views.landing, name="landing"),
]
