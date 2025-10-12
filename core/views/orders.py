# core/views/orders.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.models import Orders, OrderItems, OrderSessionMap


def _order_to_dict(order):
    """
    Convert an order into a dict with items included.
    """
    items_qs = (
        OrderItems.objects.select_related("product")
        .filter(order=order)
        .order_by("order_item_id")
    )
    items = [
        {
            "order_item_id": oi.order_item_id,
            "product_id": oi.product_id,
            "product_name": getattr(oi.product, "product_name", None),
            "quantity": oi.quantity,
            "price": float(oi.price),  # unit price
        }
        for oi in items_qs
    ]

    return {
        "order_id": order.order_id,
        "order_date": order.order_date,
        "status": order.status,
        "total_amount": float(order.total_amount or 0),
        "items": items,
    }


class RecentOrdersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Return up to the 10 most recent orders for the authenticated customer.
        """
        customer = request.user.customer
        orders = (
            Orders.objects.filter(customer=customer)
            .order_by("-order_date")[:10]
        )
        data = [_order_to_dict(o) for o in orders]
        return Response({"orders": data}, status=200)


class OrderBySessionView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, session_id: str):
        """
        Look up an order created by the webhook using the Stripe Checkout Session ID.
        Relies on OrderSessionMap (session_id -> order).
        """
        try:
            link = OrderSessionMap.objects.select_related("order").get(session_id=session_id)
        except OrderSessionMap.DoesNotExist:
            return Response(
                {"detail": "Order not found for this session."},
                status=404,
            )

        return Response(_order_to_dict(link.order), status=200)


# # core/views/orders.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.db.models import Prefetch
# from core.models import Orders, OrderItems, Products, Customers, OrderSessionMap

# # # core/views/orders.py

# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework.permissions import IsAuthenticated
# # from rest_framework_simplejwt.authentication import JWTAuthentication

# # from core.models import Orders, OrderItems

# def _order_to_dict(order):
#     # Load items and include product name if available
#     items_qs = (
#         OrderItems.objects.select_related("product")
#         .filter(order=order)
#         .order_by("order_item_id")
#     )
#     items = [
#         {
#             "order_item_id": oi.order_item_id,
#             "product_id": oi.product_id,
#             "product_name": getattr(oi.product, "product_name", None),
#             "quantity": oi.quantity,
#             "price": float(oi.price),
#         }
#         for oi in items_qs
#     ]
#     return {
#         "order_id": order.order_id,
#         "order_date": order.order_date,
#         "status": order.status,
#         "total_amount": float(order.total_amount or 0),
#         # Optional fields if you have them in your DB:
#         "stripe_session_id": getattr(order, "stripe_session_id", None),
#         "payment_intent_id": getattr(order, "payment_intent_id", None),
#         "items": items,
#     }


# class RecentOrdersView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         customer = request.user.customer
#         orders = (
#             Orders.objects.filter(customer=customer)
#             .order_by("-order_date")[:10]
#         )

#         data = [_order_to_dict(o) for o in orders]
#         return Response({"orders": data}, status=200)


# class OrderBySessionView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, session_id: str):
#         """
#         Look up an order created by the webhook using the Stripe Checkout Session ID.
#         """
#         try:
#             order = Orders.objects.get(stripe_session_id=session_id)
#         except Orders.DoesNotExist:
#             return Response(
#                 {"detail": "Order not found for this session_id.", "session_id": session_id},
#                 status=404,
#             )

#         return Response(_order_to_dict(order), status=200)



# core/views/orders.py
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
# from django.utils import timezone

# from core.models import Orders, OrderItems
# from core.models.stripe_sessions import StripeCheckoutSession
# from core.serializers.orders import OrderSerializer

# class RecentOrdersView(APIView):
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         customer = request.user.customer
#         qs = Orders.objects.filter(customer=customer).order_by('-order_date')[:10]
#         data = OrderSerializer(qs, many=True).data
#         return Response({'orders': data})

# class OrderBySessionView(APIView):
#     """
#     Lookup a just-finished order by stripe session id.
#     Returns 404 if webhook hasn't created it yet (frontend will retry briefly).
#     """
#     authentication_classes = [JWTAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, session_id: str):
#         try:
#             mapping = StripeCheckoutSession.objects.select_related('order').get(stripe_session_id=session_id)
#         except StripeCheckoutSession.DoesNotExist:
#             return Response({'detail': 'Order for session not found (yet).'}, status=404)

#         data = OrderSerializer(mapping.order).data
#         return Response(data)
