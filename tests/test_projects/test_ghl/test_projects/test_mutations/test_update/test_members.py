import pytest
from django.db import models
from jnt_django_graphene_toolbox.errors import GraphQLInputError

from apps.projects.models import ProjectMember
from apps.projects.models.project_member import ProjectMemberRole
from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory
from tests.test_users.factories.user import UserFactory


@pytest.fixture()
def project():
    """Provides project."""
    return ProjectFactory.create()


def test_delete_project_members(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test delete project members."""
    project_member1 = ProjectMemberFactory.create(project=project)
    project_member2 = ProjectMemberFactory.create(project=project)

    assert project.members.count() == 2

    users = [
        {
            "id": project_member1.user.id,
            "roles": [ProjectMemberRole.PROJECT_MANAGER],
        },
    ]

    update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "users": users,
        },
    )

    assert project.members.count() == 1
    assert project.members.first() == project_member1.user
    assert not ProjectMember.objects.filter(id=project_member2.id).exists()


def test_add_project_members(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test add project members."""
    user2 = UserFactory.create()
    user3 = UserFactory.create()

    users = [
        {"id": user2.id, "roles": [ProjectMemberRole.PROJECT_MANAGER]},
        {"id": user3.id, "roles": [ProjectMemberRole.PROJECT_MANAGER]},
    ]

    assert not project.members.exists()

    update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "users": users,
        },
    )

    assert project.members.count() == 2
    assert set(project.members.all()) == {user2, user3}


def test_update_project_member_roles(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test updating project member roles."""
    frontend = ProjectMember.roles.FRONTEND_DEVELOPER
    manager = ProjectMember.roles.PROJECT_MANAGER
    tester = ProjectMember.roles.TESTER

    query = models.Q(roles=frontend | manager)

    ProjectMemberFactory(
        user=user,
        project=project,
        roles=tester,
    )

    assert not ProjectMember.objects.filter(query).exists()

    users = [
        {
            "id": user.id,
            "roles": [
                ProjectMemberRole.FRONTEND_DEVELOPER,
                ProjectMemberRole.PROJECT_MANAGER,
            ],
        },
    ]

    update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "users": users,
        },
    )

    assert ProjectMember.objects.filter(query).count() == 1
    assert not ProjectMember.objects.filter(roles=tester).exists()


def test_roles_not_setted_validate(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test roles are not setted_validation."""
    users = [
        {"id": user.id},
    ]

    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "users": users,
        },
    )
    assert isinstance(response, GraphQLInputError)


def test_roles_is_empty(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test roles are not empty validation."""
    users = [
        {"id": user.id, "roles": []},
    ]

    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "users": users,
        },
    )

    assert isinstance(response, GraphQLInputError)


def test_roles_not_valid(
    user,
    project,
    update_project_mutation,
    ghl_auth_mock_info,
):
    """Test roles are not valid validation."""
    users = [
        {"id": user.id, "roles": ["NO_VALID"]},
    ]

    response = update_project_mutation(
        root=None,
        info=ghl_auth_mock_info,
        id=project.pk,
        input={
            "users": users,
        },
    )

    assert isinstance(response, GraphQLInputError)
