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


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ['device_type', 'user', 'status', 'notes']  # Include all necessary fields
        widgets = {
            'device_type': forms.Select(attrs={'class': 'form-control'}),
            'user': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
        labels = {
            'device_type': 'Device Type',
            'user': 'Assign to User',
            'status': 'Status',
            'notes': 'Additional Notes',
        }