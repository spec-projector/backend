from apps.projects.models import Project
from apps.projects.models.enums import ProjectMemberRole, ProjectPermission


def test_update_public_role(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test update public role."""
    project.public_role = ProjectMemberRole.VIEWER
    project.save()

    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "is_public": True,
            "public_role": ProjectMemberRole.EDITOR,
        },
    )

    assert response.project == project
    assert response.project.public_role == ProjectMemberRole.EDITOR


def test_update_public_permissions(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test update public permissions."""
    project.public_permissions = (
        Project.public_permissions.EDIT_FEATURES
        | Project.public_permissions.EDIT_FEATURE_WORKFLOW
    )
    project.save()

    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "is_public": True,
            "public_permissions": [
                ProjectPermission.VIEW_CONTRACT,
                ProjectPermission.EDIT_SPRINTS,
                ProjectPermission.EDIT_MODEL,
            ],
        },
    )

    assert response.project == project
    assert int(response.project.public_permissions) == (
        Project.public_permissions.VIEW_CONTRACT
        | Project.public_permissions.EDIT_SPRINTS
        | Project.public_permissions.EDIT_MODEL
    )
