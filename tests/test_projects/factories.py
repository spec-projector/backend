# -*- coding: utf-8 -*-

import factory

from apps.projects.models import Project


class ProjectFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: 'Project {0}'.format(n))

    class Meta:
        model = Project
