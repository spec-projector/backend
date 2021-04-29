from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations.command import BaseCommandMutation
from apps.core.logic import commands
from apps.users.graphql.types import TokenType
from apps.users.logic.commands.auth import social_complete_login
from apps.users.logic.interfaces.social_login import SystemBackend


class SocialLoginCompleteMutation(BaseCommandMutation):
    """Complete login mutation after redirection."""

    class Arguments:
        code = graphene.String(required=True)
        state = graphene.String(required=True)
        system = graphene.Argument(
            graphene.Enum.from_enum(SystemBackend),
            required=True,
        )

    token = graphene.Field(TokenType)

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Create command."""
        return social_complete_login.SocialCompleteLoginCommand(
            request=info.context,
            code=kwargs["code"],
            state=kwargs["state"],
            system=SystemBackend(kwargs["system"]),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: social_complete_login.SocialCompleteLoginCommandResult,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "token": output_dto.token,
        }
