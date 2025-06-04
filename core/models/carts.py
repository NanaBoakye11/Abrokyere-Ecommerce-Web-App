from django.db import models
from core.models.base import TimeStampedModel

class Carts(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('checked_out', 'Checked Out'),
        ('abandoned', 'Abandoned'),
    ]
    cart_id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey('Customers', models.DO_NOTHING, db_column='customer_id', null=True, blank=True)
    total_qty = models.IntegerField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', db_index=True)

    # created_at = models.DateTimeField(blank=True, null=True)
    # updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'carts'