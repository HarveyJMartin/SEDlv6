from django.core.exceptions import PermissionDenied


def is_staff_user(user):
    if not user.is_staff:
        raise PermissionDenied  # Raises a 403 Forbidden response
    return True
