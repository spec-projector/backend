# -*- coding: utf-8 -*-

import graphene


class AssigneeType(graphene.ObjectType):
    """Assignee type."""

    name = graphene.String()
    avatar = graphene.String()

    class Meta:
        name = 'Assignee'
