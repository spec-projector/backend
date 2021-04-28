import abc

from apps.billing.models import Subscription


class IUserTariffService(abc.ABC):
    """User tariff service interface."""

    @abc.abstractmethod
    def validate_max_projects(
        self,
        subscription: Subscription,
        projects_count: int,
    ) -> None:
        """Validate max projects."""

    @abc.abstractmethod
    def validate_max_project_members(
        self,
        subscription: Subscription,
        members_count: int,
    ) -> None:
        """Validate max project members."""
