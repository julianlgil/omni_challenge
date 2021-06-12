from django.test import TestCase

from .factories import ProductFactory
from ..models import AvailableProducts
import random


class TestModels(TestCase):

    def setUp(self):
        self.product = ProductFactory()

    def test_creation_available_products_model(self):
        available_product_count = AvailableProducts.objects.filter(product=self.product).count()
        self.assertEqual(1, available_product_count)

    def test_get_units(self):
        available_product = self.product.available_units
        new_units = random.randint(1, 100)
        available_product.units = new_units
        available_product.save()
        self.assertEqual(new_units, self.product.get_units())

    def test_update_units(self):
        new_units = random.randint(1, 100)
        self.product.update_units(new_units)
        self.assertEqual(new_units, self.product.get_units())
