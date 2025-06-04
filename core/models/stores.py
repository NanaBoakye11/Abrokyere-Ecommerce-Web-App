from django.db import models

class Stores(models.Model):
    store_id = models.BigAutoField(primary_key=True)
    seller = models.ForeignKey('Sellers', models.DO_NOTHING)
    store_name = models.CharField(unique=True, max_length=100)
    country = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=50, blank=True, null=True)
    store_logo = models.CharField(max_length=255, blank=True, null=True)
    payment_info = models.CharField(max_length=255, blank=True, null=True)
    website_url = models.CharField(max_length=255, blank=True, null=True)
    reviews = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'stores'
