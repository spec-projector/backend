import factory

from apps.users.models import UserAccessToken
from tests.test_users.factories.user import UserFactory


class UserAccessTokenFactory(factory.django.DjangoModelFactory):
    """User access token factory."""

    class Meta:
        model = UserAccessToken

    user = factory.SubFactory(UserFactory)
    name = factory.Faker("word")
