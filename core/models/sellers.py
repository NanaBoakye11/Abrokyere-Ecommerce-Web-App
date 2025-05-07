from django.db import models

class Sellers(models.Model):
    seller_id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(unique=True, max_length=100)
    phone = models.CharField(unique=True, max_length=200)
    password = models.CharField(max_length=255)
    sex = models.TextField(blank=True, null=True)  # This field type is a guess.
    seller_add = models.ForeignKey('SellersAddresses', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sellers'