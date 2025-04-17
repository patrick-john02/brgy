from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

def user_upload_path(instance, filename):
    return f'profile_pictures/{instance.username}/{filename}'

class CustomUser(AbstractUser):

    USER_TYPES = [
        ('admin', 'Admin'),
        ('employee', 'Employee'),
        ('resident', 'Resident'),
    ]

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True, null=True)

    user_type = models.CharField(max_length=15, choices=USER_TYPES)
    profile_picture = models.ImageField(
        upload_to=user_upload_path,
        default='profile_pictures/default.png',
        blank=True,
        null=True
    )
    
    government_id = models.ImageField(upload_to="resident_ids/", blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    
    is_deleted = models.BooleanField(default=False) 

    groups = models.ManyToManyField(Group, related_name="customuser_set", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions_set", blank=True)

    class Meta:
        permissions = [
            ("can_manage_barangay", "Can manage barangay operations"),
            ("can_view_reports", "Can view barangay reports"),
            ("can_request_documents", "Can request barangay documents"),
        ]

    def save(self, *args, **kwargs):
        if self.is_deleted:
            self.is_active = False  
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_deleted = True
        self.is_active = False  # Disable login
        self.save()

    def restore(self):
        self.is_deleted = False
        self.is_active = True
        self.save()
    
    def has_government_id(self):
        return bool(self.government_id and hasattr(self.government_id, 'url'))

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


        
class Service(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='services/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='projects/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class BarangayOfficial(models.Model):
    
    POSITION_CHOICES = [
        # Barangay Officials
        ('punong_barangay', 'Punong Barangay'),
        ('kagawad', 'Kagawad'),
        ('secretary', 'Barangay Secretary'),
        ('treasurer', 'Barangay Treasurer'),
        ('sk_chairman', 'SK Chairman'),
        
        ('drrmh_manager', 'DRRMH Manager'),
        ('asst_drrmh_manager', 'Asst. DRRMH Manager'),
        ('public_health_cluster', 'Public Health Cluster'),
        ('sexual_reproductive_health', 'Sexual and Reproductive Health'),
        ('nutrition_emergencies', 'Nutrition in Emergencies'),
        ('water_sanitation_hygiene', 'Water and Sanitation Hygiene'),
        ('mental_health_psychosocial', 'Mental Health and Psychosocial Support'),
        ('epidemiology_surveillance', 'Epidemiology and Surveillance'),
        ('risk_communication_promotion', 'Risk Communication and Health Promotion'),
        ('logistics', 'Logistics'),
        ('risk_transportation_ancillary', 'Risk Transportation and Ancillary'),
    ]

    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE,
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
        return f"{self.user.get_full_name()} - {self.get_position_display()}" if self.user else self.get_position_display()