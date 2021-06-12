from django.db import models
from common.models import BaseModel
from products.models import Products
from django.contrib.auth.models import User
from .constants import ORDER_STATUS


class Orders(BaseModel):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    total_order_price = models.FloatField()
    balance = models.FloatField(default=0)
    status = models.CharField(max_length=30, choices=ORDER_STATUS)

    class Meta:
        db_table = "orders"

    def get_product_detail(self, product):
        try:
            product_detail = self.product_detail.get(product=product)
            return product_detail
        except Exception:
            return None

    def save_order_product_detail(self, order_product_detail):
        units_to_order = order_product_detail["units"]
        product_id = order_product_detail["product_id"]
        product = Products.objects.get(id=product_id)
        if units_to_order <= product.available_units.units:
            product_total_price = product.unit_price * units_to_order
            order_product_detail = self.get_product_detail(product=product)
            if order_product_detail:
                order_product_detail.units = units_to_order
                order_product_detail.total_price = product_total_price
                order_product_detail.save()
            else:
                order_product_detail = OrderProductDetail.objects.create(order=self, product=product,
                                                                         units=units_to_order,
                                                                         total_price=product_total_price)
            return order_product_detail
        return None

    def update_order(self, total_order_price, balance):
        self.total_order_price = total_order_price
        self.balance = balance
        self.save()


class OrderProductDetail(BaseModel):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE, related_name="product_detail")
    product = models.ForeignKey(Products, on_delete=models.DO_NOTHING)
    units = models.IntegerField()
    total_price = models.FloatField()

    class Meta:
        db_table = "orders_products_detail"
        unique_together = (("order", "product"),)
