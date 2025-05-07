from django.db import models
from core.models.base import TimeStampedModel

class Drivers(models.Model):
    driver_id = models.BigAutoField(primary_key=True)
    employee = models.OneToOneField('Employees', models.DO_NOTHING)
    driver_license = models.CharField(unique=True, max_length=50)
    license_country = models.CharField(max_length=200)
    vehicle_type = models.TextField()  # This field type is a guess.
    plate_number = models.CharField(max_length=50, blank=True, null=True)
    num_of_deliveries = models.IntegerField(blank=True, null=True)
    profile_pic = models.CharField(max_length=255, blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drivers'