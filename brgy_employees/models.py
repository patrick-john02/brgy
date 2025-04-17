from django.db import models
from core.models import CustomUser
from residents.models import Resident

class BarangayEmployee(models.Model):
    EMPLOYEE_ROLES = [
        ('staff', 'Staff'),
        ('health_worker', 'Health Worker'),
        ('tanod', 'Barangay Tanod'),
        ('clerk', 'Barangay Clerk'),
        ('social_worker', 'Social Worker'),
        ('environment_officer', 'Environment Officer'),
    ]

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='employee_profile')
    role = models.CharField(max_length=50, choices=EMPLOYEE_ROLES)
    date_hired = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

