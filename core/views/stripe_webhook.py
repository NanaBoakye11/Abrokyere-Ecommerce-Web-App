# core/views/stripe_webhook.py
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.conf import settings
from django.db import transaction
from decimal import Decimal
import json, stripe
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from core.models import Carts, CartItems, Customers, Orders, OrderItems, OrderSessionMap

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
        # from django.utils import timezone
        # from core.models import Carts, CartItems, Orders, OrderItems, OrderSessionMap
        session_id = data_obj.get("id")
        payment_intent = data_obj.get("payment_intent")
        metadata = data_obj.get("metadata", {}) or {}
        
        # --- FIX APPLIED HERE ---
        raw_cart_id = metadata.get("cart_id")
        raw_customer_id = metadata.get("customer_id")
        
        try:
            # 1. CAST: Convert string IDs from metadata to integers for database query
            cart_id = int(raw_cart_id) if raw_cart_id else None
            customer_id = int(raw_customer_id) if raw_customer_id else None
        except (ValueError, TypeError) as e:
            # Handle non-numeric or missing data gracefully
            print(f"❌ Metadata casting error: {e}. Raw IDs: cart_id='{raw_cart_id}', customer_id='{raw_customer_id}'")
            return HttpResponse(status=200) # Stop processing if data is corrupted
        # ------------------------

        print("🧾 Session:", json.dumps({
            "id": session_id,
            "payment_intent": payment_intent,
            "metadata": metadata
        }, indent=2))
        
        # Added for clear diagnosis:
        print(f"DEBUG: Casted IDs used for query: cart_id={cart_id}, customer_id={customer_id}") 

        if not session_id:
            print("⚠️ No session_id on event")
            return HttpResponse(status=200)

        # Idempotency check... (rest of the code)
        try:
            if OrderSessionMap.objects.filter(session_id=session_id).exists():
                print(f"🔁 Session already processed ({session_id}).")
                return HttpResponse(status=200)
        except Exception as e:
            print(f"⚠️ Map check failed: {e}")

        # Use the casted integer IDs here
        if not cart_id or not customer_id:
            print("⚠️ Missing cart_id/customer_id metadata; cannot create order.")
            return HttpResponse(status=200)

        try:
            # 1. Fetch the Customer instance
            # Use .get() to raise DoesNotExist if customer is missing
            customer = Customers.objects.get(customer_id=customer_id)
            print(f"DEBUG: Customer instance found: {customer.email}")

            # 2. LOOKUP: Query uses the casted integer values
            cart = Carts.objects.filter(cart_id=cart_id, customer_id=customer_id).first()
            if not cart:
                # If the cart still isn't found, the IDs don't exist in the database.
                print(f"⚠️ No cart found for cart_id={cart_id}, customer_id={customer_id}")
                return HttpResponse(status=200)

            items = list(CartItems.objects.select_related("product").filter(cart=cart))
            # ... (rest of the transaction logic is correct)
            if not items:
                print("⚠️ Cart empty at webhook time.")
                return HttpResponse(status=200)

            with transaction.atomic():
                # ... order creation and cart clearing logic ...
                total_amount = sum(Decimal(str(i.product.price)) * i.quantity for i in items)

                # Order creation
                order = Orders.objects.create(
                    customer=customer,
                    order_date=timezone.now(),
                    total_amount=total_amount,
                    status="paid",
                )
                print(f"DEBUG: Order create with ID: {order.order_id}")

                OrderItems.objects.bulk_create([
                    OrderItems(
                        order=order,
                        product=i.product,
                        quantity=i.quantity,
                        price=i.product.price,  # unit price
                    ) for i in items
                ])
                print(f"DEBUG: Order items created.")

                OrderSessionMap.objects.create(session_id=session_id, order=order)
                print(f"DEBUG: OrderSessionMap created for session {session_id}.")

                # Clear cart
                CartItems.objects.filter(cart=cart).delete()
                cart.total_qty = 0
                cart.total_amount = 0
                cart.status = "completed"
                cart.save(update_fields=["total_qty", "total_amount", "status"])
                print("DEBUG: Cart cleared and status updated.")

                print(f"🎉 Order {order.order_id} created, mapped to session {session_id}. Cart cleared.")
        except Customers.DoesNotExist:
            print(f"⚠️ Customer {customer_id} not found in DB. Cannot create order.")
            return HttpResponse(status=200)
        
        except Exception as e:
            print(f"🔥 Webhook error creating order: {e}")
            return HttpResponse(status=200)
    return HttpResponse(status=200)








