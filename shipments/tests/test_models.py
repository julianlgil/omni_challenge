import random
from uuid import uuid4

from django.test import TestCase

from orders.tests.factories import OrderFactory
from products.tests.factories import ProductFactory
from .factories import ShipmentFactory
from ..models import ProductsToShip


class TestModels(TestCase):

    def setUp(self):
        self.order = self._create_order()
        self.shipment = ShipmentFactory(order=self.order, user=self.order.user)

    @staticmethod
    def _create_product():
        product = ProductFactory()
        new_units = random.randint(1, 100)
        product.update_units(new_units)
        return product

    def _create_order(self):
        product = self._create_product()
        order = OrderFactory()
        order_product_detail = {
            "product_id": product.id,
            "units": product.available_units.units - 1
        }
        order.save_order_product_detail(order_product_detail=order_product_detail)
        return order

    def test_save_product_to_ship(self):
        products_list = [product_detail.product.id for product_detail in self.order.product_detail.all()]
        self.shipment.save_products_to_ship(products=products_list)
        payment_details_count = ProductsToShip.objects.filter(shipment=self.shipment).count()
        self.assertEqual(1, payment_details_count)
