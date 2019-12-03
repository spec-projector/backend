# -*- coding: utf-8 -*-

import factory

from apps.projects.models import Project


class ProjectFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda index: 'Project {0}'.format(index))

    class Meta:
        model = Project
