# -*- coding: utf-8 -*-

import graphene
from rest_framework.generics import get_object_or_404

from apps.core.graphql.mutations import BaseMutation
from apps.projects.graphql.types.project import ProjectType
from apps.projects.models.project import Project


class CreateProject(BaseMutation):
    class Arguments:
        title = graphene.String()

    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, title):
        project = Project(title=title)
        project.save()

        return cls(project=project)


class UpdateProject(BaseMutation):
    class Arguments:
        id = graphene.ID()  # noqa: A003
        title = graphene.String()

    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, id, title):  # noqa: A002
        project = get_object_or_404(Project.objects.all(), pk=id)  # noqa: A003
        project.title = title
        project.save(update_fields=['title'])

        return cls(project=project)


class DeleteProject(BaseMutation):
    class Arguments:
        id = graphene.ID()  # noqa: A003

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):  # noqa: A002
        project = get_object_or_404(Project.objects.all(), pk=id)  # noqa: A003
        project.delete()

        return cls(ok=True)
