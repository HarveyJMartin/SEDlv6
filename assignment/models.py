from django.db import models
from django.contrib.auth.models import User
from devices.models import Device


class Assignment(models.Model):
    STATUS_CHOICES = [
        ("assigned", "Assigned"),
        ("returned", "Returned"),
        ("lost", "Lost"),
        ("damaged", "Damaged"),
        ("deletion_requested", "Deletion Requested"),
    ]

    device_type = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="assignments"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assignments")
    assigned_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="assigned")
    notes = models.TextField(blank=True, null=True)

    # Soft delete and edit functionality
    is_active = models.BooleanField(default=True)  # For soft delete
    edited_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="edited_assignments",
    )
    pending_changes = models.JSONField(
        blank=True, null=True
    )  # Stores proposed edits in JSON format
    reason_for_change = models.TextField(
        blank=True, null=True
    )  # Reason for edits or deletion

    def request_deletion(self, user, reason):
        """Marks the assignment as requesting deletion with a reason."""
        self.status = "deletion_requested"
        self.is_active = False
        self.edited_by = user
        self.reason_for_change = reason
        self.save()

    def propose_edit(self, changes, user, reason):
        """Stores proposed changes and reason for approval."""
        self.pending_changes = changes
        self.edited_by = user
        self.reason_for_change = reason
        self.save()

    def approve_changes(self, user):
        """Applies the proposed changes if the user is a superuser."""
        if not user.is_superuser:
            raise PermissionError("Only superusers can approve changes.")
        if self.pending_changes:
            for field, value in self.pending_changes.items():
                setattr(self, field, value)
            self.pending_changes = None
        self.reason_for_change = None
        self.save()

    def reject_changes(self, user):
        """Rejects proposed changes if the user is a superuser."""
        if not user.is_superuser:
            raise PermissionError("Only superusers can reject changes.")
        self.pending_changes = None
        self.reason_for_change = None
        self.save()

    def __str__(self):
        return f"{self.device_type} assigned to {self.user} on {self.assigned_date}"
