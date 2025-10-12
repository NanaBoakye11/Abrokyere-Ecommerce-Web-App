# core/urls/orders_urls.py
from django.urls import path
from core.views.orders import OrderBySessionView, RecentOrdersView

urlpatterns = [
    path("by-session/<str:session_id>/", OrderBySessionView.as_view()),
    path("recent/", RecentOrdersView.as_view()),
]