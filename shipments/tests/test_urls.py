from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .factories import ShipmentFactory


class TestUrls(TestCase):
    OBTAIN_AUTH_TOKEN_URL = reverse("users:auth_token_class")
    SHIPMENTS_API_URL = reverse("shipments:shipments_api")

    def setUp(self):
        self.shipment = ShipmentFactory()
        self.password = 'ArPg44628/**/'
        self.user = self.user_1 = self.shipment.user
        self.user.set_password(self.password)
        self.user.save()

        response = self.client.post(self.OBTAIN_AUTH_TOKEN_URL, {
            "username": self.user.username,
            "password": self.password
        })
        self.token = response.data.get("token")
        self.SHIPMENT_DETAIL_API_URL = reverse("shipments:shipment_api", kwargs={"pk": str(self.shipment.id)})

    def test_products_api_url_response_unauthorized(self):
        response = self.client.get(self.SHIPMENTS_API_URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_products_api_url_response_authorized(self):
        response = self.client.get(self.SHIPMENTS_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_products_detail_api_url_response_unauthorized(self):
        response = self.client.get(self.SHIPMENT_DETAIL_API_URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_products_detail_api_url_response_authorized(self):
        response = self.client.get(self.SHIPMENT_DETAIL_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
