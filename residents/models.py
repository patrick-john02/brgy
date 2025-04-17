from django.db import models
from django.conf import settings

class Household(models.Model):
    household_number = models.CharField(max_length=50, unique=True, db_index=True)
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
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.address}"

class ResidentProfile(models.Model):
    """Extended profile details for a resident."""
    
    resident = models.OneToOneField(
        Resident, on_delete=models.CASCADE, related_name="profile"
    )
    profile_picture = models.ImageField(
        upload_to="resident_profiles/", blank=True, null=True, default="resident_profiles/default.jpg"
    )  # Uses 'resident_profiles/default.jpg' when no profile picture is uploaded

    # New field for government ID upload
    government_id = models.ImageField(
        upload_to="resident_ids/", blank=True, null=True, help_text="Upload a valid government-issued ID."
    )

    is_head_of_family = models.BooleanField(default=False)
    is_pwd = models.BooleanField(default=False)
    is_senior_citizen = models.BooleanField(default=False)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    

    date_registered = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.resident.first_name} {self.resident.last_name} - Profile"

#certifications jobseekers
class JobseekerCertificationRequest(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,  
        on_delete=models.CASCADE,
        related_name="jobseeker_requests"
    )
    purok = models.CharField(max_length=50)  
    years_of_residency = models.PositiveIntegerField()  
    months_of_residency = models.PositiveIntegerField(default=0)  
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    date_requested = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)  
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.status}"

#certification of Certificate of Guardianship
class CertificateOfGuardianshipRequest(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="guardianship_requests"
    )
    guardian_name = models.CharField(max_length=100)
    birthday = models.DateField()
    place_of_birth = models.CharField(max_length=100)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    date_requested = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.status}"

#Certificate of good moral 
class CertificateOfGoodMoralCharacterRequest(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="good_moral_requests"
    )
    purpose = models.CharField(max_length=200, default="Barangay Community Check")
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    date_requested = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.status}"

#Business Certificate 
class BarangayBusinessCertificateRequest(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="business_certificate_requests"
    )
    line_of_business = models.CharField(max_length=100)
    res_cert_no = models.CharField(max_length=50, blank=True, null=True) 
    date_issued = models.DateField(null=True, blank=True)
    place_of_issue = models.CharField(max_length=100, blank=True, null=True)
    or_no = models.CharField(max_length=50, blank=True, null=True)  
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    date_requested = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.line_of_business} - {self.status}"

#barangay clearance request
class BarangayClearanceRequest(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="barangay_clearance_requests"
    )
    reason_for_request = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ],
        default='Pending'
    )
    date_requested = models.DateTimeField(auto_now_add=True)
    date_approved = models.DateTimeField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.status}"
    

# Certification Model
class CertificationRequest(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="certification_requests"
    )
    sex = models.CharField(max_length=10)
    age = models.PositiveIntegerField()
    color = models.CharField(max_length=50)
    brand_owner = models.CharField(max_length=100)
    brand_municipality = models.CharField(max_length=100)
    item_sold_to = models.CharField(max_length=100)
    sold_amount = models.DecimalField(max_digits=10, decimal_places=2)
    certification_purpose = models.TextField(blank=True, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_issued = models.DateField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.status}"
    
class CertificateOfResidency(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="residency_certificates"
    )
    age = models.PositiveIntegerField()
    civil_status = models.CharField(
        max_length=20,
        choices=[('Single', 'Single'), ('Married', 'Married'), ('Widow', 'Widow')]
    )
    date_requested = models.DateTimeField(auto_now_add=True)
    date_issued = models.DateField(null=True, blank=True)
    purpose = models.TextField(blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    date_approved = models.DateField(null=True, blank=True)
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.status}"
    
    
    
class OneAndSamePersonCertification(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="one_and_same_certifications"
    )
    name_one = models.CharField(max_length=100)
    name_two = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    sex = models.CharField(
        max_length=10,
        choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Ms.', 'Ms.')],
        default='Mr.'
    )
    purpose = models.TextField(blank=True, null=True)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_issued = models.DateField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    date_approved = models.DateField(null=True, blank=True)
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.status}"
    
    

class CertificateOfUnemployment(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="unemployment_certifications"
    )
    full_name = models.CharField(max_length=100)
    sex = models.CharField(
        max_length=10,
        choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Ms.', 'Ms.')],
        default='Mr.'
    )
    civil_status = models.CharField(
        max_length=10,
        choices=[('Single', 'Single'), ('Married', 'Married'), ('Widow', 'Widow')],
        default='Single'
    )
    purok = models.CharField(max_length=50)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_issued = models.DateField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    date_approved = models.DateField(null=True, blank=True)
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.status}"
    

class CertificateOfIndigency(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="indigency_certifications"
    )
    full_name = models.CharField(max_length=100)
    sex = models.CharField(
        max_length=10,
        choices=[('Mr.', 'Mr.'), ('Mrs.', 'Mrs.'), ('Ms.', 'Ms.')],
        default='Mr.'
    )
    purok = models.CharField(max_length=50)
    date_requested = models.DateTimeField(auto_now_add=True)
    date_issued = models.DateField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    date_approved = models.DateField(null=True, blank=True)
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.resident.get_full_name()} - {self.status}"



class CertificateOfAppearance(models.Model):
    resident = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="appearance_certifications"
    )
    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    office_agency = models.CharField(max_length=100)
    purpose = models.TextField()
    date_of_appearance = models.DateField()
    date_requested = models.DateTimeField(auto_now_add=True)
    date_issued = models.DateField(null=True, blank=True)
    approved_by = models.CharField(max_length=100, blank=True, null=True)
    date_approved = models.DateField(null=True, blank=True)
    barangay_official_witness = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(
        max_length=20,
        choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')],
        default='Pending'
    )

    def __str__(self):
        return f"{self.full_name} - {self.date_of_appearance}"
    