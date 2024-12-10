from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_assignments, name="assignments"),
    path("<int:assignment_id>/propose_edit/", views.propose_edit, name="propose_edit"),
    path(
        "<int:assignment_id>/request_deletion/",
        views.request_deletion,
        name="request_deletion",
    ),
    path(
        "<int:assignment_id>/approve_changes/",
        views.approve_changes,
        name="approve_changes",
    ),
    path(
        "<int:assignment_id>/reject_changes/",
        views.reject_changes,
        name="reject_changes",
    ),
]
