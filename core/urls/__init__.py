# # core/urls/__init__.py

# from django.urls import path
# from core.views.products import FeaturedProductsView

# urlpatterns = [
#     path("products/featured/", FeaturedProductsView.as_view(), name="featured-products"),
# ]


from django.urls import path, include

urlpatterns = [
    path('auth/', include('core.urls.auth')),
    path('products/', include('core.urls.products_urls')),
]