# -*- coding: utf-8 -*-

import graphene

from apps.projects.graphql.types import AssigneeType


class IssueType(graphene.ObjectType):
    """Issue type."""

    title = graphene.String()
    state = graphene.String()
    due_date = graphene.String()
    spent = graphene.Int()
    assignee = graphene.Field(AssigneeType)

    class Meta:
        name = 'Issue'
