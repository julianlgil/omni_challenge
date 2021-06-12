from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from .models import Products
from .serializers import (
    ProductsSerializer,
    UnitsProductSerializer
)
from rest_framework import status
from rest_framework.response import Response


class ProductsAPIView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      generics.GenericAPIView):
    serializer_class = ProductsSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Products.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class ProductsDetailAPIView(mixins.RetrieveModelMixin,
                            mixins.UpdateModelMixin,
                            mixins.DestroyModelMixin,
                            generics.GenericAPIView):
    serializer_class = ProductsSerializer
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        queryset = Products.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = UnitsProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        units = serializer.validated_data.get("units")

        product = self.get_object()
        updated_units = product.update_units(units_to_update=units)

        if not updated_units:
            return Response({"error": "Invalid operation"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(ProductsSerializer(product).data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"status": "deleted"}, status=status.HTTP_200_OK)
