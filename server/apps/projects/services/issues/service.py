import types

from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from apps.core.services.errors import BaseInfrastructureError
from apps.projects.logic.interfaces import IIssuesService
from apps.projects.logic.interfaces.issues import (
    IssueMeta,
    IssuesManagementSystem,
)
from apps.projects.models import Project
from apps.projects.services.issues import providers

_PROVIDERS_MAP = types.MappingProxyType(
    {
        IssuesManagementSystem.GITLAB: providers.GitlabProvider,
        IssuesManagementSystem.GITHUB: providers.GithubProvider,
        IssuesManagementSystem.DUMMY: providers.DummyProvider,
    },
)

_INTEGRATION_MAP = types.MappingProxyType(
    {
        IssuesManagementSystem.GITHUB: "github_integration",
        IssuesManagementSystem.GITLAB: "gitlab_integration",
    },
)


class ProjectIntegrationNotFoundError(BaseInfrastructureError):
    """Project integration not found error."""

    code = "not_found"
    message = _("MSG__PROJECT_INTEGRATION_NOT_FOUND")


class IssuesService(IIssuesService):
    """Issues service."""

    def get_issue_meta(
        self,
        url: str,
        project: Project,
        system: IssuesManagementSystem,
    ) -> IssueMeta:
        """Get issue meta from external system."""
        provider_class = _PROVIDERS_MAP[system]
        token = self._get_system_token(project, system)
        return provider_class(token).get_issue(url)

    def _get_system_token(
        self,
        project: Project,
        system: IssuesManagementSystem,
    ) -> str:
        if system == IssuesManagementSystem.DUMMY:
            return ""

        try:
            integration = getattr(project, _INTEGRATION_MAP[system])
        except ObjectDoesNotExist:
            raise ProjectIntegrationNotFoundError()

        return integration.token
