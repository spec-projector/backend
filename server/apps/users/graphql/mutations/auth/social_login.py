from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations.command import BaseCommandMutation
from apps.core.logic import commands
from apps.users.logic.commands.auth import social_login
from apps.users.logic.interfaces.social_login import SystemBackend


class SocialLoginMutation(BaseCommandMutation):
    """Login mutation through social."""

    class Arguments:
        system = graphene.Argument(
            graphene.Enum.from_enum(SystemBackend),
            required=True,
        )

    redirect_url = graphene.String()

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Create command."""
        return social_login.SocialLoginCommand(
            request=info.context,
            system=SystemBackend(kwargs["system"]),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: social_login.SocialLoginCommandResult,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "redirect_url": output_dto.redirect_url,
        }
