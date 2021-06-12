from django.urls import path

from .views import PaymentsAPIView, PaymentAPIView

app_name = "payments"

urlpatterns = [
    path('', PaymentsAPIView.as_view(), name='payments_api'),
    path('<str:pk>/', PaymentAPIView.as_view(), name='payment_api'),

]
