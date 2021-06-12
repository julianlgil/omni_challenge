from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .constants import OPEN
from .models import Orders
from .serializers import OrdersSerializer, OrderProductDetailsSerializer, OrderProductsListSerializer


class OrdersAPIView(mixins.ListModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    serializer_class = OrdersSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Orders.objects.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer_data = {
            "user": request.user.id,
            "total_order_price": 0,
            "status": OPEN
        }
        order_serializer = OrdersSerializer(data=serializer_data)
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save()
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


class OrderAPIView(mixins.RetrieveModelMixin,
                    mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    generics.GenericAPIView):
    serializer_class = OrdersSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Orders.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer_data = {
            "user": request.user.id,
            "total_order_price": 0,
            "status": OPEN
        }
        order_serializer = OrdersSerializer(data=serializer_data)
        order_serializer.is_valid(raise_exception=True)
        order_serializer.save()
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)

    def put(self, request, *args, **kwargs):
        order = self.get_object()
        product_list_serializer = OrderProductsListSerializer(data=request.data)
        product_list_serializer.is_valid(raise_exception=True)
        products_unavailable = []
        total_order_price = 0
        for product_to_order in product_list_serializer.validated_data["products"]:
            order_product_detail = order.save_order_product_detail(product_to_order)
            if order_product_detail:
                total_order_price += order_product_detail.total_price
            else:
                products_unavailable.append(product_to_order["product_id"])

        order.update_order(total_order_price=total_order_price, balance=total_order_price)
        status_response = status.HTTP_200_OK
        if products_unavailable:
            status_response = status.HTTP_206_PARTIAL_CONTENT
        return Response({"products_unavailable": products_unavailable, "order": OrdersSerializer(order).data},
                        status=status_response)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.status == OPEN:
            self.perform_destroy(instance)
            return Response({"status": "deleted"}, status=status.HTTP_200_OK)
        return Response({"status": "order can not be deleted, because it's not OPEN"}, status=status.HTTP_403_FORBIDDEN)