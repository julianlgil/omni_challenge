import factory
from factory.fuzzy import FuzzyInteger, FuzzyChoice

from users.tests.factories import UserFactory
from ..constants import ORDER_STATUS
from ..models import Orders


ORDER_STATUS_TO_CHOICE = [x[0] for x in ORDER_STATUS]
class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Orders

    user = factory.SubFactory(UserFactory)
    total_order_price = FuzzyInteger(low=100)
    balance = total_order_price
    status = FuzzyChoice(ORDER_STATUS_TO_CHOICE)
