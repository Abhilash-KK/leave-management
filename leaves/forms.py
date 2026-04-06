from django import forms
from .models import LeaveRequest

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['employee_name', 'leave_date', 'reason']
        widgets = {
            'leave_date': forms.DateInput(attrs={'type': 'date'}),
        }
