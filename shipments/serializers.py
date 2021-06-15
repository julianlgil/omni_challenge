from rest_framework import serializers

from shipments.models import Shipments


class ShipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shipments
        fields = ("id", "user", "order", "address", "cellphone_number", "status", "created_at", "updated_at")
        read_only = ("id", "user", "order", "created_at", "updated_at")


class CreateShipmentRequestSerializer(serializers.Serializer):
    order_id = serializers.UUIDField()
    products_to_ship = serializers.ListField(child=serializers.UUIDField())
    address = serializers.CharField(max_length=200)
    cellphone_number = serializers.CharField(max_length=10)
