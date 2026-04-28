from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import LeaveRequest

class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username']

class LeaveRequestForm(forms.ModelForm):
    class Meta:
        model = LeaveRequest
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

from .models import LeaveRequest, StudentProfile

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['readonly'] = True

class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['college_name', 'department', 'registration_number']


