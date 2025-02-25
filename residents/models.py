from django.db import models

class Household(models.Model):
    household_number = models.CharField(max_length=50, unique=True)
    address = models.TextField()

    def __str__(self):
        return f"Household {self.household_number} - {self.address}"


class Resident(models.Model):
    """Resident model with essential details."""
    
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    CIVIL_STATUS_CHOICES = [
        ('single', 'Single'), ('married', 'Married'), ('widowed', 'Widowed'),
        ('divorced', 'Divorced'), ('separated', 'Separated')
    ]
    EMPLOYMENT_STATUS_CHOICES = [
        ('employed', 'Employed'), ('unemployed', 'Unemployed'),
        ('student', 'Student'), ('retired', 'Retired')
    ]

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100)
    suffix = models.CharField(max_length=10, blank=True, null=True)
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField(db_index=True)
    place_of_birth = models.CharField(max_length=255)
    nationality = models.CharField(max_length=50, default="Filipino")
    
    civil_status = models.CharField(max_length=10, choices=CIVIL_STATUS_CHOICES)
    address = models.TextField()
    barangay_zone = models.CharField(max_length=50, blank=True, null=True)
    contact_number = models.CharField(max_length=15)
    
    household = models.ForeignKey(Household, on_delete=models.SET_NULL, null=True, related_name="members")
    voter_status = models.BooleanField(default=False)
    id_number = models.CharField(max_length=30, unique=True, db_index=True)
    
    date_registered = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.address}"


class ResidentProfile(models.Model):
    
    resident = models.OneToOneField(
        Resident, on_delete=models.CASCADE, related_name="resident_profile"
    )
    is_head_of_family = models.BooleanField(default=False)
    is_pwd = models.BooleanField(default=False)
    is_senior_citizen = models.BooleanField(default=False)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    
    voter_status = models.BooleanField(default=False)
    date_registered = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)  

    has_requested_account = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.resident.first_name} {self.resident.last_name} - Profile"