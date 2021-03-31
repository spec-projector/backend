import factory
from django.contrib.auth.hashers import make_password

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    """User factory."""

    class Meta:
        model = User

    login = factory.Sequence(lambda index: "user_{0}".format(index))
    email = factory.Sequence(lambda index: "user_{0}@gl.com".format(index))
    name = factory.Faker("name")
    password = make_password(None)
    is_staff = False
    is_active = True
