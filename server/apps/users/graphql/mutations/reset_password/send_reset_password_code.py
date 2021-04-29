from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseCommandMutation
from apps.core.logic import commands
from apps.users.logic.commands.reset_password import send_password_reset


class SendPasswordResetSecurityCodeInput(graphene.InputObjectType):
    """Input restore password."""

    email = graphene.String(required=True)


class SendPasswordResetSecurityCodeMutation(BaseCommandMutation):
    """Send password reset mutation."""

    class Arguments:
        input = graphene.Argument(
            SendPasswordResetSecurityCodeInput,
            required=True,
        )

    ok = graphene.Boolean()

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Build command."""
        input_data = kwargs["input"]
        return send_password_reset.SendPasswordResetCommand(
            email=input_data["email"],
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
