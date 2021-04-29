import pytest

from apps.billing.models import Subscription
from apps.billing.models.enums import SubscriptionStatus
from apps.core.logic import commands
from apps.users.logic.commands import register
from apps.users.logic.commands.register.errors import (
    RegistrationInputError,
    UserAlreadyExistsError,
)
from apps.users.models import User


def test_success(db, command_data):
    """Test success register."""
    command_result = commands.execute_command(
        register.RegisterCommand(**command_data),
    )

    user = command_result.token.user

    _assert_user(user, command_data)
    assert user.is_active


def test_subscription(
    db,
    command_data,
    default_tariff_config,
    default_tariff,
):
    """Test auto create default subscription."""
    command_result = commands.execute_command(
        register.RegisterCommand(**command_data),
    )

    user = command_result.token.user

    _assert_user(user, command_data)
    assert user.is_active
    assert Subscription.objects.filter(
        user=user,
        tariff=default_tariff,
        status=SubscriptionStatus.ACTIVE,
    ).exists()


def test_exists_user(user, command_data):
    """Test exists_login. Not create new users."""
    user.email = command_data["email"]
    user.save()

    with pytest.raises(UserAlreadyExistsError):
        commands.execute_command(register.RegisterCommand(**command_data))

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
def test_wrong_input_data(command_data, user_field, field_value):
    """Test wrong input. Wrong lengths from User - model."""
    command_data[user_field] = field_value

    with pytest.raises(RegistrationInputError):
        commands.execute_command(register.RegisterCommand(**command_data))


def _assert_user(user, command_data) -> None:
    assert user.email == command_data["email"]
    assert user.first_name == command_data["first_name"]
    assert user.last_name == command_data["last_name"]
    assert user.password
