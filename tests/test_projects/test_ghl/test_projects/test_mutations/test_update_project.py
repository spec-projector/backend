# -*- coding: utf-8 -*-

import pytest
from pytest import raises

from apps.core.graphql.errors import GraphQLInputError, GraphQLPermissionDenied
from apps.projects.models import ProjectMember
from apps.projects.models.project_member import PROJECT_MEMBER_ROLES
from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory
from tests.test_users.factories.user import UserFactory

GHL_QUERY_UPDATE_PROJECT = """
mutation ($id: ID!, $title: String) {
    updateProject(id: $id, title: $title) {
        project {
          id
          title
        }
    }
}
"""


@pytest.fixture()
def project():
    return ProjectFactory.create()


def test_query(user, ghl_client, project):
    """Test update raw query."""
    ghl_client.set_user(user)

    response = ghl_client.execute(
        GHL_QUERY_UPDATE_PROJECT,
        variable_values={
            "id": project.pk,
            "title": "new_{0}".format(project.title),
        },
    )

    dto = response["data"]["updateProject"]["project"]
    assert dto["id"] == str(project.id)
    assert dto["title"] == "new_{0}".format(project.title)


def test_success(user, ghl_auth_mock_info, update_project_mutation, project):
    """Test success update."""
    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        title="new title",
        description="new description",
    )

    assert response.project is not None
    assert response.project.title == "new title"
    assert response.project.description == "new description"


def test_unauth(user, ghl_mock_info, update_project_mutation, project):
    """Test unauthorized access."""
    with raises(GraphQLPermissionDenied):
        update_project_mutation(
            root=None,
            info=ghl_mock_info,
            id=project.pk,
            title="new title",
            description="new description",
        )


def test_empty_data(user, ghl_auth_mock_info, update_project_mutation, project):
    """Test empty input data."""
    with raises(GraphQLInputError) as exc_info:
        update_project_mutation(
            root=None,
            info=ghl_auth_mock_info,
            id=project.pk,
            title="",
            description="",
        )

    extensions = exc_info.value.extensions  # noqa:WPS441

    assert len(extensions["fieldErrors"]) == 2


def test_add_project_members(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    user2 = UserFactory.create()
    user3 = UserFactory.create()

    users = [
        {
            "id": user2.id,
            "roles": [PROJECT_MEMBER_ROLES.PROJECT_MANAGER],
        },
        {
            "id": user3.id,
            "roles": [PROJECT_MEMBER_ROLES.PROJECT_MANAGER],
        },
    ]

    assert not project.members.exists()

    update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        users=users,
    )

    assert project.members.count() == 2
    assert set(project.members.all()) == {user2, user3}


def test_delete_project_members(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    project_member1 = ProjectMemberFactory.create(project=project)
    project_member2 = ProjectMemberFactory.create(project=project)

    assert project.members.count() == 2

    users = [
        {
            "id": project_member1.user.id,
            "roles": [PROJECT_MEMBER_ROLES.PROJECT_MANAGER],
        },
    ]

    update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        users=users,
    )

    assert project.members.count() == 1
    assert project.members.first() == project_member1.user
    assert not ProjectMember.objects.filter(id=project_member2.id).exists()
