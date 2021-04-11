from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations.command import BaseCommandMutation
from apps.users.graphql.types import TokenType
from apps.users.logic.commands.auth import login


class LoginInput(graphene.InputObjectType):
    """User login input."""

    email = graphene.String(required=True)
    password = graphene.String(required=True)


class LoginMutation(BaseCommandMutation):
    """Login mutation returns token."""

    class Arguments:
        input = graphene.Argument(LoginInput, required=True)

    token = graphene.Field(TokenType)

    @classmethod
    def get_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Create command."""
        return login.Command(**kwargs["input"])

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result: login.CommandResult,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "token": command_result.token,
        }
