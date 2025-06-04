import uuid
from django.utils import timezone
from core.models.cart_items import CartItems
from core.models.carts import Carts
from core.models.products import Products


def get_or_create_cart(customer_id):
    cart, _ = Carts.objects.get_or_create(
        customer_id=customer_id,
        status = 'active',
        defaults={
        "total_qty": 0,
        "total_amount": 0.00,
        "created_at": timezone.now(),
        "updated_at": timezone.now(),
    }
    )
    return cart

def add_item_to_cart(customer_id, product_id, quantity):
    product = Products.objects.get(product_id=product_id)
    price = product.price

    cart = get_or_create_cart(customer_id)

    cart_item, created = CartItems.objects.get_or_create(
        cart_id = cart.cart_id,
        product_id = product_id,
        defaults={
            "quantity": quantity,
            "price": price,
            "added_at": timezone.now(),
            "updated_at": timezone.now()
        }
    )
    if not created:
        cart_item.quantity += quantity
        cart_item.updated_at = timezone.now()
        cart_item.save()

    all_items = CartItems.objects.filter(cart_id=cart_id)
    total_qty = sum(item.quantity for item in all_items)
    total_amount = sum(item.quantity * item.price for item in all_items)

    cart.total_qty = total_qty
    cart.total_amount = total_amount
    cart.updated_at = timezone.now()
    cart.save()

    return cart_item

