from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.core.logic import commands
from apps.users.graphql.types import UserAccessTokenCreatedType
from apps.users.logic.commands.user_access_token import add_access_token


class AddUserAccessTokenMutation(BaseCommandMutation):
    """Add user access token mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        name = graphene.String(required=True)

    access_token = graphene.Field(UserAccessTokenCreatedType)

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Build command."""
        return add_access_token.Command(
            user=info.context.user,  # type: ignore
            data=add_access_token.UserAccessTokenDto(name=kwargs.get("name")),
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result: add_access_token.CommandResult,
    ) -> Dict["str", object]:
        """Prepare response data."""
        user_access_token = command_result.access_token
        return {
            "access_token": {
                "id": user_access_token.id,
                "name": user_access_token.name,
                "key": user_access_token.key,
                "createdAt": user_access_token.created_at,
            },
        }
