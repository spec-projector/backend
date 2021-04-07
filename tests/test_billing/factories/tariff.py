import factory

from apps.billing.models import Tariff


class TariffFactory(factory.django.DjangoModelFactory):
    """Tariff factory."""

    class Meta:
        model = Tariff

    code = factory.Faker("word")
    title = factory.Faker("word")
    teaser = factory.Faker("word")
    is_active = True
