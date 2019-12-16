# -*- coding: utf-8 -*-

from dataclasses import dataclass
from typing import Optional

from apps.projects.services.issues.meta import AssigneeMeta


@dataclass
class IssueMeta:
    """Issue meta."""

    title: str
    state: str
    due_date: Optional[str]
    spent: Optional[int]
    assignee: Optional[AssigneeMeta]
