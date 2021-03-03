from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.graphql.types import TokenType
from apps.users.logic.use_cases.reset_password import reset as reset_uc


class ResetPasswordInput(graphene.InputObjectType):
    """Input restore password."""

    email = graphene.String(required=True)
    code = graphene.String(required=True)
    password = graphene.String(required=True)


class ResetPasswordMutation(BaseUseCaseMutation):
    """Reset password mutation."""

    class Meta:
        use_case_class = reset_uc.UseCase

    class Arguments:
        input = graphene.Argument(ResetPasswordInput, required=True)

    token = graphene.Field(TokenType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        input_data = kwargs["input"]
        return reset_uc.InputDto(
            email=input_data["email"],
            code=input_data["code"],
            password=input_data["password"],
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: reset_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "token": output_dto.token,
        }
