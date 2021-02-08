from apps.projects.models import FigmaIntegration


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
