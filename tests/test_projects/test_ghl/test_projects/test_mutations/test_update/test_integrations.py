from apps.projects.models import FigmaIntegration
from tests.test_projects.factories.figma_integration import (
    FigmaIntegrationFactory,
)
from tests.test_projects.factories.github_integration import (
    GitHubIntegrationFactory,
)
from tests.test_projects.factories.gitlab_integration import (
    GitLabIntegrationFactory,
)


def test_add_integration(
    user,
    project,
    ghl_auth_mock_info,
    update_project_mutation,
    couchdb_service,
):
    """Test add integration."""
    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "title": "project",
            "figma_integration": {"token": "super token"},
        },
    )

    integration = response.project.figma_integration
    assert integration
    assert integration.token == "super token"


def test_update_integration(
    user,
    project,
    ghl_auth_mock_info,
    update_project_mutation,
    couchdb_service,
):
    """Test update integration."""
    FigmaIntegration.objects.create(project=project, token="token")
    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "title": "project",
            "figma_integration": {"token": "super token"},
        },
    )

    integration = response.project.figma_integration
    assert integration
    assert integration.token == "super token"


def test_delete_integration(
    user,
    project,
    ghl_auth_mock_info,
    update_project_mutation,
    couchdb_service,
):
    """Test delete integration."""
    FigmaIntegration.objects.create(project=project, token="token")
    update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "title": "project",
            "figma_integration": None,
        },
    )

    assert not FigmaIntegration.objects.filter(project=project).exists()


def test_update_integration_is_empty_object(
    user,
    ghl_auth_mock_info,
    update_project_mutation,
    project,
):
    """Test success update with empty integrations."""
    _add_integrations(project)
    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "title": "new title",
            "description": "new description",
            "figma_integration": {},
            "github_integration": {},
            "gitlab_integration": {},
        },
    )

    assert response.project is not None
    assert response.project.title == "new title"
    assert response.project.description == "new description"

    _assert_integrations(project)


def _assert_integrations(project) -> None:
    """Assert integrations."""
    assert project.figma_integration.token
    assert project.gitlab_integration.token
    assert project.github_integration.token


def _add_integrations(project) -> None:
    """Add integrations for project."""
    integrations = (
        FigmaIntegrationFactory,
        GitHubIntegrationFactory,
        GitLabIntegrationFactory,
    )
    for integration in integrations:
        integration.create(project=project)  # type: ignore
