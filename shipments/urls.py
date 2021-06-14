from django.urls import path

from .views import ShipmentsAPIView, ShipmentAPIView

app_name = "shipments"

urlpatterns = [
    path('', ShipmentsAPIView.as_view(), name='shipments_api'),
    path('<str:pk>/', ShipmentAPIView.as_view(), name='shipment_api'),

]
