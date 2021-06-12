import factory
from ..models import Products
from factory.fuzzy import FuzzyText, FuzzyFloat


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Products

    name = factory.Faker('name')
    description = FuzzyText(length=200)
    unit_price = FuzzyFloat(low=100)
