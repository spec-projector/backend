from typing import Dict, Optional

import graphene
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.logic.use_cases.auth import gl_login as gl_login_uc


class LoginGitlabMutation(BaseUseCaseMutation):
    """Login mutation through Gitlab returns url."""

    class Meta:
        use_case_class = gl_login_uc.UseCase

    redirect_url = graphene.String()

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return gl_login_uc.InputDto(
            request=info.context,
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: gl_login_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {
            "redirect_url": output_dto.redirect_url,
        }
