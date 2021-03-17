from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.graphql.types import TokenType
from apps.users.logic.interfaces.social_login import SystemBackend
from apps.users.logic.use_cases.auth import (
    social_complete_login as social_complete_login_uc,
)


class SocialLoginCompleteMutation(BaseUseCaseMutation):
    """Complete login mutation after redirection."""

    class Meta:
        use_case_class = social_complete_login_uc.UseCase

    class Arguments:
        code = graphene.String(required=True)
        state = graphene.String(required=True)
        system = graphene.Argument(
            graphene.Enum.from_enum(SystemBackend),
            required=True,
        )

    token = graphene.Field(TokenType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return social_complete_login_uc.InputDto(
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
        output_dto: social_complete_login_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "token": output_dto.token,
        }