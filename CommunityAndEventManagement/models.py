from django.db import models
from django.conf import settings  # This references your CustomUser

# 1. Community Events & Announcements
class CommunityEvent(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=255)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posted_events'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Community Event"
        verbose_name_plural = "Community Events"


# 2. Volunteering Opportunities
class VolunteeringOpportunity(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    posted_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='volunteering_posts'
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Volunteering Opportunity"
        verbose_name_plural = "Volunteering Opportunities"


class VolunteerSignup(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='volunteer_signups'
    )
    opportunity = models.ForeignKey(
        VolunteeringOpportunity,
        on_delete=models.CASCADE,
        related_name='signups'
    )
    signup_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.opportunity.title}"

    class Meta:
        unique_together = ('user', 'opportunity')
        verbose_name = "Volunteer Signup"
        verbose_name_plural = "Volunteer Signups"


# 3. Online Discussion Forums
class ForumTopic(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='forum_topics'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Forum Topic"
        verbose_name_plural = "Forum Topics"


class ForumPost(models.Model):
    topic = models.ForeignKey(
        ForumTopic,
        on_delete=models.CASCADE,
        related_name='posts'
    )
    content = models.TextField()
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='forum_posts'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post by {self.created_by} on {self.topic.title}"

    class Meta:
        verbose_name = "Forum Post"
        verbose_name_plural = "Forum Posts"
        ordering = ['created_at']
