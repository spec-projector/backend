from typing import Optional

from django.http import HttpRequest
from graphene.test import Client

from apps.users.models import Token, User
from apps.users.services.token import create_user_token
from gql import schema


class GraphQLRequestFactory(Client):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(schema, *args, **kwargs)

        self._user: Optional[User] = None
        self._token: Optional[Token] = None

    def set_user(self, user: User, token: Optional[Token] = None) -> None:
        """Set user for auth requests."""
        self._user = user

        if token is None:
            token = create_user_token(user)

        self._token = token

    def _auth_if_need(self, request: HttpRequest) -> None:
        if not self._token:
            return

        request.META.update(
            HTTP_AUTHORIZATION='Bearer {}'.format(self._token.key),
        )
