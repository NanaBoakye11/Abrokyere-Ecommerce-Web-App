from django.urls import path
from core.views.products import FeaturedProductsView, ProductsByCategoryView

urlpatterns = [
    path('featured/', FeaturedProductsView.as_view(), name='featured-products'),
    path('category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products-by-category'),
]