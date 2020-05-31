# -*- coding: utf-8 -*-

import graphene


class AssigneeType(graphene.ObjectType):
    """Assignee type."""

    class Meta:
        name = "Assignee"

    name = graphene.String()
    avatar = graphene.String()
