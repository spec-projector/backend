from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.graphql.types import TokenType
from apps.users.logic.use_cases.register import register as register_uc


class RegisterInput(graphene.InputObjectType):
    """User register input."""

    login = graphene.String(required=True)
    email = graphene.String(required=True)
    name = graphene.String(required=True)
    password = graphene.String(required=True)


class RegisterMutation(BaseUseCaseMutation):
    """Register mutation returns token."""

    class Meta:
        use_case_class = register_uc.UseCase

    class Arguments:
        input = graphene.Argument(RegisterInput, required=True)

    token = graphene.Field(TokenType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return register_uc.InputDto(**kwargs["input"])

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: register_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "token": output_dto.token,
        }
