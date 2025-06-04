from django.db import models

class ProductReviews(models.Model):
    review_id = models.BigAutoField(primary_key=True)
    product = models.ForeignKey('Products', on_delete=models.CASCADE, related_name='reviews')
    customer = models.ForeignKey('Customers', on_delete=models.SET_NULL, null=True, blank=True)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'product_reviews'
        managed = False