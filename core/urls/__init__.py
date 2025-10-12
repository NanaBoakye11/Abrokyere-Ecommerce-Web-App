# # core/urls/__init__.py

# from django.urls import path
# from core.views.products import FeaturedProductsView

# urlpatterns = [
#     path("products/featured/", FeaturedProductsView.as_view(), name="featured-products"),
# ]


from django.urls import path, include
from core.views.checkout import CreateCheckoutSessionView
from core.views.stripe_webhook import stripe_webhook
from core.views.products import FeaturedProductsView

urlpatterns = [
    path('auth/', include('core.urls.auth')),
    path('products/', include('core.urls.products_urls')),
    path('products/featured/', FeaturedProductsView.as_view(), name='featured-products'),

    path('cart/', include('core.urls.cart')),
    path('checkout/create-session/', CreateCheckoutSessionView.as_view(), name='checkout-create-session'),
    path('orders/', include('core.urls.orders_urls')),

    # Stripe webhook
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),

]