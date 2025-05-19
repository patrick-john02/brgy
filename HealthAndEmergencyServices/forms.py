from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
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



# CustomUser form for creating or updating users
class CustomUserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'middle_name', 'last_name', 'suffix', 'user_type', 'profile_picture', 'government_id', 'is_verified']
        widgets = {
            'profile_picture': forms.ClearableFileInput(),  # Remove 'multiple' here
            'government_id': forms.ClearableFileInput(),  # Remove 'multiple' here
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if get_user_model().objects.filter(username=username).exists():
            raise ValidationError("Username is already taken. Please choose another.")
        return username

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture and profile_picture.size > 5 * 1024 * 1024:  # 5MB limit for profile picture
            raise ValidationError("Profile picture size should not exceed 5MB.")
        return profile_picture

    def clean_government_id(self):
        government_id = self.cleaned_data.get('government_id')
        if government_id and government_id.size > 5 * 1024 * 1024:  # 5MB limit for government ID
            raise ValidationError("Government ID size should not exceed 5MB.")
        return government_id

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user
    

#admin 
class EmergencyContactForm(forms.ModelForm):
    class Meta:
        model = EmergencyContact
        fields = ['name', 'relationship', 'phone_number', 'address']