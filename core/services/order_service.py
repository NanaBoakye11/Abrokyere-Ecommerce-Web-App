from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from core.models import Carts, CartItems, Customers, Products
from core.models import Orders, OrderItems
from core.models import WebhookEventLog


@transaction.atomic
def create_order_from_cart_unmanaged(cart, stripe_session, event_id: str):
    """
    Create an Orders row plus OrderItems from a cart using your unmanaged tables.
    Idempotent via WebhookEventLog.
    Returns (order, created_flag).
    """
    # Idempotency gate
    if WebhookEventLog.objects.filter(event_id=event_id).exists():
        # Already processed
        existing_order = Orders.objects.filter(status="paid").order_by("-order_id").first()
        return existing_order, False

    # Build order header
    email = None
    cd = (stripe_session.get("customer_details") or {})
    email = cd.get("email") or (stripe_session.get("metadata", {}) or {}).get("customer_email") \
            or (cart.customer.email if cart.customer_id else None)

    order = Orders.objects.create(
        customer=cart.customer,            # DO_NOTHING FK – you already have Customers row
        order_date=timezone.now(),
        total_amount=Decimal("0.00"),      # will update after items
        status="paid",
    )

    total = Decimal("0.00")
    items = cart.cartitems_set.select_related("product")

    for ci in items:
        unit_price = Decimal(str(ci.product.price))  # store unit price in order_items.price
        qty = ci.quantity
        line_total = unit_price * qty

        OrderItems.objects.create(
            order=order,
            product=ci.product,
            quantity=qty,
            price=unit_price,
        )

        total += line_total

    # Update header total
    order.total_amount = total
    order.save(update_fields=["total_amount"])

    # Mark webhook processed
    WebhookEventLog.objects.create(event_id=event_id)

    return order, True


@transaction.atomic
def clear_cart(cart):
    """Delete items and reset totals on existing unmanaged cart."""
    cart.cartitems_set.all().delete()
    cart.total_qty = 0
    cart.total_amount = Decimal("0.00")
    cart.status = "active"     # keep active (or set to 'completed' if that’s your flow)
    cart.save(update_fields=["total_qty", "total_amount", "status"])
