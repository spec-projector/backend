from dataclasses import dataclass

from rest_framework import serializers

from apps.billing.logic.services import SubscriptionService
from apps.billing.logic.use_cases.subscription import errors
from apps.billing.models import ChangeSubscriptionRequest, Tariff
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


class InputDtoValidator(serializers.Serializer):
    """Delete project input."""

    tariff = serializers.PrimaryKeyRelatedField(queryset=Tariff.objects)


class UseCase(BaseUseCase):
    """Use case for initiate change subscription."""

    def __init__(self, subscription_service: SubscriptionService):
        """Initilize."""
        self._subscription_service = subscription_service

    def execute(self, input_dto: InputDto) -> OutputDto:
        """Main logic here."""
        tariff = self._get_tariff(input_dto.tariff)
        request = self._subscription_service.change_user_subscription(
            input_dto.user,
            tariff,
            input_dto.hash,
        )

        return OutputDto(
            change_subcription_request=request,
        )

    def _get_tariff(self, tariff_id: int) -> Tariff:
        try:
            return Tariff.objects.get(is_active=True, pk=tariff_id)
        except Tariff.DoesNotExist:  # noqa: WPS329
            raise errors.InvalidTariffError()
