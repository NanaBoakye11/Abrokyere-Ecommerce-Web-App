from django.db import models
from core.models.base import TimeStampedModel

class CartItems(models.Model):
    cart_item_id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey('Carts', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'cart_items'