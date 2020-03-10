# -*- coding: utf-8 -*-

from apps.projects.models import ProjectMember
from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory

GHL_QUERY_PROJECT = """
query ($id: ID!) {
  project(id: $id) {
    id
    members {
      user {
        id
      }
      roles
    }
  }
}
"""


def test_query(user, ghl_client):
    """Test getting empty project members raw query."""
    ghl_client.set_user(user)

    project = ProjectFactory.create(owner=user)

    response = ghl_client.execute(
        GHL_QUERY_PROJECT, variable_values={"id": project.id},
    )

    assert "errors" not in response
    assert not response["data"]["project"]["members"]


def test_retrieve_member_with_roles(user, ghl_client):
    """Test getting project members."""
    ghl_client.set_user(user)

    project = ProjectFactory.create(owner=user)
    ProjectMemberFactory.create(
        project=project,
        user=user,
        roles=(
            ProjectMember.roles.BACKEND_DEVELOPER
            | ProjectMember.roles.FRONTEND_DEVELOPER
        ),
    )

    response = ghl_client.execute(
        GHL_QUERY_PROJECT, variable_values={"id": project.id},
    )

    project_resp = response["data"]["project"]

    assert "errors" not in response
    assert project_resp["id"] == str(project.id)
    assert set(project_resp["members"][0]["roles"]) == {
        "BACKEND_DEVELOPER",
        "FRONTEND_DEVELOPER",
    }
