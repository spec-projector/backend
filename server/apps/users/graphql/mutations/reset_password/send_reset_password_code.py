from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.logic.use_cases.reset_password import reset as reset_uc
from apps.users.logic.use_cases.reset_password import (
    send_password_reset as send_reset_uc,
)


class SendPasswordResetSecurityCodeInput(graphene.InputObjectType):
    """Input restore password."""

    email = graphene.String(required=True)


class SendPasswordResetSecurityCodeMutation(BaseUseCaseMutation):
    """Send password reset mutation."""

    class Meta:
        use_case_class = send_reset_uc.UseCase

    class Arguments:
        input = graphene.Argument(
            SendPasswordResetSecurityCodeInput,
            required=True,
        )

    ok = graphene.Boolean()

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        input_data = kwargs["input"]
        return send_reset_uc.InputDto(email=input_data["email"])

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: reset_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {"ok": True}
