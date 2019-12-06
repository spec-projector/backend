# -*- coding: utf-8 -*-

from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import SerializerMutation
from apps.core.graphql.mutations.helpers.persisters import (
    update_from_validated_data,
)
from apps.projects.graphql.mutations.projects.inputs import UpdateProjectInput
from apps.projects.graphql.types.project import ProjectType


class UpdateProjectMutation(SerializerMutation):
    class Meta:
        serializer_class = UpdateProjectInput

    project = graphene.Field(ProjectType)

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,
        validated_data: Dict[str, object],
    ) -> 'UpdateProjectMutation':
        project = validated_data.pop('project')

        update_from_validated_data(project, validated_data)

        return cls(project=project)
