# -*- coding: utf-8 -*-

import graphene
from rest_framework.generics import get_object_or_404

from apps.core.graphql.mutations import OldBaseMutation
from apps.projects.models.project import Project


class DeleteProjectMutation(OldBaseMutation):
    class Arguments:
        id = graphene.ID()  # noqa: A003

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):  # noqa: A002
        project = get_object_or_404(Project.objects.all(), pk=id)  # noqa: A003
        project.delete()

        return cls(ok=True)
