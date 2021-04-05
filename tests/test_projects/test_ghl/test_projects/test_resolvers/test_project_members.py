from graphene_django.rest_framework.tests.test_mutation import mock_info

from apps.projects.graphql.types import ProjectType
from tests.test_projects.factories import ProjectFactory, ProjectMemberFactory


def test_empty(db):
    """Test project members not exists."""
    project = ProjectFactory.create()
    queryset = ProjectType.resolve_members(project, mock_info())

    assert not queryset.exists()


def test_member_not_active(user):
    """Test project members not active."""
    user.is_active = False
    user.save()

    project_member = ProjectMemberFactory.create(user=user)
    queryset = ProjectType.resolve_members(project_member.project, mock_info())

    assert not queryset.exists()


def test_get_members(db):
    """Test retrieve project members."""
    size_project_members = 5
    project = ProjectFactory.create()
    project_members = ProjectMemberFactory.create_batch(
        size=size_project_members,
        project=project,
    )

    queryset = ProjectType.resolve_members(project, mock_info())

    assert queryset.count() == size_project_members
    assert set(queryset) == set(project_members)
