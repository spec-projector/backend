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
