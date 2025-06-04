from django.db import models

class Inventory(models.Model):
    inventory_id = models.BigAutoField(primary_key=True)
    store = models.ForeignKey('Stores', models.DO_NOTHING)
    product = models.ForeignKey('Products', models.DO_NOTHING)
    # color = models.ForeignKey('Colors', models.DO_NOTHING)
    quantity = models.IntegerField(blank=True, null=True)
    # category = models.ForeignKey('Categories', models.DO_NOTHING, blank=True, null=True)
    location = models.CharField(max_length=50, blank=True, null=True)
    restock_threshold = models.IntegerField(blank=True, null=True)



    class Meta:
        managed = False
        db_table = 'inventory'