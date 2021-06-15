import random
from typing import (
    Iterable,
    Union
)

from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from orders.tests.factories import OrderFactory
from .factories import PaymentFactory


class TestViews(TestCase):
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
        self.order = OrderFactory(user=self.user)
        self.payment.set_payment_detail(order=self.order, amount=self.payment.amount)
        self.PAYMENT_DETAIL_API_URL = reverse("payments:payment_api", kwargs={"pk": str(self.payment.id)})

    @staticmethod
    def mock_random_payments(user):
        payments_list = []
        for _ in range(0, random.randint(1, 10)):
            payments_list.append(PaymentFactory(user=user))
        return payments_list

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
        payment_request = {
            "order_id": self.order.id,
            "amount": self.order.balance
        }
        response = self.client.post(
            path=self.PAYMENTS_API_URL,
            data=payment_request,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("created_at", response.data)

    def test_create_payment_with_amount_not_valid(self):
        payment_reuqest = {
            "order_id": self.order.id,
            "amount": self.order.balance + 1
        }
        response = self.client.post(
            path=self.PAYMENTS_API_URL,
            data=payment_reuqest,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_payment(self):
        response = self.client.get(self.PAYMENT_DETAIL_API_URL, HTTP_AUTHORIZATION=f"Bearer {self.token}")
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEqual(str(self.payment.id), response.data.get("id"))

    def test_change_payment_status_to_successful(self):
        status_payment_request = {
            "status": "SUCCESSFUL"
        }
        response = self.client.put(
            path=self.PAYMENT_DETAIL_API_URL,
            data=status_payment_request,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("SUCCESSFUL", response.data["status"])

    def test_change_payment_status_to_pending_payment(self):
        status_payment_request = {
            "status": "PENDING"
        }
        response = self.client.put(
            path=self.PAYMENT_DETAIL_API_URL,
            data=status_payment_request,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("PENDING", response.data["status"])

    def test_change_payment_status_to_successful_with_balance_0(self):
        order_with_balance_0 = OrderFactory(user=self.user, balance=0)
        self.payment.set_payment_detail(order=order_with_balance_0, amount=self.payment.amount)
        status_payment_request = {
            "status": "SUCCESSFUL"
        }
        response = self.client.put(
            path=self.PAYMENT_DETAIL_API_URL,
            data=status_payment_request,
            content_type="application/json",
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertIn("SUCCESSFUL", response.data["status"])

    def test_delete_payment(self):
        response = self.client.delete(
            path=self.PAYMENT_DETAIL_API_URL,
            HTTP_AUTHORIZATION=f"Bearer {self.token}"
        )
        self.assertEquals(response.status_code, status.HTTP_200_OK)
