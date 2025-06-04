from django.db import models
from core.models.base import TimeStampedModel

class CartItems(models.Model):
    cart_item_id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey('Carts', on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=15, decimal_places=2)
    class Meta:
        managed = False
        db_table = 'cart_items'