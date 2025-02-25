from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from residents.models import Resident, ResidentProfile

class CustomUser(AbstractUser):
    """Custom user model with role-based permissions."""
    
    USER_TYPES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('resident', 'Resident'),
    ]
    
    user_type = models.CharField(max_length=15, choices=USER_TYPES)

    # Prevent resident deletion if they have an account
    resident_profile = models.OneToOneField(
        Resident,
        on_delete=models.PROTECT,  
        null=True,
        blank=True,
        related_name="user_account"
    )

    is_deleted = models.BooleanField(default=False)  # Soft delete flag

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

    class Meta:
        permissions = [
            ("can_manage_barangay", "Can manage barangay operations"),
            ("can_view_reports", "Can view barangay reports"),
            ("can_request_documents", "Can request barangay documents"),
        ]

    def save(self, *args, **kwargs):
        """Ensure resident_profile is valid before saving."""
        if self.resident_profile:
            if not Resident.objects.filter(id=self.resident_profile_id).exists():
                self.resident_profile = None  
            elif not ResidentProfile.objects.filter(resident=self.resident_profile).exists():
                self.resident_profile = None
            else:
                resident_profile = ResidentProfile.objects.get(resident=self.resident_profile)
                if not resident_profile.has_requested_account:
                    self.resident_profile = None  

        # Ensure disabled users cannot log in
        if self.is_deleted:
            self.is_active = False  

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Soft delete the user instead of permanently removing it."""
        self.is_deleted = True
        self.is_active = False  # Disable login
        self.save()

    def restore(self):
        """Restore a soft-deleted user."""
        self.is_deleted = False
        self.is_active = True
        self.save()



class Service(models.Model):
    """Barangay service model."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    """Barangay project model."""
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BarangayOfficial(models.Model):
    """Barangay officials with their respective positions."""
    
    POSITION_CHOICES = [
        ('captain', 'Barangay Captain'),
        ('kagawad', 'Kagawad'),
        ('secretary', 'Barangay Secretary'),
        ('treasurer', 'Barangay Treasurer'),
        ('sk_chairman', 'SK Chairman'),
    ]

    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,  # If employee account is deleted, remove Barangay Official
        related_name="barangay_official",
        null=True,
        blank=True
    )
    
    position = models.CharField(max_length=50, choices=POSITION_CHOICES)
    profile_image = models.ImageField(upload_to='officials/profiles/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.position}" if self.user else self.position
