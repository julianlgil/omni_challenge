from django.db import transaction
from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .constants import PENDING
from .models import Orders, Shipments
from .serializers import ShipmentSerializer, CreateShipmentRequestSerializer


class ShipmentsAPIView(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       mixins.DestroyModelMixin,
                       generics.GenericAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Shipments.objects.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        request_serializer = CreateShipmentRequestSerializer(data=request.data)
        request_serializer.is_valid(raise_exception=True)
        serializer_data = {
            "user": request.user.id,
            "order": request_serializer.validated_data["order_id"],
            "status": PENDING,
            "address": request_serializer.validated_data["address"],
            "cellphone_number": request_serializer.validated_data["cellphone_number"]
        }
        shipment_serialized = ShipmentSerializer(data=serializer_data)
        shipment_serialized.is_valid(raise_exception=True)
        shipment_serialized.save()
        shipment = shipment_serialized.instance
        try:
            with transaction.atomic():
                shipment.is_valid_order_to_shipped()
                shipment.save_products_to_ship(products=request_serializer.validated_data["products_to_ship"])
        except TypeError:
            return Response({"error": "The order status is not valid"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        except Exception:
            return Response({"error": "There are product(s) that do(es) not exist in this order"},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response(shipment_serialized.data, status=status.HTTP_201_CREATED)


class ShipmentAPIView(mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      mixins.UpdateModelMixin,
                      generics.GenericAPIView):
    serializer_class = ShipmentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Shipments.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)
