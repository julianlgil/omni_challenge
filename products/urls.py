from django.urls import path
from .views import ProductsAPIView, ProductsDetailAPIView

app_name = "products"

urlpatterns = [
    path('', ProductsAPIView.as_view(), name='products_api'),
    path('<str:pk>/', ProductsDetailAPIView.as_view(), name='products_detail_api'),
]
