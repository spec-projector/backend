import factory

from apps.billing.models import ChangeSubscriptionRequest
from tests.test_billing.factories import TariffFactory


class ChangeSubscriptionRequestFactory(factory.django.DjangoModelFactory):
    """ChangeSubscriptionRequest factory."""

    class Meta:
        model = ChangeSubscriptionRequest

    tariff = factory.SubFactory(TariffFactory)
    hash = factory.Faker("md5")
