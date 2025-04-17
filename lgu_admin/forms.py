from django import forms
from residents.models import Resident, ResidentProfile, Household
from core.models import CustomUser, BarangayOfficial
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
import secrets
import random
import string


#adding resident profile and information
class ResidentForm(forms.ModelForm):
    BARANGAY_ZONES = [
        ("Zone 1", "Zone 1"),
        ("Zone 2", "Zone 2"),
        ("Zone 3", "Zone 3"),
        ("Zone 4", "Zone 4"),
        ("Zone 5", "Zone 5"),
        ("Zone 6", "Zone 6"),
        ("Zone 7", "Zone 7"),
    ]

    barangay_zone = forms.ChoiceField(
        choices=BARANGAY_ZONES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )

    class Meta:
        model = Resident
        fields = ['first_name', 'middle_name', 'last_name', 'suffix', 'birth_date', 
                  'place_of_birth', 'gender', 'nationality', 'civil_status', 'address',
                  'barangay_zone', 'contact_number', 'voter_status', 'id_number']


class ResidentProfileForm(forms.ModelForm):
    class Meta:
        model = ResidentProfile
        fields = [
            "profile_picture", "government_id", "is_head_of_family",
            "is_pwd", "is_senior_citizen", "occupation"
        ]



# for adding user accounts 
class UserAccountForm(forms.ModelForm):
    
    profile_picture = forms.ImageField(required=False, label="Profile Picture")

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type', 'profile_picture']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        
        if 'profile_picture' in self.cleaned_data and self.cleaned_data['profile_picture']:
            user.profile_picture = self.cleaned_data['profile_picture']

        random_password = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(10))
        user.set_password(random_password) 

        if commit:
            user.save()
            subject = "Your Barangay System Account Credentials"
            message = (
                f"Hello {user.first_name} {user.last_name},\n\n"
                f"Your account has been created.\n"
                f"Username: {user.username}\n"
                f"Password: {random_password}\n"
                f"User Type: {user.get_user_type_display()}\n\n"
                f"Please change your password after logging in.\n\n"
                f"Best Regards,\nBarangay System Admin"
            )
            send_mail(subject, message, 'your_email@example.com', [user.email])

        return user

#creation of residents account on admin side
class ResidentAccountForm(forms.ModelForm):
    
    profile_picture = forms.ImageField(required=False)
    government_id = forms.ImageField(required=False)
    contact_number = forms.CharField(max_length=15, required=True)
    barangay_zone = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=255, required=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'middle_name', 'last_name', 'suffix', 
                  'email', 'profile_picture', 'government_id', 'contact_number', 'barangay_zone', 'address']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'resident'

        random_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        user.set_password(random_password)

        if commit:
            user.save()

        user.raw_password = random_password  
        return user


#edit form for user accounts
class EditUserAccountForm(UserChangeForm):
    USER_TYPE_CHOICES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('resident', 'Resident'),
    ]

    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        required=True,
        label="User Type",
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    profile_picture = forms.ImageField(
        required=False,
        label="Profile Picture",
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'user_type', 'profile_picture']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_id = self.instance.pk

        if CustomUser.objects.exclude(pk=user_id).filter(username=username).exists():
            raise forms.ValidationError("A user with that username already exists.")
        
        return username

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = [
            'first_name',
            'middle_name',
            'last_name',
            'suffix',
            'profile_picture',
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'suffix': forms.TextInput(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_profile_picture(self):
        picture = self.cleaned_data.get('profile_picture')
        if picture:
            if picture.size > 5 * 1024 * 1024:  # 5MB limit
                raise forms.ValidationError("Profile picture file size must be under 5MB.")
            if not picture.content_type.startswith('image/'):
                raise forms.ValidationError("Uploaded file must be an image.")
        return picture
