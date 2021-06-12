from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from users.tests.factories import UserFactory
from .factories import ProductFactory


class TestUrls(TestCase):
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

    def test_products_api_url_response_unauthorized(self):
        response = self.client.get(self.PRODUCTS_API_URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_products_api_url_response_authorized(self):
        response = self.client.get(self.PRODUCTS_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_products_detail_api_url_response_unauthorized(self):
        response = self.client.get(self.PRODUCTS_DETAIL_API_URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_products_detail_api_url_response_authorized(self):
        response = self.client.get(self.PRODUCTS_DETAIL_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
