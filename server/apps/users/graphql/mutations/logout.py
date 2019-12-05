# -*- coding: utf-8 -*-

import graphene

from apps.core.graphql.mutations import OldBaseMutation


class LogoutMutation(OldBaseMutation):
    ok = graphene.Boolean()

    @classmethod
    def do_mutate(cls, root, info):
        info.context.auth.delete()

        return cls(ok=True)
