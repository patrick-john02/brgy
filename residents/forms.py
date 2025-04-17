from django import forms
from .models import (
    JobseekerCertificationRequest, 
    CertificateOfGuardianshipRequest,
    CertificateOfGoodMoralCharacterRequest,
    BarangayBusinessCertificateRequest,
    BarangayClearanceRequest,
    CertificationRequest,
    CertificateOfResidency,
    OneAndSamePersonCertification,
    CertificateOfUnemployment,
    CertificateOfIndigency,
    CertificateOfAppearance,
)

class JobseekerCertificationForm(forms.ModelForm):
    class Meta:
        model = JobseekerCertificationRequest
        fields = ['purok', 'years_of_residency', 'months_of_residency']
        widgets = {
            'purok': forms.TextInput(attrs={'class': 'form-control'}),
            'years_of_residency': forms.NumberInput(attrs={'class': 'form-control'}),
            'months_of_residency': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CertificateOfGuardianshipForm(forms.ModelForm):
    class Meta:
        model = CertificateOfGuardianshipRequest
        fields = ['guardian_name', 'birthday', 'place_of_birth']
        widgets = {
            'guardian_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birthday': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'place_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CertificateOfGoodMoralCharacterForm(forms.ModelForm):
    class Meta:
        model = CertificateOfGoodMoralCharacterRequest
        fields = ['purpose']
        widgets = {
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BarangayBusinessCertificateForm(forms.ModelForm):
    class Meta:
        model = BarangayBusinessCertificateRequest
        fields = [
            'line_of_business', 
            'res_cert_no', 
            'date_issued', 
            'place_of_issue', 
            'or_no'
        ]
        widgets = {
            'line_of_business': forms.TextInput(attrs={'class': 'form-control'}),
            'res_cert_no': forms.TextInput(attrs={'class': 'form-control'}),
            'date_issued': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'place_of_issue': forms.TextInput(attrs={'class': 'form-control'}),
            'or_no': forms.TextInput(attrs={'class': 'form-control'}),
        }

class BarangayClearanceForm(forms.ModelForm):
    class Meta:
        model = BarangayClearanceRequest
        fields = ['reason_for_request']
        widgets = {
            'reason_for_request': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CertificationForm(forms.ModelForm):
    class Meta:
        model = CertificationRequest
        fields = ['sex', 'age', 'color', 'brand_owner', 'brand_municipality', 'item_sold_to', 'sold_amount', 'certification_purpose']
        widgets = {
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'color': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_owner': forms.TextInput(attrs={'class': 'form-control'}),
            'brand_municipality': forms.TextInput(attrs={'class': 'form-control'}),
            'item_sold_to': forms.TextInput(attrs={'class': 'form-control'}),
            'sold_amount': forms.NumberInput(attrs={'class': 'form-control'}),
            'certification_purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CertificateOfResidencyForm(forms.ModelForm):
    class Meta:
        model = CertificateOfResidency
        fields = ['age', 'civil_status', 'purpose']
        widgets = {
            'age': forms.NumberInput(attrs={'class': 'form-control'}),
            'civil_status': forms.Select(attrs={'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class OneAndSamePersonCertificationForm(forms.ModelForm):
    class Meta:
        model = OneAndSamePersonCertification
        fields = ['name_one', 'name_two', 'full_name', 'sex', 'purpose']
        widgets = {
            'name_one': forms.TextInput(attrs={'class': 'form-control'}),
            'name_two': forms.TextInput(attrs={'class': 'form-control'}),
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class CertificateOfUnemploymentForm(forms.ModelForm):
    class Meta:
        model = CertificateOfUnemployment
        fields = ['full_name', 'sex', 'civil_status', 'purok']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'civil_status': forms.Select(attrs={'class': 'form-control'}),
            'purok': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CertificateOfIndigencyForm(forms.ModelForm):
    class Meta:
        model = CertificateOfIndigency
        fields = ['full_name', 'sex', 'purok']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'purok': forms.TextInput(attrs={'class': 'form-control'}),
        }

class CertificateOfAppearanceForm(forms.ModelForm):
    class Meta:
        model = CertificateOfAppearance
        fields = ['full_name', 'designation', 'office_agency', 'purpose', 'date_of_appearance']
        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'designation': forms.TextInput(attrs={'class': 'form-control'}),
            'office_agency': forms.TextInput(attrs={'class': 'form-control'}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'date_of_appearance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
