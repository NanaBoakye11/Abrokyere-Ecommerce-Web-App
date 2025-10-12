# core/views/stripe_webhook.py
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
from decimal import Decimal
import json, stripe
from django.views.decorators.csrf import csrf_exempt
from core.models import Carts, CartItems, Customers, Orders, OrderItems
from core.models import OrderSessionMap  # new

# stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def stripe_webhook(request):
    print("📩 /api/stripe/webhook/ hit")
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', None)

    if not secret:
        print("❌ STRIPE_WEBHOOK_SECRET missing in settings")
        return HttpResponse(status=400)

    try:
        event = stripe.Webhook.construct_event(payload=payload, sig_header=sig_header, secret=secret)
    except ValueError as e:
        print(f"❌ Invalid payload: {e}")
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        print(f"❌ Signature verification failed: {e}")
        return HttpResponse(status=400)

    event_type = event.get("type")
    data_obj = event.get("data", {}).get("object", {})
    print(f"✅ Event: {event_type}")

    if event_type == "checkout.session.completed":
        from django.utils import timezone
        from core.models import Carts, CartItems, Orders, OrderItems, OrderSessionMap

        session_id = data_obj.get("id")
        payment_intent = data_obj.get("payment_intent")
        metadata = data_obj.get("metadata", {}) or {}
        cart_id = metadata.get("cart_id")
        customer_id = metadata.get("customer_id")

        print("🧾 Session:", json.dumps({
            "id": session_id,
            "payment_intent": payment_intent,
            "metadata": metadata
        }, indent=2))

        if not session_id:
            print("⚠️ No session_id on event")
            return HttpResponse(status=200)

        # Idempotency: skip if we already mapped this session
        try:
            if OrderSessionMap.objects.filter(session_id=session_id).exists():
                print(f"🔁 Session already processed ({session_id}).")
                return HttpResponse(status=200)
        except Exception as e:
            print(f"⚠️ Map check failed: {e}")

        if not cart_id or not customer_id:
            print("⚠️ Missing cart_id/customer_id metadata; cannot create order.")
            return HttpResponse(status=200)

        try:
            cart = Carts.objects.filter(cart_id=cart_id, customer_id=customer_id).first()
            if not cart:
                print(f"⚠️ No active cart for cart_id={cart_id}, customer_id={customer_id}")
                return HttpResponse(status=200)

            items = list(CartItems.objects.select_related("product").filter(cart=cart))
            if not items:
                print("⚠️ Cart empty at webhook time.")
                return HttpResponse(status=200)

            with transaction.atomic():
                total_amount = sum(Decimal(str(i.product.price)) * i.quantity for i in items)

                order = Orders.objects.create(
                    customer_id=customer_id,
                    order_date=timezone.now(),
                    total_amount=total_amount,
                    status="paid",
                )

                OrderItems.objects.bulk_create([
                    OrderItems(
                        order=order,
                        product=i.product,
                        quantity=i.quantity,
                        price=i.product.price,  # unit price
                    ) for i in items
                ])

                OrderSessionMap.objects.create(session_id=session_id, order=order)

                # Clear cart
                CartItems.objects.filter(cart=cart).delete()
                cart.total_qty = 0
                cart.total_amount = 0
                cart.status = "completed"  # or keep 'active'
                cart.save(update_fields=["total_qty", "total_amount", "status"])

                print(f"🎉 Order {order.order_id} created, mapped to session {session_id}. Cart cleared.")

        except Exception as e:
            print(f"🔥 Webhook error creating order: {e}")
            # Return 200 so Stripe doesn’t hammer retries if it’s a data issue
            return HttpResponse(status=200)

    return HttpResponse(status=200)













# @csrf_exempt
# def stripe_webhook(request):
#     raw = request.body.decode("utf-8") if request.body else ""
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
#     secret = getattr(settings, "STRIPE_WEBHOOK_SECRET", None)

#     # Log first so we know we were hit
#     print("📩 /api/stripe/webhook/ hit")

#     if not sig_header or not secret:
#         print("❌ Missing signature header or STRIPE_WEBHOOK_SECRET")
#         return HttpResponse(status=400)

#     try:
#         event = stripe.Webhook.construct_event(payload=raw, sig_header=sig_header, secret=secret)
#     except Exception as e:
#         print("❌ Signature verification failed:", e)
#         return HttpResponse(status=400)

#     etype = event.get("type")
#     print("✅ Event:", etype)

#     if etype == "checkout.session.completed":
#         session = event["data"]["object"]
#         session_id = session.get("id")
#         md = session.get("metadata") or {}
#         customer_id = md.get("customer_id")
#         cart_id = md.get("cart_id")

