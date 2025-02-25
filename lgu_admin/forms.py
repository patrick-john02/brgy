from django import forms
from residents.models import Resident
from core.models import CustomUser, BarangayOfficial

#adding resident profile and information
class ResidentForm(forms.ModelForm):
    
    class Meta:
        model = Resident
        fields = [
            'first_name', 'middle_name', 'last_name', 'suffix', 
            'gender', 'birth_date', 'place_of_birth', 'nationality',
            'civil_status', 'address', 'barangay_zone', 'contact_number',
            'household', 'voter_status', 'id_number'
        ]

# for adding employee account 
class EmployeeAccountForm(forms.ModelForm):
    """Form for creating employee accounts."""

    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    position = forms.ChoiceField(choices=BarangayOfficial.POSITION_CHOICES, required=False)

    class Meta:
        model = CustomUser
        fields = ["username", "first_name", "last_name", "email", "position"]

    def clean_password2(self):
        """Ensure passwords match."""
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords do not match!")
        return password2

    def save(self, commit=True):
        """Save the user as an employee."""
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.user_type = "employee"  # Ensure user is an employee
        if commit:
            user.save()
        return user
