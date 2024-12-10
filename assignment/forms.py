from django import forms
from .models import Assignment


class AssignmentEditForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ["notes", "status"]  # Add other editable fields as needed
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 4}),
            "status": forms.Select(),
        }
        labels = {
            "notes": "Assignment Notes",
            "status": "Status",
        }
