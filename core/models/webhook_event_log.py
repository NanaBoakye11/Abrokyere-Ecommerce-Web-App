import uuid
from django.db import models
from django.utils import timezone

class WebhookEventLog(models.Model):
    """
    Stores processed Stripe event IDs to ensure idempotency.
    This table is managed by Django and safe to migrate.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    event_id = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "webhook_event_log"
        managed = True

    def __str__(self):
        return self.event_id
