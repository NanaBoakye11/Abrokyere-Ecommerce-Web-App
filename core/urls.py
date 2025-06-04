# core/urls.py

from django.urls import path, include
from core.views.products import FeaturedProductsView


urlpatterns = [
    path('api/auth/', include('core.urls.auth')),
    path('products/featured/', FeaturedProductsView.as_view(), name='featured-products'),
    path('products/', include('core.urls.product_urls')),
    path('cart/', include('core.urls.cart')),
]
