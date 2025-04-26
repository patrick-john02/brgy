from django.db import models
from django.conf import settings

# Optionally use choices for service types
SOCIAL_SERVICE_CHOICES = [
    ('financial_aid', 'Financial Aid'),
    ('food_assistance', 'Food Assistance'),
    ('medical_assistance', 'Medical Assistance'),
    ('livelihood', 'Livelihood Program'),
]

PWD_SENIOR_SERVICE_CHOICES = [
    ('discount_request', 'Discount Request'),
    ('mobility_assistance', 'Mobility Assistance'),
    ('gov_program', 'Government-Sponsored Program'),
]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),
    ('rejected', 'Rejected'),
]

class SocialWelfareApplication(models.Model):
    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50, choices=SOCIAL_SERVICE_CHOICES)
    purpose = models.TextField()
    supporting_documents = models.FileField(upload_to='welfare_documents/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_applied = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.get_service_type_display()}"

class PwdSeniorServiceRequest(models.Model):
    resident = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=50, choices=PWD_SENIOR_SERVICE_CHOICES)
    details = models.TextField()
    id_card_upload = models.FileField(upload_to='senior_pwd_ids/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    date_requested = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.get_service_type_display()}"
