from django.db import models
from django.contrib.auth.models import User
from devices.models import Device
from django.core.exceptions import PermissionDenied


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
        """
        Approves changes or deletion requests. Only staff users can perform this action.
        """
        if not user.is_staff:
            raise PermissionDenied("Only staff members can approve changes.")

        if self.status == "deletion_requested":
            # Approve the deletion: Delete the assignment
            self.delete()
        elif self.pending_changes:
            # Approve the proposed changes: Apply them
            for field, value in self.pending_changes.items():
                setattr(self, field, value)
            self.pending_changes = None
            self.reason_for_change = None
            self.status = "assigned"  # Reset status back to assigned
            self.save()

    def reject_changes(self, user):
        """
        Rejects changes or deletion requests. Only staff users can perform this action.
        """
        if not user.is_staff:
            raise PermissionDenied("Only staff members can reject changes.")

        if self.status == "deletion_requested":
            # Reject the deletion: Reset the status back to assigned
            self.status = "assigned"
        self.pending_changes = None
        self.reason_for_change = None
        self.save()
