from django import forms
from .models import SocialWelfareApplication

class SocialWelfareApplicationForm(forms.ModelForm):
    class Meta:
        model = SocialWelfareApplication
        fields = ['service_type', 'purpose', 'supporting_documents']

        widgets = {
            'service_type': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'purpose': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter application details', 'required': True}),
            'supporting_documents': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }
