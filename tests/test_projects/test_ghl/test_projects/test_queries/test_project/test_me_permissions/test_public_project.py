from apps.core.utils.fields import get_all_selected_bitfield
from apps.projects.models import ProjectMember
from apps.projects.models.enums import ProjectMemberRole, ProjectPermission


def test_public_project(user, project, ghl_client, ghl_raw):
    """Test getting public project not authorized user."""
    ghl_client.set_user(user)
    response = ghl_client.execute(
        ghl_raw("get_project"),
        variable_values={"id": project.id},
    )
    assert "errors" not in response

    project_response = response["data"]["project"]
    assert project_response["id"] == str(project.id)
    _check_permissions(
        project_response["me"],
        project.public_role,
        project.public_permissions,
    )


def test_public_project_as_member(
    project_member,
    project,
    ghl_client,
    ghl_raw,
):
    """Test get public project as project member."""
    project_member.permissions = (
        ProjectMember.permissions.EDIT_SPRINTS
        | ProjectMember.permissions.EDIT_MODULES
    )
    project_member.save()

    ghl_client.set_user(project_member.user)
    response = ghl_client.execute(
        ghl_raw("get_project"),
        variable_values={"id": project.id},
    )
    assert "errors" not in response

    project_response = response["data"]["project"]
    assert project_response["id"] == str(project.id)
    _check_permissions(
        project_response["me"],
        project_member.role,
        project_member.permissions,
    )


def test_not_auth_user(project, ghl_client, ghl_raw):
    """Test not auth user."""
    response = ghl_client.execute(
        ghl_raw("get_project"),
        variable_values={"id": project.id},
    )
    assert "errors" not in response

    project_response = response["data"]["project"]
    assert project_response["id"] == str(project.id)
    _check_permissions(
        project_response["me"],
        project.public_role,
        project.public_permissions,
    )


def test_as_owner(user, project, ghl_client, ghl_raw):
    """Test as owner."""
    ghl_client.set_user(user)
    project.owner = user
    project.save()

    response = ghl_client.execute(
        ghl_raw("get_project"),
        variable_values={"id": project.id},
    )
    assert "errors" not in response

    project_response = response["data"]["project"]
    assert project_response["id"] == str(project.id)
    _check_permissions(
        project_response["me"],
        ProjectMemberRole.EDITOR,
        get_all_selected_bitfield(ProjectPermission),
    )


def _check_permissions(
    response_permissions,
    expected_role,
    expected_permissions,
) -> None:
    """Assert permissions from response."""
    assert response_permissions["role"] == expected_role
    assert response_permissions["permissions"] == [
        permissions for permissions, is_set in expected_permissions if is_set
    ]
