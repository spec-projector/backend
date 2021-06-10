import pytest
from django.contrib.auth.models import AnonymousUser

from apps.core.logic import queries
from apps.projects.logic.queries.project.allowed import Query
from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory


@pytest.fixture()
def public_project(db):
    """Create project."""
    return ProjectFactory.create(is_public=True)


@pytest.fixture()
def private_project(db):
    """Create project."""
    return ProjectFactory.create(is_public=False)


def test_as_anonymus(public_project, private_project, query_bus):
    """Test available is public project."""
    projects = queries.execute_query(
        Query(user=AnonymousUser, include_public=True),
    )

    assert projects.count() == 1
    assert projects.first() == public_project


def test_projects_as_owner(user, private_project, query_bus):
    """Test empty projects."""
    private_project.owner = user
    private_project.save()

    projects = queries.execute_query(
        Query(user=user, include_public=True),
    )

    assert projects.count() == 1
    assert projects.first() == private_project


def test_user_is_project_member(user, private_project, query_bus):
    """Test empty projects."""
    ProjectMemberFactory.create(user=user, project=private_project)

    projects = queries.execute_query(
        Query(user=user, include_public=True),
    )

    assert projects.count() == 1
    assert projects.first() == private_project


def test_user_and_public_project(
    user,
    public_project,
    private_project,
    query_bus,
):
    """Test empty projects."""
    projects = queries.execute_query(
        Query(user=user, include_public=True),
    )

    assert projects.count() == 1
    assert projects.first() == public_project
