# core/urls/auth.py

from django.urls import path, include
from core.views.auth import RegisterView, AuthStatusView, LoginView
from core.views.products import FeaturedProductsView


urlpatterns = [
    path('register/', RegisterView.as_view(), name='customer-register'),
    path('login/', LoginView.as_view(), name='customer-login'),
    path('user/', AuthStatusView.as_view(), name='auth-status'),  # ✅ Add this


    # path('products/featured/', FeaturedProductsView.as_view(), name='featured-products')
]
