from django.db import models
from core.models.base import TimeStampedModel

class CustomerAddresses(models.Model):
    address_id = models.BigAutoField(primary_key=True)
    street_address = models.CharField(max_length=250, blank=True, null=True)
    city = models.CharField(max_length=250, blank=True, null=True)
    state = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=250, blank=True, null=True)
    postal_code = models.CharField(max_length=250, blank=True, null=True)
    # created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(blank=True, null=True)
    customer_id = models.ForeignKey('Customers', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer_addresses'