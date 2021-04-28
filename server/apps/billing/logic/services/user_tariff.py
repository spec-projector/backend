from django.utils.translation import gettext_lazy as _

from apps.billing.logic.interfaces import IUserTariffService
from apps.billing.logic.services.subscription import NoActiveSubscriptionError
from apps.billing.models import Subscription, Tariff
from apps.core.logic.errors import BaseApplicationError


class BaseTariffError(BaseApplicationError):
    """Base tariff error."""


class NotFoundTariffError(BaseTariffError):
    """Tariff not found error."""

    code = "tariff_not_found"
    message = _("MSG__TARIFF_NOT_FOUND")


class MaxProjectsTariffError(BaseTariffError):
    """The maximum number of projects has been reached."""

    code = "maximum_number_of_projects_has_been_reached"
    message = _("MSG__THE_MAXIMUM_NUMBER_OF_PROJECTS_HAS_BEEN_REACHED")


class MaxProjectMembersTariffError(BaseTariffError):
    """The maximum number members of project has been reached."""

    code = "maximum_number_members_of_project_has_been_reached"
    message = _("MSG__THE_MAXIMUM_NUMBER_MEMBERS_OF_PROJECT_HAS_BEEN_REACHED")


class UserTariffService(IUserTariffService):
    """Service for validate tariff features."""

    def validate_max_projects(
        self,
        subscription: Subscription,
        projects_count: int,
    ) -> None:
        """Validate max projects by subscription."""
        tariff = self._validate_tariff(subscription)

        if not tariff.max_projects:
            return None
        elif tariff.max_projects >= projects_count:
            return None

        raise MaxProjectsTariffError()

    def validate_max_project_members(
        self,
        subscription: Subscription,
        members_count: int,
    ) -> None:
        """Validate max project members by subscription."""
        tariff = self._validate_tariff(subscription)
        if not tariff.max_project_members:
            return None
        elif tariff.max_project_members >= members_count:
            return None

        raise MaxProjectMembersTariffError()

    def _validate_tariff(self, subscription: Subscription) -> Tariff:
        """Validate tariff."""
        if not subscription:
            raise NoActiveSubscriptionError()
        elif not subscription.tariff:
            raise NotFoundTariffError()

        return subscription.tariff
