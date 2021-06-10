import pytest

from apps.core.logic import commands
from apps.core.models import EmailMessage
from apps.users.logic.commands.reset_password import (
    send_password_reset as command,
)
from apps.users.logic.commands.reset_password.errors import EmailNotExistsError
from apps.users.models import ResetPasswordRequest


@pytest.fixture()
def command_data(user):
    """Create register input dto."""
    return {
        "email": user.email,
    }


def test_send_reset_success(user, command_data):
    """Test success reset."""
    assert not ResetPasswordRequest.objects.filter(user=user).exists()

    commands.execute_command(command.Command(**command_data))

    assert ResetPasswordRequest.objects.filter(user=user).exists()
    assert EmailMessage.objects.filter(to=command_data["email"]).exists()


def test_wrong_email(user, command_data):
    """Test wrong email."""
    command_data["email"] = "wrong@mail.com"

    with pytest.raises(EmailNotExistsError):
        commands.execute_command(
            command.Command(**command_data),
        )

    assert not EmailMessage.objects.filter(to=command_data["email"]).exists()
