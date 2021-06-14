from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from common.models import BaseModel
from orders.constants import PENDING_SHIPPING
from orders.models import Orders, OrderProductDetail
from .constants import SHIPMENT_STATUS, DELIVERED


class Shipments(BaseModel):
    address = models.CharField(max_length=100)
    cellphone_number = models.CharField(max_length=10)
    order = models.ForeignKey(to=Orders, on_delete=models.CASCADE, related_name="shipments")
    status = models.CharField(max_length=30, choices=SHIPMENT_STATUS)

    class Meta:
        db_table = "shipments"

    def save_products_to_ship(self, products):
        order = self.order
        for product in products:
            product_detail = order.get_product_detail(product)
            ProductsToShip.objects.create(shipment=self, product_to_send=product_detail)

    def is_valid_order_to_shipped(self):
        if self.order.status != PENDING_SHIPPING:
            raise TypeError


class ProductsToShip(BaseModel):
    shipment = models.ForeignKey(to=Shipments, on_delete=models.CASCADE, related_name="products_to_ship")
    product_to_send = models.ForeignKey(to=OrderProductDetail, on_delete=models.DO_NOTHING)

    class Meta:
        db_table = "products_to_ship"
        unique_together = (("shipment", "product_to_send"),)


@receiver(post_save, sender=Shipments)
def update_product_post_save_order(sender, **kwargs):
    shipment = kwargs["instance"]
    order = shipment.order
    shipments = order.shipments.all()
    count = 0
    if order.status == shipment.status:
        return
    for shipment_by_order in shipments:
        if shipment_by_order.status == DELIVERED:
            count += 1
    if count == len(shipments) and shipment.status == DELIVERED:
        order.status = DELIVERED
    elif shipment.status != DELIVERED:
        order.status = shipment.status
    order.save()
