from django import forms
from .models import (
    EmergencyContact, HealthIssue,
    MedicalAssistanceRequest, HealthServiceFeedback
)

class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'phone_number', 'address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class HealthIssueForm(forms.ModelForm):
    class Meta:
        model = HealthIssue
        fields = ['health_condition', 'status', 'alert_level', 'notes']
        widgets = {
            'health_condition': forms.TextInput(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'alert_level': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class MedicalAssistanceRequestForm(forms.ModelForm):
    class Meta:
        model = MedicalAssistanceRequest
        fields = ['request_type', 'location', 'request_description']
        widgets = {
            'request_type': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'request_description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class HealthServiceFeedbackForm(forms.ModelForm):
    class Meta:
        model = HealthServiceFeedback
        fields = ['feedback', 'rating']
        widgets = {
            'feedback': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
        }
