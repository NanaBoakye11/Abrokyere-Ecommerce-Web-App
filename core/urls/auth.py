# core/urls/auth.py

from django.urls import path
from core.views.auth import RegisterView
from core.views.auth import LoginView
from core.views.products import FeaturedProductsView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='customer-register'),
    path('login/', LoginView.as_view(), name='customer-login'),
    # path('products/featured/', FeaturedProductsView.as_view(), name='featured-products')
]
