from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from core.models import ProductReviews
from core.services.review_services import update_product_rating

class SubmitReviewView(APIView):
    def post(self, request):
        # Extract data
        customer_id = request.data.get('customer_id')
        product_id = request.data.get('product_id')
        rating = request.data.get('rating')
        comment = request.data.get('comment', '')

        # Validation omitted for brevity
        review = ProductReviews.objects.create(
            customer_id=customer_id,
            product_id=product_id,
            rating=rating,
            comment=comment
        )

        # 🔁 Update product's avg rating & count
        update_product_rating(product_id)

        return Response({"message": "Review submitted"}, status=status.HTTP_201_CREATED)