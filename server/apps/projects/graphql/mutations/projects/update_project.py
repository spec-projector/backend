# -*- coding: utf-8 -*-

import graphene
from rest_framework.generics import get_object_or_404

from apps.core.graphql.mutations import OldBaseMutation
from apps.projects.graphql.types.project import ProjectType
from apps.projects.models.project import Project


class UpdateProjectMutation(OldBaseMutation):
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
