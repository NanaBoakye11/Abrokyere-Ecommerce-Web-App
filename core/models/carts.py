from django.db import models
from core.models.base import TimeStampedModel

class Carts(models.Model):
    cart_id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey('Customers', models.DO_NOTHING)
    total_qty = models.IntegerField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carts'