import pytest

from tests.test_projects.factories.figma_integration import (
    FigmaIntegrationFactory,
)
from tests.test_projects.factories.github_integration import (
    GitHubIntegrationFactory,
)
from tests.test_projects.factories.gitlab_integration import (
    GitLabIntegrationFactory,
)
from tests.test_projects.factories.project import ProjectFactory


@pytest.fixture()
def project(user):
    """Create project."""
    return ProjectFactory.create(owner=user)


@pytest.fixture()
def figma_integration(project):
    """Create figma integration."""
    return FigmaIntegrationFactory.create(project=project)


@pytest.fixture()
def github_integration(project):
    """Create github integration."""
    return GitHubIntegrationFactory.create(project=project)


@pytest.fixture()
def gitlab_integration(project):
    """Create gitlab integration."""
    return GitLabIntegrationFactory.create(project=project)
