from django.db import models



class SellersAddresses(models.Model):
    seller_add_id = models.BigAutoField(primary_key=True)
    street_address = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    country = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'sellers_addresses'