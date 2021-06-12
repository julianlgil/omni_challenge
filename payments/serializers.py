from rest_framework import serializers

from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ("id", "user", "amount", "status", "created_at", "updated_at")
        read_only = ("id", "user", "created_at", "updated_at")

