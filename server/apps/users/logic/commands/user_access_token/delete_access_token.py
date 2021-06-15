from dataclasses import dataclass

from rest_framework import serializers

from apps.core.logic import commands
from apps.core.logic.errors import AccessDeniedApplicationError
from apps.core.logic.helpers.validation import validate_input
from apps.users.models import User, UserAccessToken


class DeleteAccessTokenDtoValidator(serializers.Serializer):
    """Delete access token validator."""

    id = serializers.PrimaryKeyRelatedField(
        queryset=UserAccessToken.objects,
        source="token",
    )


@dataclass(frozen=True)
class DeleteUserAccessTokenDto:
    """Delete user access token data."""

    id: str


@dataclass(frozen=True)
class Command(commands.ICommand):
    """Delete user access token input dto."""

    data: DeleteUserAccessTokenDto  # noqa: WPS110
    user: User


class CommandHandler(commands.ICommandHandler[Command, None]):
    """Delete user access token."""

    def execute(self, command: Command) -> None:
        """Main logic here."""
        validated_data = validate_input(
            command.data,
            DeleteAccessTokenDtoValidator,
        )
        if validated_data["token"].user != command.user:
            raise AccessDeniedApplicationError()

        validated_data["token"].delete()
