from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Assignment
from .forms import AssignmentEditForm, AssignmentForm
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied
from django.contrib import messages


def is_staff_user(user):
    if not user.is_staff:
        raise PermissionDenied  # Raises a 403 Forbidden response
    return True


@user_passes_test(is_staff_user)
def assign_device(request):
    if request.method == "POST":
        form = AssignmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("all_assignments")
    else:
        form = AssignmentForm()
    return render(request, "assignment/new_assignment.html", {"form": form})


@user_passes_test(is_staff_user)
def delete_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":  # Perform deletion
        assignment.delete()
        return redirect("all_assignments")
    # For GET requests, render the confirmation page
    return render(request, "assignment/confirm_delete.html", {"assignment": assignment})


def requested_changes(request):
    edit_requests = Assignment.objects.filter(pending_changes__isnull=False)
    delete_requests = Assignment.objects.filter(status="deletion_requested")
    return render(
        request,
        "assignment/requested_changes.html",
        {
            "edit_requests": edit_requests,
            "delete_requests": delete_requests,
        },
    )


@user_passes_test(is_staff_user)
def all_assignments(request):
    # Fetch all assignments regardless of status or changes
    assignments = Assignment.objects.all().order_by("-assigned_date")
    return render(
        request, "assignment/all_assignments.html", {"assignments": assignments}
    )


@user_passes_test(is_staff_user)
def edit_assignment(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        form = AssignmentForm(request.POST, instance=assignment)
        if form.is_valid():
            form.save()
            return redirect("all_assignments")
    else:
        form = AssignmentForm(instance=assignment)
    return render(
        request,
        "assignment/edit_assignment.html",
        {"form": form, "assignment": assignment},
    )


def user_assignments(request):
    if not request.user.is_authenticated:
        return redirect("login")

    assignments = Assignment.objects.filter(user=request.user).order_by(
        "-assigned_date"
    )
    return render(
        request, "assignment/user_assignments.html", {"assignments": assignments}
    )


def propose_edit(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Check for any pending request
    if assignment.pending_changes or assignment.status == "deletion_requested":
        messages.error(
            request,
            "This assignment already has a pending request. Please wait for it to be resolved.",
        )
        return redirect("assignments")  # Redirect to My Assignments page

    if request.method == "POST":
        form = AssignmentEditForm(request.POST, instance=assignment)
        if form.is_valid():
            changes = form.cleaned_data
            reason = request.POST.get("reason")
            assignment.propose_edit(changes, request.user, reason)
            messages.success(request, "Your proposal has been submitted successfully.")
            return redirect("assignments")  # Redirect to My Assignments page
    else:
        form = AssignmentEditForm(instance=assignment)
    return render(request, "assignment/propose_edit.html", {"form": form})


def request_deletion(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)

    # Check for any pending request
    if assignment.pending_changes or assignment.status == "deletion_requested":
        messages.error(
            request,
            "This assignment already has a pending request. Please wait for it to be resolved.",
        )
        return redirect("assignments")  # Redirect to My Assignments page

    if request.method == "POST":
        reason = request.POST.get("reason")
        assignment.request_deletion(request.user, reason)
        messages.success(
            request, "Your deletion request has been submitted successfully."
        )
        return redirect("assignments")  # Redirect to My Assignments page
    return render(
        request, "assignment/request_deletion.html", {"assignment": assignment}
    )


@user_passes_test(is_staff_user)
def approve_changes(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST" and request.user.is_staff:
        assignment.approve_changes(request.user)
        messages.success(request, "Request approved successfully.")
        return redirect("all_assignments")
    proposed_changes = assignment.pending_changes or {}
    changes = [
        {
            "field": field,
            "current_value": getattr(assignment, field, None),
            "proposed_value": value,
        }
        for field, value in proposed_changes.items()
    ]
    return render(
        request,
        "assignment/approve_changes.html",
        {
            "assignment": assignment,
            "changes": changes,
        },
    )


@user_passes_test(is_staff_user)
def reject_changes(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST" and request.user.is_staff:
        assignment.reject_changes(request.user)
        messages.success(request, "Request rejected successfully.")
        return redirect("all_assignments")
    proposed_changes = assignment.pending_changes or {}
    changes = [
        {
            "field": field,
            "current_value": getattr(assignment, field, None),
            "proposed_value": value,
        }
        for field, value in proposed_changes.items()
    ]
    return render(
        request,
        "assignment/reject_changes.html",
        {
            "assignment": assignment,
            "changes": changes,
        },
    )
