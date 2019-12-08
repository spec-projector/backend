# -*- coding: utf-8 -*-

import graphene
from graphql import ResolveInfo

from apps.projects.graphql.types import IssueType
from apps.projects.services.issues.retriever import System, get_issue


class IssuesQueries(graphene.ObjectType):
    """Issue queries."""

    issue = graphene.Field(
        IssueType,
        url=graphene.String(required=True),
        token=graphene.String(required=True),
        system=graphene.Enum.from_enum(System)(required=True),
    )

    def resolve_issue(
        self,
        info: ResolveInfo,  # noqa: WPS110
        url: str,
        token: str,
        system: System,
    ) -> IssueType:
        return get_issue(url, token, system)
