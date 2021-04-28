import abc

import injector

from apps.billing.logic.interfaces import ISubscriptionService
from apps.projects.models import Project
from apps.users.models import User


class ITariffLimitsService(abc.ABC):
    """Tariff limits interface."""

    @injector.inject
    def __init__(self, subscription_service: ISubscriptionService):
        """Initilize."""
        self._subscription_service = subscription_service

    @abc.abstractmethod
    def assert_new_project_allowed(
        self,
        user: User,
    ) -> None:
        """Check new project allowed."""

    @abc.abstractmethod
    def assert_project_member_count_allowed(
        self,
        project: Project,
        members_count: int,
    ) -> None:
        """Check max project members."""
