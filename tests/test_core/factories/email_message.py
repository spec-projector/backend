import factory

from apps.core.models import EmailMessage


class EmailMessageFactory(factory.django.DjangoModelFactory):
    """Email message factory."""

    class Meta:
        model = EmailMessage

    to = factory.Faker("email")
    subject = factory.Faker("text", max_nb_chars=20)
    html = factory.Faker("text", max_nb_chars=600)
