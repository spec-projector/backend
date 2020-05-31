# -*- coding: utf-8 -*-

import graphene

from apps.projects.graphql.types import AssigneeType


class IssueType(graphene.ObjectType):
    """Issue type."""

    class Meta:
        name = "Issue"

    title = graphene.String()
    state = graphene.String()
    due_date = graphene.String()
    spent = graphene.Float()
    assignee = graphene.Field(AssigneeType)
