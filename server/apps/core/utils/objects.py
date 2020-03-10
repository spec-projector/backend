# -*- coding: utf-8 -*-

from functools import reduce
from typing import Dict, Optional


def deep_getattr(
    instance: object, attr: str, default: Optional[object] = None,
) -> Optional[object]:
    """Deeping get object attribute."""
    try:
        return reduce(getattr, attr.split("."), instance)
    except AttributeError:
        return default


class _ObjectView:
    def __init__(self, source_dict: Dict[str, object]):
        """Initializing."""
        self.__dict__ = source_dict


def dict2obj(source_dict: Dict[str, object]) -> _ObjectView:
    """Convert dictionary to object."""
    return _ObjectView(source_dict)
