from typing import Dict, Optional

import graphene
from graphene_file_upload.scalars import Upload
from graphql import ResolveInfo

from apps.core.graphql.mutations.command import BaseCommandMutation
from apps.core.logic import commands
from apps.users.graphql.types import UserType
from apps.users.logic.commands.me import upload_avatar


class UploadMeAvatarInput(graphene.InputObjectType):
    """User me avatar input."""

    file = graphene.Field(Upload, required=True)  # noqa: WPS110
    left = graphene.Int(required=True)
    top = graphene.Int(required=True)
    width = graphene.Int(required=True)
    height = graphene.Int(required=True)
    scale = graphene.Float(required=True)


class UploadMeAvatarMutation(BaseCommandMutation):
    """Upload me avatar mutation."""

    class Meta:
        auth_required = True

    class Arguments:
        input = graphene.Argument(UploadMeAvatarInput, required=True)

    user = graphene.Field(UserType)

    @classmethod
    def build_command(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        **kwargs,
    ) -> commands.ICommand:
        """Prepare use case input data."""
        return upload_avatar.MeUploadAvatarCommand(
            user=info.context.user,  # type: ignore
            **kwargs["input"],
        )

    @classmethod
    def get_response_data(
        cls,
        root: Optional[object],
        info: ResolveInfo,  # noqa: WPS110
        command_result: upload_avatar.MeUploadAvatarCommandResult,
    ) -> Dict[str, object]:
        """Prepare response data."""
        return {"user": command_result.user}
