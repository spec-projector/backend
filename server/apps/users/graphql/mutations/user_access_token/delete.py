from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.core.logic import commands
from apps.users.logic.commands.user_access_token import delete_access_token


class DeleteUserAccessTokenMutation(BaseCommandMutation):
    """Delete user access token mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        id = graphene.ID(required=True)

    status = graphene.String()

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Build command."""
        return delete_access_token.Command(
            user=info.context.user,  # type: ignore
            data=delete_access_token.DeleteUserAccessTokenDto(
                id=kwargs.get("id"),
            ),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "status": "success",
        }
