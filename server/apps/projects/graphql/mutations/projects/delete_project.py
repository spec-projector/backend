# -*- coding: utf-8 -*-

from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import SerializerMutation
from apps.projects.graphql.mutations.projects.inputs import DeleteProjectInput
from apps.projects.models import Project


class DeleteProjectMutation(SerializerMutation):
    status = graphene.String()

    class Meta:
        serializer_class = DeleteProjectInput

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,
        validated_data: Dict[str, Project],
    ) -> 'DeleteProjectMutation':
        validated_data['project'].delete()

        return cls(status='success')
