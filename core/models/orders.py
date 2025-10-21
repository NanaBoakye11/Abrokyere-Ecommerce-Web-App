# core/models/orders.py


from django.db import models
from core.models.base import TimeStampedModel

class Orders(models.Model):
    order_id = models.BigAutoField(primary_key=True)
    customer = models.ForeignKey('Customers', models.DO_NOTHING)
    order_date = models.DateTimeField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    status = models.TextField(blank=True, null=True)  # This field type is a guess.

    class Meta:
        managed = False
        db_table = 'orders'