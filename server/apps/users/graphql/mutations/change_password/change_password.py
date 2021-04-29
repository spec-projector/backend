from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.core.logic import commands
from apps.users.logic.commands import change_password


class ChangePasswordInput(graphene.InputObjectType):
    """Input change password."""

    password = graphene.String(required=True)


class ChangePasswordMutation(BaseCommandMutation):
    """Change password mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        input = graphene.Argument(ChangePasswordInput, required=True)

    ok = graphene.Boolean()

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Create command."""
        return change_password.ChangePasswordCommand(
            password=kwargs["input"]["password"],
            user=info.context.user,  # type: ignore
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {"ok": True}
