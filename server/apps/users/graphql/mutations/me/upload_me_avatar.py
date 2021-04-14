from typing import Dict, Optional

import graphene
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.graphql.types import UserType
from apps.users.logic.use_cases.me import upload_image as upload_image_uc


class UploadMeAvatarInput(graphene.InputObjectType):
    """User me avatar input."""

    file = graphene.Field(Upload, required=True)  # noqa: WPS110
    left = graphene.Int(required=True)
    top = graphene.Int(required=True)
    width = graphene.Int(required=True)
    height = graphene.Int(required=True)
    scale = graphene.Float(required=True)


class UploadMeAvatarMutation(BaseUseCaseMutation):
    """Upload me avatar mutation."""

    class Meta:
        use_case_class = upload_image_uc.UseCase
        auth_required = True

    class Arguments:
        input = graphene.Argument(UploadMeAvatarInput, required=True)

    user = graphene.Field(UserType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        return upload_image_uc.InputDto(
            user=info.context.user,  # type: ignore
            **kwargs["input"],
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: upload_image_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {"user": output_dto.user}
