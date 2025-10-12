# core/urls/stripe_urls.py
from django.urls import path
from core.views.stripe_webhook import stripe_webhook

urlpatterns = [
    path('webhook/', stripe_webhook, name='stripe-webhook'),  # /api/stripe/webhook/
]
