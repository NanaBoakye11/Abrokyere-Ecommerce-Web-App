from django.db import models
from core.models.base import TimeStampedModel

class Deliveries(models.Model):
    delivery_id = models.BigAutoField(primary_key=True)
    delivery_address = models.CharField(max_length=255)
    driver = models.ForeignKey('Drivers', models.DO_NOTHING)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    delivery_method = models.TextField()  # This field type is a guess.
    delivery_status = models.TextField(blank=True, null=True)  # This field type is a guess.
    scheduled_delievery_time = models.DateTimeField(blank=True, null=True)
    actual_dt = models.DateTimeField(blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    instructions = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'deliveries'