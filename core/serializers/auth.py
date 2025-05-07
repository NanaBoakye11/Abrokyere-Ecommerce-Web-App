# core/serializers/auth.py

from rest_framework import serializers

class CustomerLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
