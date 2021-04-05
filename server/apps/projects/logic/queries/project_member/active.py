from dataclasses import dataclass
from typing import Optional

from django.db import models

from apps.core.logic.queries import BaseQuery
from apps.projects.models import Project, ProjectMember


@dataclass(frozen=True)
class InputDto:
    """Get users query input data."""

    project: Project
    queryset: Optional[models.QuerySet] = None


class Query(BaseQuery):
    """Active project members."""

    def execute(self, input_dto: InputDto) -> models.QuerySet:
        """Handler."""
        members = input_dto.queryset
        if members is None:
            members = ProjectMember.objects.all()

        return members.filter(
            project=input_dto.project,
            user__is_active=True,
        )
