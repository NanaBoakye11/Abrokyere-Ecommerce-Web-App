from django.urls import path
from core.views.cart import AddToCartView, CartDetailView
from core.views.cart import UpdateCartItemView, RemoveCartItemView
# from .cart import UpdateCartItemView, RemoveCartItemView



urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
    path('', CartDetailView.as_view(), name='cart-detail'),  # ✅ this line enables GET /api/cart/
    path('update-item/', UpdateCartItemView.as_view(), name='update-cart-item'),
    path('remove-item/<uuid:cart_item_id>/', RemoveCartItemView.as_view(), name='remove-cart-item'),
]
