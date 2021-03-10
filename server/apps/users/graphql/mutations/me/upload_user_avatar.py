from typing import Dict, Optional

import graphene
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo

from apps.core.graphql.mutations import BaseUseCaseMutation
from apps.users.graphql.mutations.me.errors import UserNotExistsError
from apps.users.graphql.types import UserType
from apps.users.logic.use_cases.me import upload_image as upload_image_uc
from apps.users.models import User


class UploadUserAvatarInput(graphene.InputObjectType):
    """User user avatar input."""

    user = graphene.Int(required=True)
    file = graphene.Field(Upload, required=True)  # noqa: WPS110
    left = graphene.Int(required=True)
    top = graphene.Int(required=True)
    width = graphene.Int(required=True)
    height = graphene.Int(required=True)
    scale = graphene.Float(required=True)


class UploadUserAvatarMutation(BaseUseCaseMutation):
    """Upload user avatar mutation."""

    class Meta:
        use_case_class = upload_image_uc.UseCase
        auth_required = True

    class Arguments:
        input = graphene.Argument(UploadUserAvatarInput, required=True)

    user = graphene.Field(UserType)

    @classmethod
    def get_input_dto(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ):
        """Prepare use case input data."""
        input_data = kwargs["input"]
        try:
            user = User.objects.get(id=input_data.pop("user"))
        except User.DoesNotExist:
            raise UserNotExistsError()

        return upload_image_uc.InputDto(user=user, **input_data)

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        output_dto: upload_image_uc.OutputDto,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {"user": output_dto.user}
