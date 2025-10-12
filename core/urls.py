# core/urls.py

from django.urls import path, include
from core.views.products import FeaturedProductsView
from core.views.auth import AuthStatusView
from core.views.cart import CartDetailView
from core.views.cart import UpdateCartItemView, RemoveCartItemView
from core.views.checkout import CreateCheckoutSessionView
from core.views.stripe_webhook import stripe_webhook
from core.views.orders import RecentOrdersView, OrderBySessionView


urlpatterns = [
    # path('api/auth/', include('core.urls.auth')),
    path('auth/', include('core.urls.auth')),

                #PRODUCTS#
    path('products/featured/', FeaturedProductsView.as_view(), name='featured-products'),
    path('products/', include('core.urls.product_urls')),
    path('cart/', include('core.urls.cart')),

                    # Cart Items #
    path('cart/update-item/', UpdateCartItemView.as_view()),
    path('cart/remove-item/<int:cart_item_id>/', RemoveCartItemView.as_view(), name='remove-cart-item'),

                #CHECKOUT + WEBHOOK
    path("checkout/create-session/", CreateCheckoutSessionView.as_view()),
    path("stripe/webhook/", stripe_webhook, name="stripe-webhook"),

   # orders
    path('orders/recent/', RecentOrdersView.as_view()),
    path('orders/by-session/<str:session_id>/', OrderBySessionView.as_view()),

                
                
                
                #OLD CODE NOT NEEDED
    # path('cart/', CartDetailView.as_view(), name='cart-detail'),
    # path('api/auth/user/', AuthStatusView.as_view(), name='auth-status'),
]
