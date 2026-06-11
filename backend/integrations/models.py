from django.db import models
from django.contrib.auth.models import User


class Integration(models.Model):

    PROVIDER_CHOICES = [
        ('quickbooks', 'QuickBooks'),
        ('salesforce', 'Salesforce'),
        ('hubspot', 'HubSpot'),
        ('slack', 'Slack'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='integrations'
    )

    provider = models.CharField(
        max_length=50,
        choices=PROVIDER_CHOICES
    )

    access_token = models.TextField()

    refresh_token = models.TextField(
        blank=True,
        null=True
    )

    expires_at = models.DateTimeField(
        blank=True,
        null=True
    )

    realm_id = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.provider}"