#         if not (session_id and customer_id and cart_id):
#             print("⚠️ Missing metadata. session_id/customer_id/cart_id:", session_id, customer_id, cart_id)
#             return HttpResponse(status=200)  # acknowledge to avoid endless retries

#         # Idempotency: if we already created an order for this session, return 200
#         if OrderSessionMap.objects.filter(session_id=session_id).exists():
#             print("ℹ️ OrderSessionMap exists, skipping duplicate create for", session_id)
#             return HttpResponse(status=200)

#         try:
#             customer = Customers.objects.get(pk=customer_id)
#         except Customers.DoesNotExist:
#             print("❌ Customer not found:", customer_id)
#             return HttpResponse(status=200)

#         try:
#             cart = Carts.objects.get(pk=cart_id, customer=customer, status="active")
#         except Carts.DoesNotExist:
#             print("⚠️ Cart not found/active; maybe already cleared.", cart_id)
#             cart = None

#         with transaction.atomic():
#             # Compute totals from cart items (if any)
#             total_amount = Decimal("0.00")
#             line_items = []
#             if cart:
#                 items_qs = CartItems.objects.select_related("product").filter(cart=cart)
#                 for ci in items_qs:
#                     # store unit price to order_items.price (common pattern)
#                     line_items.append((ci.product_id, ci.quantity, Decimal(str(ci.product.price))))
#                     total_amount += Decimal(str(ci.product.price)) * ci.quantity

#             # Create Order
#             order = Orders.objects.create(
#                 customer=customer,
#                 total_amount=total_amount,
#                 status="paid",
#             )

#             # Create OrderItems
#             for product_id, qty, unit_price in line_items:
#                 OrderItems.objects.create(
#                     order=order,
#                     product_id=product_id,
#                     quantity=qty,
#                     price=unit_price,  # price per unit
#                 )

#             # Map session -> order
#             OrderSessionMap.objects.create(session_id=session_id, order=order)

#             # Clear the cart safely
#             if cart:
#                 CartItems.objects.filter(cart=cart).delete()
#                 cart.total_qty = 0
#                 cart.total_amount = Decimal("0.00")
#                 cart.status = "completed"
#                 cart.save(update_fields=["total_qty", "total_amount", "status"])

#             print(f"🎉 Order {order.order_id} created for session {session_id}")

#         return HttpResponse(status=200)

#     return HttpResponse(status=200)
































# from django.views.decorators.csrf import csrf_exempt
# from django.http import HttpResponse
# import stripe
# import json
# from django.conf import settings

# @csrf_exempt
# def stripe_webhook(request):
#     print("📩 /api/stripe/webhook/ hit")
#     payload = request.body
#     sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
#     # secret = "whsec_cd79cf249592f09997e722c75a42ec8a9af1574b299f0f8d7271dfcb4035c8ad"
#     if not sig_header:
#         print("❌ Missing Stripe signature header")
#         return HttpResponse(status=400)

#     try:
#         event = stripe.Webhook.construct_event(
#             payload=payload,
#             sig_header=sig_header,
#             secret=settings.STRIPE_WEBHOOK_SECRET
#             # secret=secret
#         )
#     except ValueError as e:
#         print("❌ Invalid payload:", e)
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         print("❌ Signature verification failed:", e)
#         return HttpResponse(status=400)

#     print("✅ Event type:", event.get("type"))
#     if event["type"] == "checkout.session.completed":
#         session = event["data"]["object"]
#         print("✅ Session:", json.dumps(session, indent=2))

#     return HttpResponse(status=200)

# @csrf_exempt
# def stripe_webhook(request):
#     print("📩 Incoming Webhook Request")


#     payload = request.body
#     print("📦 Raw Payload:", payload)

#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     print("🔐 Signature Header:", sig_header)

#     endpoint_secret = settings.STRIPE_WEBHOOK_SECRET


#     if sig_header is None:
#         print("❌ Missing Stripe signature header")
#         return HttpResponse(status=400)

#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
#     except ValueError as e:
#         print("❌ Invalid payload", e)
#         return HttpResponse(status=400)
#     except stripe.error.SignatureVerificationError as e:
#         print("❌ Signature verification failed", e)
#         return HttpResponse(status=400)

#     print("✅ Received Stripe Event:", event.get("type"))


#     if event['type'] == 'checkout.session.completed':
#         session = event['data']['object']
#         print("✅ Session completed payload:", json.dumps(session, indent=2))
#         print(json.dumps(session, indent=2))

#         # ✅ Create Order and OrderItems logic here

#     return HttpResponse(status=200)
