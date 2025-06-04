from django.urls import path
from core.views.cart import AddToCartView

urlpatterns = [
    path('add/', AddToCartView.as_view(), name='add-to-cart'),
]
