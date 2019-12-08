# -*- coding: utf-8 -*-

from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import SerializerMutation
from apps.projects.graphql.mutations.projects.inputs import CreateProjectInput
from apps.projects.graphql.types.project import ProjectType
from apps.projects.models.project import Project


class CreateProjectMutation(SerializerMutation):
    project = graphene.Field(ProjectType)

    class Meta:
        serializer_class = CreateProjectInput

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        validated_data: Dict[str, str],
    ) -> 'CreateProjectMutation':
        project = Project.objects.create(
            title=validated_data['title'],
            owner=info.context.user,
        )

        return cls(project=project)
