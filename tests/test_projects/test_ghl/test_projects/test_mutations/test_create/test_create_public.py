from apps.projects.models import Project
from apps.projects.models.enums import ProjectMemberRole, ProjectPermission


def test_create_public_role(
    user,
    ghl_auth_mock_info,
    create_project_mutation,
    couchdb_service,
):
    """Test create with public role."""
    response = create_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "title": "my project",
            "public_role": ProjectMemberRole.EDITOR,
        },
    )

    assert response.project.public_role == ProjectMemberRole.EDITOR


def test_create_public_permissions(
    user,
    ghl_auth_mock_info,
    create_project_mutation,
    couchdb_service,
):
    """Test create with public permissions."""
    response = create_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        input={
            "title": "my project",
            "public_permissions": [
                ProjectPermission.VIEW_CONTRACT,
                ProjectPermission.EDIT_SPRINTS,
                ProjectPermission.EDIT_MODEL,
            ],
        },
    )

    assert int(response.project.public_permissions) == (
        Project.public_permissions.VIEW_CONTRACT
        | Project.public_permissions.EDIT_SPRINTS
        | Project.public_permissions.EDIT_MODEL
    )
