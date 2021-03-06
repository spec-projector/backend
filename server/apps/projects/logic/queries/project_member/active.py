from dataclasses import dataclass
from typing import Optional

from django.db import models

from apps.core.logic import queries
from apps.projects.models import Project, ProjectMember


@dataclass(frozen=True)
class Query(queries.IQuery):
    """Get users query input data."""

    project: Project
    queryset: Optional[models.QuerySet] = None


class QueryHandler(queries.IQueryHandler[Query, models.QuerySet]):
    """Active project members."""

    def ask(self, query: Query) -> models.QuerySet:
        """Handler."""
        members = query.queryset
        if members is None:
            members = ProjectMember.objects.all()

        return members.filter(
            project=query.project,
            user__is_active=True,
        )
