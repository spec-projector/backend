import factory

from apps.users.models import ResetPasswordRequest
from tests.test_users.factories.user import UserFactory


class ResetPasswordRequestFactory(factory.django.DjangoModelFactory):
    """Reset password request factory."""

    class Meta:
        model = ResetPasswordRequest

    user = factory.SubFactory(UserFactory)
