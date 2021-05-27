import pytest


@pytest.fixture()
def project(project):
    """Update project."""
    project.is_public = False
    project.save()

    return project


def test_not_auth_user_not_public(project, ghl_client, ghl_raw):
    """Test not auth user not public project."""
    response = ghl_client.execute(
        ghl_raw("get_project"),
        variable_values={"id": project.id},
    )
    assert "errors" not in response
    assert response["data"]["project"] is None


def test_not_public_project_not_owner_not_member(
    user,
    project,
    ghl_client,
    ghl_raw,
):
    """Test not public project."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        ghl_raw("get_project"),
        variable_values={"id": project.id},
    )

    assert "errors" not in response
    assert response["data"]["project"] is None


def test_not_public_as_owner(user, project, ghl_client, ghl_raw):
    """Test not public as owner."""
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
        project.public_role,
        project.public_permissions,
    )


def test_not_public_as_member(project_member, project, ghl_client, ghl_raw):
    """Test not public project as member."""
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
