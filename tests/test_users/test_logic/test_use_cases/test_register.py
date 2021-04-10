from dataclasses import asdict

import pytest

from apps.billing.models import Subscription
from apps.billing.models.enums import SubscriptionStatus
from apps.core import injector
from apps.users.logic.use_cases.register import register as register_uc
from apps.users.logic.use_cases.register.errors import (
    RegistrationInputError,
    UserAlreadyExistsError,
)
from apps.users.models import User
from tests.test_billing.factories import TariffFactory

LAST_NAME = "newuser"
EMAIL = "new_user@mail.net"


@pytest.fixture()
def use_case(db):
    """Create registration use case."""
    return injector.get(register_uc.UseCase)


@pytest.fixture()
def input_dto(db):
    """Create register input dto."""
    return register_uc.InputDto(
        first_name="new user",
        email=EMAIL,
        last_name=LAST_NAME,
        password="123456",
    )


def test_success(use_case, input_dto):
    """Test success register."""
    output_dto = use_case.execute(input_dto)

    user = output_dto.token.user

    _assert_user(user, input_dto)
    assert user.is_active


def test_subscription(use_case, input_dto):
    """Test auto create default subscription."""
    tariff = TariffFactory.create(is_default=True)
    output_dto = use_case.execute(input_dto)

    user = output_dto.token.user

    _assert_user(user, input_dto)
    assert user.is_active
    assert Subscription.objects.filter(
        user=user,
        tariff=tariff,
        status=SubscriptionStatus.ACTIVE,
    ).exists()


def test_exists_user(user, input_dto, use_case):
    """Test exists_login. Not create new users."""
    user.email = input_dto.email
    user.save()

    with pytest.raises(UserAlreadyExistsError):
        use_case.execute(input_dto)

    assert User.objects.count() == 1


@pytest.mark.parametrize(
    ("user_field", "field_value"),
    [
        ("first_name", "a" * 51),
        ("last_name", "b" * 51),
        ("email", "{0}@net.com".format("c" * 50)),
        ("email", "wrong_email"),
    ],
)
def test_wrong_input_data(use_case, input_dto, user_field, field_value):
    """Test wrong input. Wrong lengths from User - model."""
    input_data = asdict(input_dto)
    input_data[user_field] = field_value

    with pytest.raises(RegistrationInputError):
        use_case.execute(register_uc.InputDto(**input_data))


def _assert_user(user, input_dto) -> None:
    """Assert user."""
    assert user.email == input_dto.email
    assert user.first_name == input_dto.first_name
    assert user.last_name == input_dto.last_name
    assert user.password
