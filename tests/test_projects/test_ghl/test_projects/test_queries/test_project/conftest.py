import pytest

from apps.projects.models import Project, ProjectMember
from apps.projects.models.enums import ProjectMemberRole
from tests.test_projects.factories import ProjectFactory, ProjectMemberFactory


@pytest.fixture()
def project(db):
    """Create project."""
    return ProjectFactory.create(
        is_public=True,
        public_permissions=Project.public_permissions.EDIT_FEATURES,
    )


@pytest.fixture()
def project_member(user, project):
    """Create project member."""
    return ProjectMemberFactory.create(
        user=user,
        project=project,
        role=ProjectMemberRole.VIEWER,
        permissions=ProjectMember.permissions.EDIT_FEATURE_API,
    )
