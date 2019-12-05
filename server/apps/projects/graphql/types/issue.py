# -*- coding: utf-8 -*-

import graphene


class IssueType(graphene.ObjectType):
    """Issue type."""

    title = graphene.String()
    status = graphene.String()

    class Meta:
        name = 'Issue'
