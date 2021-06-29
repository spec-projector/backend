from apps.core.utils.bit_field import get_all_selected_bitfield
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
        },
    )

    assert response.project.public_permissions == get_all_selected_bitfield(
        ProjectPermission,
    )
