from datetime import timedelta

import pytest
from django.utils import timezone

from apps.core.logic import commands
from apps.users.logic.commands.reset_password import reset as reset_command
from apps.users.logic.commands.reset_password.errors import (
    CodeValidationError,
    EmailNotExistsError,
)
from tests.test_users.factories.reset_password_request import (
    ResetPasswordRequestFactory,
)

NEW_PASSWORD = "new pass"  # noqa: S105


@pytest.fixture()
def command_data(user):
    """Create register input dto."""
    reset_password = ResetPasswordRequestFactory.create(user=user)

    return {
        "email": user.email,
        "code": reset_password.code,
        "password": NEW_PASSWORD,
    }


def test_reset_success(user, command_data):
    """Test success reset."""
    command_result = commands.execute_command(
        reset_command.Command(**command_data),
    )

    updated_user = command_result.token.user

    assert updated_user.check_password(NEW_PASSWORD)


def test_wrong_email(user, command_data):
    """Test wrong email."""
    command_data["email"] = "wrong@mail.com"

    with pytest.raises(EmailNotExistsError):
        commands.execute_command(
            reset_command.Command(**command_data),
        )


def test_wrong_code(user, command_data):
    """Test wrong code."""
    command_data["code"] = "111"

    with pytest.raises(CodeValidationError):
        commands.execute_command(
            reset_command.Command(**command_data),
        )


def test_expired_code(user, command_data):
    """Test expired code."""
    reset_password = ResetPasswordRequestFactory.create(
        user=user,
        expired_at=timezone.now() - timedelta(seconds=1),
    )
    command_data["code"] = reset_password

    with pytest.raises(CodeValidationError):
        commands.execute_command(
            reset_command.Command(**command_data),
        )
