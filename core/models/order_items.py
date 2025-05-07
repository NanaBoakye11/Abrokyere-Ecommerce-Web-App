from django.db import models
from core.models.base import TimeStampedModel

class OrderItems(models.Model):
    order_item_id = models.BigAutoField(primary_key=True)
    order = models.ForeignKey('Orders', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'order_items'