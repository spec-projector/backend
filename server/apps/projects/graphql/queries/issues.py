# -*- coding: utf-8 -*-

import graphene
from graphql import ResolveInfo

from apps.projects.graphql.types import AssigneeType, IssueType
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
        issue_meta = get_issue(url, token, system)

        assignee = None

        if issue_meta.assignee:
            assignee = AssigneeType(
                name=issue_meta.assignee.name,
                avatar=issue_meta.assignee.avatar,
            )

        return IssueType(
            title=issue_meta.title,
            state=issue_meta.state.upper() if issue_meta.state else None,
            due_date=issue_meta.due_date,
            spent=issue_meta.spent,
            assignee=assignee,
        )
