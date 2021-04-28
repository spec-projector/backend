from django.utils.translation import gettext_lazy as _

from apps.billing.logic.interfaces import ITariffLimitsService
from apps.billing.logic.services.subscription import NoActiveSubscriptionError
from apps.billing.models import Tariff
from apps.core.logic.errors import BaseApplicationError
from apps.projects.models import Project
from apps.users.models import User


class BaseTariffError(BaseApplicationError):
    """Base tariff error."""


class NotFoundTariffError(BaseTariffError):
    """Tariff not found error."""

    code = "tariff_not_found"
    message = _("MSG__TARIFF_NOT_FOUND")


class MaxProjectsTariffError(BaseTariffError):
    """The maximum number of projects has been reached."""

    code = "maximum_projects_limit"

    def __init__(self, allowed_count) -> None:
        """Initialize error."""
        msg = _("MSG__MAXIMUM_PROJECTS_LIMIT {allowed_count}")
        super().__init__(message=msg.format(allowed_count=allowed_count))


class MaxProjectMembersTariffError(BaseTariffError):
    """The maximum number members of project has been reached."""

    code = "maximum_project_members_limit"

    def __init__(self, allowed_count) -> None:
        """Initialize error."""
        msg = _("MSG__MAXIMUM_PROJECT_MEMBERS_LIMIT {allowed_count}")
        super().__init__(message=msg.format(allowed_count=allowed_count))


class TariffLimitsService(ITariffLimitsService):
    """Service for validate tariff limits."""

    def assert_new_project_allowed(
        self,
        user: User,
    ) -> None:
        """Check new project allowed."""
        tariff = self._get_user_tariff(user)
        if not tariff.max_projects:
            return None
        elif tariff.max_projects > Project.objects.filter(owner=user).count():
            return None

        raise MaxProjectsTariffError(tariff.max_projects)

    def assert_project_member_count_allowed(
        self,
        project: Project,
        members_count: int,
    ) -> None:
        """Check is project members count allowed."""
        tariff = self._get_user_tariff(project.owner)
        if not tariff.max_project_members:
            return None
        elif tariff.max_project_members >= members_count:
            return None

        raise MaxProjectMembersTariffError(tariff.max_project_members)

    def _get_user_tariff(self, user: User) -> Tariff:
        """Get user tariff by subscription."""
        subscription = self._subscription_service.get_user_subscription(user)
        if not subscription:
            raise NoActiveSubscriptionError()
        elif not subscription.tariff:
            raise NotFoundTariffError()

        return subscription.tariff
