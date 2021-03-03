from dataclasses import asdict

import pytest

from apps.core import injector
from apps.core.logic.interfaces import IEmailService
from apps.core.models import EmailMessage
from apps.users.logic.interfaces import IResetPasswordRequestService
from apps.users.logic.use_cases.reset_password import (
    send_password_reset as send_reset_uc,
)
from apps.users.logic.use_cases.reset_password.errors import (
    EmailNotExistsError,
)
from apps.users.models import ResetPasswordRequest


@pytest.fixture()
def use_case(db):
    """Create send service use case."""
    return send_reset_uc.UseCase(
        reset_password_service=injector.get(IResetPasswordRequestService),
        email_service=injector.get(IEmailService),
    )


@pytest.fixture()
def input_dto(user):
    """Create register input dto."""
    return send_reset_uc.InputDto(email=user.email)


def test_send_reset_success(user, use_case, input_dto):
    """Test success reset."""
    assert not ResetPasswordRequest.objects.filter(user=user).exists()

    output_dto = use_case.execute(input_dto)

    assert output_dto.ok
    assert ResetPasswordRequest.objects.filter(user=user).exists()
    assert EmailMessage.objects.filter(to=input_dto.email).exists()


def test_wrong_email(user, use_case, input_dto):
    """Test wrong email."""
    input_data = asdict(input_dto)
    input_data["email"] = "wrong@mail.com"

    with pytest.raises(EmailNotExistsError):
        use_case.execute(send_reset_uc.InputDto(**input_data))

    assert not EmailMessage.objects.filter(to=input_dto.email).exists()
