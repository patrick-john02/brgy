from django.db import models
from django.conf import settings  # Use CustomUser safely

# 1. Skills Development Programs
class SkillsDevelopmentProgram(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255, blank=True, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    mode = models.CharField(
        max_length=50,
        choices=[('online', 'Online'), ('in_person', 'In-Person')],
        default='in_person'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='skills_programs'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Skills Development Program"
        verbose_name_plural = "Skills Development Programs"


class ProgramRegistration(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='program_registrations'
    )
    program = models.ForeignKey(
        SkillsDevelopmentProgram,
        on_delete=models.CASCADE,
        related_name='registrations'
    )
    registered_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.program.title}"

    class Meta:
        unique_together = ('user', 'program')
        verbose_name = "Program Registration"
        verbose_name_plural = "Program Registrations"


# 2. Child and Family Welfare Programs
class FamilyWelfareProgram(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    target_audience = models.CharField(
        max_length=255,
        help_text="e.g., Children under 10, Parents, Families, etc."
    )
    date = models.DateField()
    location = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100, blank=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='family_programs'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Family Welfare Program"
        verbose_name_plural = "Family Welfare Programs"
