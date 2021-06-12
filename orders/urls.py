from django.urls import path
from .views import OrdersAPIView, OrderAPIView

app_name = "orders"

urlpatterns = [
    path('', OrdersAPIView.as_view(), name='orders_api'),
    path('<str:pk>/', OrderAPIView.as_view(), name='order_api'),

]
