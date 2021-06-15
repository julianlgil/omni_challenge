import random
from typing import (
    Iterable,
    Union
)

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.tests.factories import UserFactory
from .factories import ProductFactory


class TestViews(TestCase):
    OBTAIN_AUTH_TOKEN_URL = reverse("users:auth_token_class")
    PRODUCTS_API_URL = reverse("products:products_api")

    def setUp(self):
        self.password = 'ArPg44628/**/'
        self.user = self.user_1 = UserFactory()
        self.user.set_password(self.password)
        self.user.save()

        response = self.client.post(self.OBTAIN_AUTH_TOKEN_URL, {
            "username": self.user.username,
            "password": self.password
        })
        self.token = response.data.get("token")
        self.product = ProductFactory()
        self.PRODUCTS_DETAIL_API_URL = reverse("products:products_detail_api", kwargs={"pk": str(self.product.id)})

    @staticmethod
    def mock_random_products():
        products_list = []
        for _ in range(0, random.randint(1, 100)):
            products_list.append(ProductFactory())

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
        response = self.client.get(self.PRODUCTS_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.check_asserts_pagination_structure(response=response)

    def test_get_products_list(self):
        mock_products = self.mock_random_products()
        response = self.client.get(self.PRODUCTS_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(mock_products.__len__() + 1, response.data.get("count"))

    def test_create_product(self):
        product_data = {
            "name": "Jean",
            "description": "Lorem ipsun",
            "unit_price": 1000
        }
        response = self.client.post(
            path=self.PRODUCTS_API_URL,
            data=product_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("created_at", response.data)

    def test_retrieve_product(self):
        response = self.client.get(self.PRODUCTS_DETAIL_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(self.product.id), response.data.get("id"))

    def test_add_valid_units_to_product(self):
        units_to_update = random.randint(1, 100)
        units_data = {
            "units": units_to_update
        }
        response = self.client.post(
            path=self.PRODUCTS_DETAIL_API_URL,
            data=units_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("units", response.data)
        self.assertEqual(int(response.data.get("units")), units_to_update)

    def test_add_invalid_units_to_product(self):
        units_to_update = random.randint(1, 100) * -1
        units_data = {
            "units": units_to_update
        }
        response = self.client.post(
            path=self.PRODUCTS_DETAIL_API_URL,
            data=units_data,
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_name_to_product(self):
        old_name = self.product.name
        product_data = {
            "name": "new_name",
            "description": "this product change"
        }
        response = self.client.put(
            path=self.PRODUCTS_DETAIL_API_URL,
            data=product_data,
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("name", response.data)
        self.assertNotEqual(response.data.get("name"), old_name)

    def test_delete_product(self):
        response = self.client.delete(
            path=self.PRODUCTS_DETAIL_API_URL,
            content_type='application/json',
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
