from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.graphql.types import TokenType
from apps.users.logic.use_cases.auth import login as login_uc


class LoginMutation(BaseUseCaseMutation):
    """Login mutation returns token."""

    class Meta:
        use_case_class = login_uc.UseCase

    class Arguments:
        login = graphene.String(required=True)
        password = graphene.String(required=True)

    token = graphene.Field(TokenType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return login_uc.InputDto(
            username=kwargs["login"],
            password=kwargs["password"],
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: login_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "token": output_dto.token,
        }
