import random
from uuid import uuid4

from django.test import TestCase

from orders.tests.factories import OrderFactory
from products.tests.factories import ProductFactory
from .factories import PaymentFactory
from ..models import PaymentDetail


class TestModels(TestCase):

    def setUp(self):
        self.payment = PaymentFactory()
        self.order = self._create_order()

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

    def test_set_payment_detail(self):
        self.payment.set_payment_detail(order=self.order, amount=self.order.balance)
        payment_details_count = PaymentDetail.objects.filter(payment=self.payment).count()
        self.assertEqual(1, payment_details_count)
