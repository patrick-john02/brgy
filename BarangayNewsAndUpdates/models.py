from django.db import models
from django.conf import settings  # Use this to reference your CustomUser

# Real-Time News and Alerts
class BarangayNews(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # reference CustomUser
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_urgent = models.BooleanField(default=False)
    category = models.CharField(
        max_length=100,
        choices=[
            ('policy', 'Policy Update'),
            ('regulation', 'Regulation'),
            ('interruption', 'Service Interruption'),
            ('event', 'Community Event'),
            ('other', 'Other')
        ],
        default='other'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Barangay News"
        verbose_name_plural = "Barangay News"


# Monthly Newsletters
class MonthlyNewsletter(models.Model):
    month = models.CharField(max_length=20)
    year = models.PositiveIntegerField()
    summary = models.TextField()
    uploaded_pdf = models.FileField(upload_to='newsletters/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # reference CustomUser
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.month} {self.year} Newsletter"

    class Meta:
        unique_together = ('month', 'year')
        verbose_name = "Monthly Newsletter"
        verbose_name_plural = "Monthly Newsletters"
