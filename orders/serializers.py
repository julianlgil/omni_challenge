from rest_framework import serializers

from .models import Orders


class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Orders
        fields = ("id", "user", "total_order_price", "status", "created_at", "updated_at")
        read_only = ("id", "user", "total_order_price", "status", "created_at", "updated_at")


class OrderProductDetailsSerializer(serializers.Serializer):
    product_id = serializers.UUIDField()
    units = serializers.IntegerField()


class OrderProductsListSerializer(serializers.Serializer):
    products = OrderProductDetailsSerializer(many=True)
