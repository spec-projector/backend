import factory

from apps.users.models import User


class UserFactory(factory.django.DjangoModelFactory):
    login = factory.Sequence(lambda n: 'User {0}'.format(n))
    name = factory.Faker('name')
    is_staff = False
    is_active = True

    class Meta:
        model = User
