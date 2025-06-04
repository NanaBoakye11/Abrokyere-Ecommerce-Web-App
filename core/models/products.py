from django.db import models

class Products(models.Model):
    product_id = models.BigAutoField(primary_key=True)
    category = models.ForeignKey('Categories', models.DO_NOTHING, blank=True, null=True)
    product_name = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=15, decimal_places=2)
    description = models.CharField(max_length=500, blank=True, null=True)
    prod_reviews = models.CharField(max_length=600, blank=True, null=True)
    color = models.ForeignKey('Colors', models.DO_NOTHING)
    featured = models.BooleanField(default=False)
    # quantity = models.IntegerField(default=0)
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    rating_count = models.IntegerField(default=0)

    class Meta:
        managed = False
        db_table = 'products'


class ProductImages(models.Model):
    image_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey(
        'Products', 
        on_delete=models.CASCADE,
        related_name='product_images'
    )
    image_url = models.CharField(max_length=500)
    is_main = models.BooleanField(default=False)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_images'

