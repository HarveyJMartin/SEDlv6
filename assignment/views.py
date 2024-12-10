from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Assignment
from .forms import AssignmentEditForm  # Assuming a form exists for proposing edits


def user_assignments(request):
    if not request.user.is_authenticated:
        return redirect("login")  # Redirect to login if the user is not authenticated

    assignments = Assignment.objects.filter(user=request.user).order_by(
        "-assigned_date"
    )  # Fetch user's assignments
    return render(
        request, "assignment/user_assignments.html", {"assignments": assignments}
    )


def propose_edit(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        form = AssignmentEditForm(request.POST, instance=assignment)
        if form.is_valid():
            changes = form.cleaned_data
            reason = request.POST.get("reason")
            assignment.propose_edit(changes, request.user, reason)
            return redirect("assignments")
    else:
        form = AssignmentEditForm(instance=assignment)
    return render(request, "assignments/propose_edit.html", {"form": form})


def request_deletion(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST":
        reason = request.POST.get("reason")
        assignment.request_deletion(request.user, reason)
        return redirect("assignments")
    return render(
        request, "assignments/request_deletion.html", {"assignment": assignment}
    )


def approve_changes(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST" and request.user.is_superuser:
        assignment.approve_changes(request.user)
        return redirect("assignments")
    current_values = {
        field: getattr(assignment, field) for field in assignment.pending_changes.keys()
    }
    return render(
        request,
        "assignments/approve_changes.html",
        {
            "assignment": assignment,
            "proposed_changes": assignment.pending_changes,
            "current_values": current_values,
        },
    )


def reject_changes(request, assignment_id):
    assignment = get_object_or_404(Assignment, id=assignment_id)
    if request.method == "POST" and request.user.is_superuser:
        assignment.reject_changes(request.user)
        return redirect("assignments")
    current_values = {
        field: getattr(assignment, field) for field in assignment.pending_changes.keys()
    }
    return render(
        request,
        "assignments/reject_changes.html",
        {
            "assignment": assignment,
            "proposed_changes": assignment.pending_changes,
            "current_values": current_values,
        },
    )
