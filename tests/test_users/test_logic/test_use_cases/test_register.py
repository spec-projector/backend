from dataclasses import asdict

import pytest

from apps.core import injector
from apps.users.logic.interfaces import ITokenService
from apps.users.logic.use_cases.register import register as register_uc
from apps.users.logic.use_cases.register.errors import (
    RegistrationInputError,
    UserAlreadyExistsError,
)
from apps.users.models import User

LOGIN = "newuser"
EMAIL = "new_user@mail.net"


@pytest.fixture()
def use_case(db):
    """Create registration use case."""
    return register_uc.UseCase(token_service=injector.get(ITokenService))


@pytest.fixture()
def input_dto(db):
    """Create register input dto."""
    return register_uc.InputDto(
        name="new user",
        email=EMAIL,
        login=LOGIN,
        password="123456",
    )


def test_register_success(use_case, input_dto):
    """Test success register."""
    output_dto = use_case.execute(input_dto)

    user = output_dto.token.user

    _assert_user(user, input_dto)
    assert user.is_active


@pytest.mark.parametrize(
    ("user_field", "field_value"),
    [
        ("login", LOGIN),
        ("email", EMAIL),
    ],
)
def test_exists_user(user, input_dto, use_case, user_field, field_value):
    """Test exists_login. Not create new users."""
    setattr(user, user_field, field_value)
    user.save()

    input_data = asdict(input_dto)
    input_data[user_field] = field_value

    with pytest.raises(UserAlreadyExistsError):
        use_case.execute(register_uc.InputDto(**input_data))

    assert User.objects.count() == 1


@pytest.mark.parametrize(
    ("user_field", "field_value"),
    [
        ("name", "a" * 51),
        ("login", "b" * 21),
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
    assert user.name == input_dto.name
    assert user.email == input_dto.email
    assert user.login == input_dto.login
    assert user.password
