# -*- coding: utf-8 -*-

from apps.core.utils.objects import dict2obj
from apps.users.graphql.resolvers import resolve_me_user


def test_me_user(user, client):
    client.user = user
    info = dict2obj({'context': client})

    assert resolve_me_user(None, info) == user
