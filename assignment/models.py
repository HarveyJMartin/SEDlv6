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
    previous_status = models.CharField(max_length=50, null=True, blank=True)

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

    def request_deletion(self, reason):
        """
        Handles deletion requests. Stores the current status before requesting deletion.
        """
        if self.status == "deletion_requested":
            raise ValueError("This assignment already has a deletion request pending.")

        self.previous_status = self.status  # Store the current status
        self.status = "deletion_requested"  # Set status to deletion requested
        self.reason_for_change = reason
        self.save()

    def propose_edit(self, changes, user, reason):
        """
        Store proposed changes in the `pending_changes` field. Changes are not applied immediately.
        """
        if self.pending_changes:
            raise ValueError("There are already pending changes for this assignment.")

        # Store proposed changes
        self.pending_changes = changes
        self.reason_for_change = reason
        self.save()

    def approve_changes(self, user):
        """
        Approves proposed changes. Only staff users can perform this action.
        """
        if not user.is_staff:
            raise PermissionDenied("Only staff members can approve changes.")

        if self.pending_changes:
            # Apply proposed changes
            for field, value in self.pending_changes.items():
                setattr(self, field, value)  # Dynamically update the fields
            # Clear pending changes
            self.pending_changes = None
            self.reason_for_change = None
            self.save()  # Save the updated instance
        elif self.status == "deletion_requested":
            # Approve deletion request: Delete the assignment
            self.delete()

    def reject_changes(self, user):
        """
        Rejects proposed changes or deletion requests. Only staff users can perform this action.
        """
        if not user.is_staff:
            raise PermissionDenied("Only staff members can reject changes.")

        if self.pending_changes:
            # Reject proposed changes by discarding them
            self.pending_changes = None
            self.reason_for_change = None
        elif self.status == "deletion_requested":
            # Revert to the previous status before the deletion request
            self.status = self.previous_status or "assigned"
            self.previous_status = None  # Clear the previous status
        self.save()
