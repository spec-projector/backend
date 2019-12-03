# -*- coding: utf-8 -*-

import factory

from apps.projects.models import Project
from tests.test_users.factories.user import UserFactory


class ProjectFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda index: 'Project {0}'.format(index))
    owner = factory.SubFactory(UserFactory)

    class Meta:
        model = Project
