from django import forms
from django.contrib.auth.forms import UserCreationForm
from lgu_admin.models import BarangayReport, CustomUser


class CustomUserRegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    middle_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=True)
    suffix = forms.CharField(max_length=10, required=False)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(widget=forms.PasswordInput, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'middle_name', 'last_name', 'suffix', 'username', 'email', 'password1', 'password2']

REPORT_TYPES = [
    ("", "Select Report Type"),
    ("complaint", "Complaint"),
    ("incident", "Incident"),
    ("accident", "Accident"),
]

class BarangayReportForm(forms.ModelForm):

    report_type = forms.ChoiceField(
        choices=REPORT_TYPES,
        widget=forms.Select(attrs={"class": "form-control", "required": True})
    )

    class Meta:
        model = BarangayReport
        fields = ["name", "email", "report_type", "description", "image"]
