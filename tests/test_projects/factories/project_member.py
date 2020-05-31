# -*- coding: utf-8 -*-

import factory

from apps.projects.models import ProjectMember
from tests.test_projects.factories.project import ProjectFactory
from tests.test_users.factories.user import UserFactory


class ProjectMemberFactory(factory.django.DjangoModelFactory):
    """Project member factory."""

    class Meta:
        model = ProjectMember

    user = factory.SubFactory(UserFactory)
    project = factory.SubFactory(ProjectFactory)
    roles = (
        ProjectMember.roles.BACKEND_DEVELOPER
        | ProjectMember.roles.FRONTEND_DEVELOPER
    )
