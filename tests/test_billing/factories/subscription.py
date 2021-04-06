import factory

from apps.billing.models import Subscription
from apps.billing.models.enums import SubscriptionStatus
from tests.test_billing.factories import TariffFactory


class SubscriptionFactory(factory.django.DjangoModelFactory):
    """Subscription factory."""

    class Meta:
        model = Subscription

    tariff = factory.SubFactory(TariffFactory)
    hash = factory.Faker("md5")
    status = SubscriptionStatus.CONFIRMING
