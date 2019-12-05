# -*- coding: utf-8 -*-

from apps.users.graphql.mutations.gl_complete_auth import (
    GitLabCompleteAuthMutation,
)
from apps.users.graphql.mutations.gl_login import GitLabLoginMutation
from apps.users.graphql.mutations.login import LoginMutation
from apps.users.graphql.mutations.logout import LogoutMutation


class AuthMutations:
    complete_gitlab_auth = GitLabCompleteAuthMutation.Field()
    login_gitlab = GitLabLoginMutation.Field()
    login = LoginMutation.Field()
    logout = LogoutMutation.Field()
