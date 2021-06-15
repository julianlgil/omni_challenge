import random
import uuid
from typing import (
    Iterable,
    Union
)

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from orders.tests.factories import OrderFactory
from products.tests.factories import ProductFactory
from .factories import ShipmentFactory


class TestViews(TestCase):
    OBTAIN_AUTH_TOKEN_URL = reverse("users:auth_token_class")
    PAYMENTS_API_URL = reverse("shipments:shipments_api")

    def setUp(self):
        self.order = OrderFactory()
        self.password = 'ArPg44628/**/'
        self.user = self.user_1 = self.order.user
        self.user.set_password(self.password)
        self.user.save()

        response = self.client.post(self.OBTAIN_AUTH_TOKEN_URL, {
            "username": self.user.username,
            "password": self.password
        })
        self.token = response.data.get("token")
        self._update_order()
        self.shipment = ShipmentFactory(user=self.user, order=self.order)
        self.products_list = [product_detail.product.id for product_detail in self.order.product_detail.all()]
        self.shipment.save_products_to_ship(products=self.products_list)
        self.PAYMENT_DETAIL_API_URL = reverse("shipments:shipment_api", kwargs={"pk": str(self.shipment.id)})

    @staticmethod
    def mock_random_payments(user):
        payments_list = []
        for _ in range(0, random.randint(1, 10)):
            payments_list.append(ShipmentFactory(user=user))
        return payments_list

    @staticmethod
    def _create_product():
        product = ProductFactory()
        new_units = random.randint(1, 100)
        product.update_units(new_units)
        return product

    def _update_order(self):
        product = self._create_product()
        order_product_detail = {
            "product_id": product.id,
            "units": product.available_units.units - 1
        }
        self.order.save_order_product_detail(order_product_detail=order_product_detail)

    def check_asserts_pagination_structure(self, response):
        self.assertIn("count", response.data.keys())
        self.assertIsInstance(response.data.get("count"), int)

        self.assertIn("next", response.data.keys())
        self.assertIsInstance(response.data.get("next"), Union[str, None].__args__)

        self.assertIn("previous", response.data.keys())
        self.assertIsInstance(response.data.get("previous"), Union[str, None].__args__)

        self.assertIn("results", response.data.keys())
        self.assertIsInstance(response.data.get("results"), Iterable)

    def test_get_payments_pagination_structure(self):
        response = self.client.get(self.PAYMENTS_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.check_asserts_pagination_structure(response=response)

    def test_get_payments_list(self):
        mock_payments = self.mock_random_payments(self.user)
        response = self.client.get(self.PAYMENTS_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(mock_payments) + 1, response.data.get("count"))

    def test_create_payment(self):
        shipment_request = {
            "order_id": self.order.id,
            "address": "calle falsa 123",
            "cellphone_number": "3111111111",
            "products_to_ship": self.products_list
        }
        response = self.client.post(
            path=self.PAYMENTS_API_URL,
            data=shipment_request,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("created_at", response.data)

    def test_create_payment_with_invalid_product(self):
        shipment_request = {
            "order_id": self.order.id,
            "address": "calle falsa 123",
            "cellphone_number": "3111111111",
            "products_to_ship": [uuid.uuid4()]
        }
        response = self.client.post(
            path=self.PAYMENTS_API_URL,
            data=shipment_request,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_create_payment_with_invalid_order(self):
        order = OrderFactory(user=self.user, status="DELIVERED")
        shipment_request = {
            "order_id": order.id,
            "address": "calle falsa 123",
            "cellphone_number": "3111111111",
            "products_to_ship": [uuid.uuid4()]
        }
        response = self.client.post(
            path=self.PAYMENTS_API_URL,
            data=shipment_request,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    def test_retrieve_payment(self):
        response = self.client.get(self.PAYMENT_DETAIL_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(self.shipment.id), response.data.get("id"))

    def test_change_shipmet_status_to_shipped(self):
        status_shipment_request = {
            "status": "SHIPPED"
        }
        response = self.client.put(
            path=self.PAYMENT_DETAIL_API_URL,
            data=status_shipment_request,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("SHIPPED", response.data["status"])

    def test_change_payment_status_to_delivered(self):
        status_payment_request = {
            "status": "DELIVERED"
        }
        response = self.client.put(
            path=self.PAYMENT_DETAIL_API_URL,
            data=status_payment_request,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("DELIVERED", response.data["status"])

    def test_delete_payment(self):
        response = self.client.delete(
            path=self.PAYMENT_DETAIL_API_URL,
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
