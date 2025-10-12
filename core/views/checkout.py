# core/views/checkout.py

from decimal import Decimal

import stripe
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Carts, CartItems

stripe.api_key = settings.STRIPE_SECRET_KEY


class CreateCheckoutSessionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Creates a Stripe Checkout Session for the authenticated user's active cart.
        Includes cart/customer metadata so the webhook can build an Order & clear the cart.
        """
        try:
            customer = request.user.customer
        except Exception:
            return Response({"error": "Customer profile not found."}, status=status.HTTP_400_BAD_REQUEST)

        # Get active cart
        cart = Carts.objects.filter(customer=customer, status="active").first()
        if not cart:
            return Response({"error": "No active cart."}, status=status.HTTP_400_BAD_REQUEST)

        items_qs = CartItems.objects.select_related("product").filter(cart=cart)
        if not items_qs.exists():
            return Response({"error": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

        # Build Stripe line_items
        line_items = []
        for item in items_qs:
            # Use the product's unit price; Stripe expects the *unit* amount in cents
            unit_price = Decimal(str(item.product.price))
            unit_amount_cents = int(unit_price * 100)

            # Guard against zero/negative amounts
            if unit_amount_cents <= 0:
                return Response(
                    {"error": f"Invalid unit price for {item.product.product_name}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            line_items.append({
                "price_data": {
                    "currency": "usd",
                    "unit_amount": unit_amount_cents,
                    "product_data": {
                        "name": item.product.product_name,
                    },
                },
                "quantity": item.quantity,
            })

        # Pass metadata so the webhook can resolve cart → order
        metadata = {
            "cart_id": str(cart.cart_id),
            "customer_id": str(customer.customer_id),
            "customer_email": customer.email or "",
        }

        try:
            session = stripe.checkout.Session.create(
                mode="payment",
                line_items=line_items,
                success_url="http://localhost:3000/orders/confirmation?session_id={CHECKOUT_SESSION_ID}",
                cancel_url="http://localhost:3000/orders/error",
                metadata=metadata,


                # cancel_url="http://localhost:3000/cart",
                # Optional niceties you can enable later:
                # customer_email=customer.email,        # if you want Stripe to prefill email
                # allow_promotion_codes=True,
                # billing_address_collection="auto",
            )
        except stripe.error.StripeError as e:
            # Bubble up a safe error to the client; log e.user_message/e.code if desired
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"url": session.url}, status=status.HTTP_200_OK)






# # core/views/checkout.py

# import stripe
# from django.conf import settings
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from core.models import Carts, CartItems

# stripe.api_key = settings.STRIPE_SECRET_KEY

# class CreateCheckoutSessionView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         customer = request.user.customer
#         cart = Carts.objects.get(customer=customer, status='active')
#         items = CartItems.objects.filter(cart=cart)

#         line_items = []
#         for item in items:
#             line_items.append({
#                 'price_data': {
#                     'currency': 'usd',
#                     'unit_amount': int(item.price * 100),  # in cents
#                     'product_data': {'name': item.product.product_name},
#                 },
#                 'quantity': item.quantity,
#             })

#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=line_items,
#             mode='payment',
#             success_url='http://localhost:3000/order/confirmation?session_id={CHECKOUT_SESSION_ID}',
#             cancel_url='http://localhost:3000/cart',
#         )

#         return Response({'url': checkout_session.url})
