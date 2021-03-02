from dataclasses import asdict
from datetime import timedelta

import pytest
from django.utils import timezone

from apps.core import injector
from apps.users.logic.interfaces import (
    IResetPasswordRequestService,
    ITokenService,
)
from apps.users.logic.use_cases.reset_password import reset as reset_uc
from apps.users.logic.use_cases.reset_password.errors import (
    CodeValidationError,
    EmailNotExistsError,
)
from tests.test_users.factories.reset_password_request import (
    ResetPasswordRequestFactory,
)

NEW_PASSWORD = "new pass"  # noqa: S105


@pytest.fixture()
def use_case(db):
    """Create registration use case."""
    return reset_uc.UseCase(
        token_service=injector.get(ITokenService),
        reset_password_service=injector.get(IResetPasswordRequestService),
    )


@pytest.fixture()
def input_dto(user):
    """Create register input dto."""
    reset_password = ResetPasswordRequestFactory.create(user=user)

    return reset_uc.InputDto(
        email=user.email,
        code=reset_password.code,
        password=NEW_PASSWORD,
    )


def test_reset_success(user, use_case, input_dto):
    """Test success reset."""
    output_dto = use_case.execute(input_dto)

    updated_user = output_dto.token.user

    assert updated_user.check_password(NEW_PASSWORD)


def test_wrong_email(user, use_case, input_dto):
    """Test wrong email."""
    input_data = asdict(input_dto)
    input_data["email"] = "wrong@mail.com"

    with pytest.raises(EmailNotExistsError):
        use_case.execute(reset_uc.InputDto(**input_data))


def test_wrong_code(user, use_case, input_dto):
    """Test wrong code."""
    input_data = asdict(input_dto)
    input_data["code"] = "111"

    with pytest.raises(CodeValidationError):
        use_case.execute(reset_uc.InputDto(**input_data))


def test_expired_code(user, use_case, input_dto):
    """Test expired code."""
    reset_password = ResetPasswordRequestFactory.create(
        user=user,
        expired_at=timezone.now() - timedelta(seconds=1),
    )
    input_data = asdict(input_dto)
    input_data["code"] = reset_password

    with pytest.raises(CodeValidationError):
        use_case.execute(reset_uc.InputDto(**input_data))
