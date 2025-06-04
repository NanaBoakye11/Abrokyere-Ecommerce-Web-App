from django.db.models import Avg, Count
from core.models import Products

def update_product_rating(product_id):
    from core.models import ProductReviews  # to avoid circular import

    product = Products.objects.get(product_id=product_id)
    agg = product.reviews.aggregate(
        avg=Avg('rating'),
        count=Count('rating')
    )
    product.rating_average = round(agg['avg'] or 0, 2)
    product.rating_count = agg['count']
    product.save()