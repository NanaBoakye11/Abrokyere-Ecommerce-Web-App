from django.urls import path
from core.views.products import FeaturedProductsView, ProductsByCategoryView, ProductsGroupedByCategory, ProductDetailView

urlpatterns = [
    path('featured/', FeaturedProductsView.as_view(), name='featured-products'),
    path('category/<int:category_id>/', ProductsByCategoryView.as_view(), name='products-by-category'),
    path('grouped/', ProductsGroupedByCategory.as_view(), name='products-grouped'),
    path('<int:product_id>/', ProductDetailView.as_view(), name='product-detail'),
]