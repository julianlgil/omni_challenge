import factory
from factory.fuzzy import FuzzyInteger, FuzzyChoice

from users.tests.factories import UserFactory
from ..constants import PAYMENT_STATUS
from ..models import Payment

PAYMENT_STATUS_TO_CHOICE = [x[0] for x in PAYMENT_STATUS]
class PaymentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory(UserFactory)
    amount = FuzzyInteger(low=100)
    status = FuzzyChoice(PAYMENT_STATUS_TO_CHOICE)

