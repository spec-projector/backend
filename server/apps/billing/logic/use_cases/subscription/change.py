from dataclasses import dataclass

import injector
from rest_framework import serializers

from apps.billing.logic.interfaces import ISubscriptionService
from apps.billing.models import ChangeSubscriptionRequest, Tariff
from apps.core.logic.helpers.validation import validate_input
from apps.core.logic.use_cases import BaseUseCase
from apps.users.models import User


@dataclass(frozen=True)
class InputDto:
    """Delete project input dto."""

    user: User
    tariff: int
    hash: str


@dataclass(frozen=True)
class OutputDto:
    """Change subscription output dto."""

    change_subcription_request: ChangeSubscriptionRequest


class _InputDtoValidator(serializers.Serializer):
    """Validator."""

    tariff = serializers.PrimaryKeyRelatedField(queryset=Tariff.objects)


class UseCase(BaseUseCase):
    """Use case for initiate change subscription."""

    @injector.inject
    def __init__(self, subscription_service: ISubscriptionService):
        """Initilize."""
        self._subscription_service = subscription_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        validated = validate_input(input_dto, _InputDtoValidator)
        request = (
            self._subscription_service.create_change_subscription_request(
                input_dto.user,
                validated["tariff"],
                input_dto.hash,
            )
        )

        return OutputDto(
            change_subcription_request=request,
        )
