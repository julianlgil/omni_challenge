from rest_framework import generics
from rest_framework import mixins
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .constants import PENDING
from .models import Orders, Payment
from .serializers import PaymentSerializer, CreatePaymentRequestSerializer


class PaymentsAPIView(mixins.ListModelMixin,
                      mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      generics.GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Payment.objects.filter(user=self.request.user)
        return queryset

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer_request = CreatePaymentRequestSerializer(data=request.data)
        serializer_request.is_valid(raise_exception=True)
        order_id = serializer_request.validated_data["order_id"]
        amount = serializer_request.validated_data["amount"]
        order = Orders.objects.get(id=order_id)
        if amount > order.balance:
            return Response({"error": "monto invalido"}, status=status.HTTP_400_BAD_REQUEST)
        serializer_data = {
            "user": request.user.id,
            "amount": amount,
            "status": PENDING
        }
        payment_serializer = PaymentSerializer(data=serializer_data)
        payment_serializer.is_valid(raise_exception=True)
        payment_serializer.save()
        payment = payment_serializer.instance
        payment.set_payment_detail(order=order, amount=amount)
        return Response(payment_serializer.data, status=status.HTTP_201_CREATED)


class PaymentAPIView(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.UpdateModelMixin,
                     generics.GenericAPIView):
    serializer_class = PaymentSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = Payment.objects.all()
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
        return Response(data={"status": "deleted"}, status=status.HTTP_200_OK)
