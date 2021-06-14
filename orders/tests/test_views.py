import random
from typing import (
    Iterable,
    Union
)

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from products.tests.factories import ProductFactory
from .factories import OrderFactory
from ..constants import OPEN, DELIVERED


class TestViews(TestCase):
    OBTAIN_AUTH_TOKEN_URL = reverse("users:auth_token_class")
    ORDERS_API_URL = reverse("orders:orders_api")

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
        self.ORDER_DETAIL_API_URL = reverse("orders:order_api", kwargs={"pk": str(self.order.id)})

    @staticmethod
    def mock_random_orders(user):
        products_list = []
        for _ in range(0, random.randint(1, 100)):
            products_list.append(OrderFactory(user=user))
        return products_list

    def check_asserts_pagination_structure(self, response):
        self.assertIn("count", response.data.keys())
        self.assertIsInstance(response.data.get("count"), int)

        self.assertIn("next", response.data.keys())
        self.assertIsInstance(response.data.get("next"), Union[str, None].__args__)

        self.assertIn("previous", response.data.keys())
        self.assertIsInstance(response.data.get("previous"), Union[str, None].__args__)

        self.assertIn("results", response.data.keys())
        self.assertIsInstance(response.data.get("results"), Iterable)

    def test_get_products_pagination_structure(self):
        response = self.client.get(self.ORDERS_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.check_asserts_pagination_structure(response=response)

    def test_get_products_list(self):
        mock_products = self.mock_random_orders(self.user)
        response = self.client.get(self.ORDERS_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mock_products.__len__() + 1, response.data.get("count"))

    def test_create_product(self):
        response = self.client.post(
            path=self.ORDERS_API_URL,
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("created_at", response.data)

    def test_retrieve_product(self):
        response = self.client.get(self.ORDER_DETAIL_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(self.order.id), response.data.get("id"))

    def test_add_products_to_order_when_not_availble_units(self):
        product1 = ProductFactory()
        units = random.randint(1, 100)
        product1.update_units(units)
        order_product = {
            "products": [{
                "product_id": product1.id,
                "units": units + 1
            }]
        }
        response = self.client.put(
            path=self.ORDER_DETAIL_API_URL,
            data=order_product,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_206_PARTIAL_CONTENT)
        self.assertIn(product1.id, response.data["products_unavailable"])

    def test_add_products_to_order(self):
        product1 = ProductFactory()
        units = random.randint(1, 100)
        product1.update_units(units)
        order_product = {
            "products": [{
                "product_id": product1.id,
                "units": units - 1
            }]
        }
        response = self.client.put(
            path=self.ORDER_DETAIL_API_URL,
            data=order_product,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(product1.id, response.data["products_unavailable"])

    def test_delete_when_order_status_is_OPEN(self):
        self.order.status = OPEN
        self.order.save()
        response = self.client.delete(
            path=self.ORDER_DETAIL_API_URL,
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_delete_when_order_status_is_not_OPEN(self):
        self.order.status = DELIVERED
        self.order.save()
        response = self.client.delete(
            path=self.ORDER_DETAIL_API_URL,
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)
