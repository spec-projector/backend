# -*- coding: utf-8 -*-

from typing import Optional

from graphql import ResolveInfo


def resolve_me_user(
    root: Optional[object],
    info: ResolveInfo,  # noqa: WPS110
):
    """Resolves current context user."""
    return info.context.user  # type: ignore
