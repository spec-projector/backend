# -*- coding: utf-8 -*-

from apps.core.utils.objects import dict2obj
from apps.users.graphql.types.user import UserType
from apps.users.models import User
from tests.test_users.factories.user import UserFactory


def test_user(user, client):
    client.user = user
    info = dict2obj({'context': client})

    assert user.is_active is True
    assert UserType().get_node(info, user.id) == user


def test_user_inactive(user, client):
    user.is_active = False
    user.save(update_fields=['is_active'])

    client.user = user
    info = dict2obj({'context': client})

    assert UserType().get_node(info, user.id) is None


def test_users(user, client):
    client.user = user
    info = dict2obj({'context': client})

    user_active = UserFactory.create()
    UserFactory.create_batch(3, is_active=False)

    users = UserType().get_queryset(User.objects.all(), info)

    assert users.count() == 2
    assert user in users
    assert user_active in users
