from apps.projects.models import ProjectMember
from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory


def test_query(user, ghl_client, ghl_raw):
    """Test getting empty project members raw query."""
    ghl_client.set_user(user)

    project = ProjectFactory.create(owner=user)

    response = ghl_client.execute(
        ghl_raw("get_project"),
        variable_values={"id": project.id},
    )

    assert "errors" not in response
    assert not response["data"]["project"]["members"]


def test_retrieve_member_with_permissions(user, ghl_client, ghl_raw):
    """Test getting project members."""
    ghl_client.set_user(user)

    project = ProjectFactory.create(owner=user)
    ProjectMemberFactory.create(
        project=project,
        user=user,
        permissions=(
            ProjectMember.permissions.EDIT_FEATURES
            | ProjectMember.permissions.EDIT_MODEL
        ),
    )

    response = ghl_client.execute(
        ghl_raw("get_project"),
        variable_values={"id": project.id},
    )

    project_response = response["data"]["project"]

    assert "errors" not in response
    assert project_response["id"] == str(project.id)
    assert set(project_response["members"][0]["permissions"]) == {
        "EDIT_FEATURES",
        "EDIT_MODEL",
    }
