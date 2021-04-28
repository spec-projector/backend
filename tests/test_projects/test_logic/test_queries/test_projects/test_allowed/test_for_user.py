import pytest

from apps.projects.logic.queries.project import ListAllowedProjectsQuery
from tests.test_projects.factories.project import ProjectFactory
from tests.test_projects.factories.project_member import ProjectMemberFactory


@pytest.fixture(params=[True, False])
def project(db, request):
    """Create project."""
    return ProjectFactory.create(is_public=request.param)


@pytest.fixture()
def project_member(user, project):
    """Create project member."""
    return ProjectMemberFactory.create(user=user, project=project)


def test_not_projects(user, project, query_bus):
    """Test empty projects."""
    projects = query_bus.dispatch(ListAllowedProjectsQuery(user=user))
    assert not projects.exists()


def test_projects_as_owner(user, project, query_bus):
    """Test empty projects."""
    project.owner = user
    project.save()

    projects = query_bus.dispatch(ListAllowedProjectsQuery(user=user))

    assert projects.count() == 1
    assert projects.first() == project


def test_projects_as_project_member(user, project_member, query_bus):
    """Test empty projects."""
    projects = query_bus.dispatch(ListAllowedProjectsQuery(user=user))

    assert projects.count() == 1
    assert projects.first() == project_member.project
