from uuid import uuid4

import factory
from django.test import TestCase

from products.models import Products
from products.tests.factories import ProductFactory
from .factories import OrderFactory
from ..models import OrderProductDetail
import random


class TestModels(TestCase):

    def setUp(self):
        self.order = OrderFactory()
        self.product = self._create_product()
        self.order_product_detail = {
            "product_id": self.product.id,
            "units": self.product.available_units.units-1
        }
        self.order.save_order_product_detail(order_product_detail=self.order_product_detail)

    @staticmethod
    def _create_product():
        product = ProductFactory()
        new_units = random.randint(1, 100)
        product.update_units(new_units)
        return product


    def test_save_order_product_detail(self):
        self.order.save_order_product_detail(order_product_detail=self.order_product_detail)
        order_products_count = OrderProductDetail.objects.filter(order=self.order).count()
        self.assertEqual(1, order_products_count)

    def test_get_product_detail(self):
        order_product_detail = self.order.get_product_detail(self.product.id)
        self.assertEqual(self.order_product_detail.get("product_id"), order_product_detail.product_id)


    def test_get_product_detail_when_product_not_exist(self):
        order_product_detail = self.order.get_product_detail(product=uuid4())
        self.assertEqual(None, order_product_detail)
