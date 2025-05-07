from django.db import models
from core.models.base import TimeStampedModel

class Clerks(models.Model):
    clerk_id = models.BigAutoField(primary_key=True)
    employee = models.ForeignKey('Employees', models.DO_NOTHING, blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'clerks'
