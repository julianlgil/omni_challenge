from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from .factories import PaymentFactory


class TestUrls(TestCase):
    OBTAIN_AUTH_TOKEN_URL = reverse("users:auth_token_class")
    PAYMENTS_API_URL = reverse("payments:payments_api")

    def setUp(self):
        self.payment = PaymentFactory()
        self.password = 'ArPg44628/**/'
        self.user = self.user_1 = self.payment.user
        self.user.set_password(self.password)
        self.user.save()

        response = self.client.post(self.OBTAIN_AUTH_TOKEN_URL, {
            "username": self.user.username,
            "password": self.password
        })
        self.token = response.data.get("token")
        self.PAYMENT_DETAIL_API_URL = reverse("payments:payment_api", kwargs={"pk": str(self.payment.id)})

    def test_products_api_url_response_unauthorized(self):
        response = self.client.get(self.PAYMENTS_API_URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_products_api_url_response_authorized(self):
        response = self.client.get(self.PAYMENTS_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_products_detail_api_url_response_unauthorized(self):
        response = self.client.get(self.PAYMENT_DETAIL_API_URL)
        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_products_detail_api_url_response_authorized(self):
        response = self.client.get(self.PAYMENT_DETAIL_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
