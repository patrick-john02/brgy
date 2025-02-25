from django.db import models
from core.models import CustomUser

class BarangayAdmin(models.Model):
    """Barangay Admin model extending the CustomUser."""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="barangay_admin")
    position = models.CharField(max_length=100, default="Barangay Admin")
    date_assigned = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.position}"

class BarangayReport(models.Model):
    """Reports received by the barangay administration (complaints, incidents, etc.)."""
    REPORT_TYPE_CHOICES = [
        ('complaint', 'Complaint'),
        ('incident', 'Incident'),
        ('accident', 'Accident'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField()
    report_type = models.CharField(max_length=50, choices=REPORT_TYPE_CHOICES)
    description = models.TextField()
    image = models.ImageField(upload_to='lgu_admin/reports/', null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.name} - {self.report_type} - {self.date_created}"