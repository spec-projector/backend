from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.core.logic import commands
from apps.users.graphql.types import TokenType
from apps.users.logic.commands.reset_password import reset


class ResetPasswordInput(graphene.InputObjectType):
    """Input restore password."""

    email = graphene.String(required=True)
    code = graphene.String(required=True)
    password = graphene.String(required=True)


class ResetPasswordMutation(BaseCommandMutation):
    """Reset password mutation."""

    class Arguments:
        input = graphene.Argument(ResetPasswordInput, required=True)

    token = graphene.Field(TokenType)

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Build command."""
        input_data = kwargs["input"]
        return reset.Command(
            email=input_data["email"],
            code=input_data["code"],
            password=input_data["password"],
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result: reset.CommandResult,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "token": command_result.token,
        }
