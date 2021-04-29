from dataclasses import dataclass

import injector
from rest_framework import serializers

from apps.billing.logic.interfaces import ISubscriptionService
from apps.billing.models import ChangeSubscriptionRequest, Tariff
from apps.core.logic import commands
from apps.core.logic.helpers.validation import validate_input
from apps.users.models import User


@dataclass(frozen=True)
class ChangeSubscriptionCommand(commands.ICommand):
    """Change user subscription command."""

    user: User
    tariff: int
    hash: str


@dataclass(frozen=True)
class ChangeSubscriptionCommandResult:
    """Change subscription result."""

    change_subcription_request: ChangeSubscriptionRequest


class _CommandValidator(serializers.Serializer):
    """Validator."""

    tariff = serializers.PrimaryKeyRelatedField(queryset=Tariff.objects)


class CommandHandler(
    commands.ICommandHandler[
        ChangeSubscriptionCommand,
        ChangeSubscriptionCommandResult,
    ],
):
    """Command handler for initiate change subscription."""

    @injector.inject
    def __init__(self, subscription_service: ISubscriptionService):
        """Initilize."""
        self._subscription_service = subscription_service

    def execute(
        self,
        command: ChangeSubscriptionCommand,
    ) -> ChangeSubscriptionCommandResult:
        """Main logic here."""
        validated = validate_input(command, _CommandValidator)
        request = (
            self._subscription_service.create_change_subscription_request(
                command.user,
                validated["tariff"],
                command.hash,
            )
        )

        return ChangeSubscriptionCommandResult(
            change_subcription_request=request,
        )
