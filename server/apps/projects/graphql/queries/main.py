# -*- coding: utf-8 -*-

from apps.projects.graphql.queries import issues, projects


class ProjectsQueries(
    issues.IssuesQueries, projects.ProjectsQueries,
):
    """All projects queries."""
