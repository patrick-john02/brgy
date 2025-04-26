from django.db import models
from django.conf import settings  # Using CustomUser instead of default User

# Emergency Contact Information Model
class EmergencyContact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.relationship}"

    class Meta:
        verbose_name = "Emergency Contact"
        verbose_name_plural = "Emergency Contacts"

# Health Monitoring and Alerts Model
class HealthIssue(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_issues')
    health_condition = models.CharField(max_length=255)
    reported_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Reported', 'Reported'), ('Resolved', 'Resolved')], default='Reported')
    alert_level = models.CharField(max_length=20, choices=[('Low', 'Low'), ('Medium', 'Medium'), ('High', 'High')], default='Low')
    notes = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.health_condition} - {self.status}"

    class Meta:
        verbose_name = "Health Issue"
        verbose_name_plural = "Health Issues"

# Health Alerts Subscription Model
class HealthAlertSubscription(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_alert_subscriptions')
    subscribed_to = models.CharField(max_length=255)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} subscribed to {self.subscribed_to}"

    class Meta:
        verbose_name = "Health Alert Subscription"
        verbose_name_plural = "Health Alert Subscriptions"

# Medical Assistance Request Model
class MedicalAssistanceRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='medical_assistance_requests')
    request_type = models.CharField(max_length=50, choices=[('Ambulance', 'Ambulance'), ('Medical Help', 'Medical Help'), ('Other', 'Other')])
    location = models.CharField(max_length=255)
    request_description = models.TextField()
    request_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('In Progress', 'In Progress'), ('Completed', 'Completed')], default='Pending')
    responded_by = models.CharField(max_length=255, null=True, blank=True)
    response_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.request_type} request by {self.user.username} - {self.status}"

    class Meta:
        verbose_name = "Medical Assistance Request"
        verbose_name_plural = "Medical Assistance Requests"

# Health Service Providers Model
class HealthServiceProvider(models.Model):
    name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=15)
    address = models.CharField(max_length=255, null=True, blank=True)
    service_type = models.CharField(max_length=50, choices=[
        ('Hospital', 'Hospital'),
        ('Ambulance', 'Ambulance'),
        ('Clinic', 'Clinic'),
        ('Pharmacy', 'Pharmacy'),
        ('Other', 'Other')
    ])

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Health Service Provider"
        verbose_name_plural = "Health Service Providers"

# Health Service Feedback Model
class HealthServiceFeedback(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='health_service_feedbacks')
    service_provider = models.ForeignKey(HealthServiceProvider, on_delete=models.CASCADE)
    feedback = models.TextField()
    rating = models.IntegerField(choices=[
        (1, 'Poor'), (2, 'Fair'), (3, 'Good'), (4, 'Very Good'), (5, 'Excellent')
    ])
    date_submitted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username} on {self.service_provider.name}"

    class Meta:
        verbose_name = "Health Service Feedback"
        verbose_name_plural = "Health Service Feedbacks"
