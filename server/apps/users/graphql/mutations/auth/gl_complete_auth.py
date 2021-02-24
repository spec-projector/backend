from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.graphql.types import TokenType
from apps.users.logic.use_cases.auth import (
    gl_complete_auth as gl_complete_auth_uc,
)


class CompleteGitlabAuthMutation(BaseUseCaseMutation):
    """Complete login mutation after redirection from Gitlab."""

    class Meta:
        use_case_class = gl_complete_auth_uc.UseCase

    class Arguments:
        code = graphene.String(required=True)
        state = graphene.String(required=True)

    token = graphene.Field(TokenType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return gl_complete_auth_uc.InputDto(
            request=info.context,
            **kwargs,
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: gl_complete_auth_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "token": output_dto.token,
        }
