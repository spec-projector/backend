# -*- coding: utf-8 -*-

from functools import reduce
from typing import Dict, Optional


def deep_getattr(
    instance: object,
    attr: str,
    default: Optional[object] = None,
) -> Optional[object]:
    try:
        return reduce(getattr, attr.split('.'), instance)
    except AttributeError:
        return default


class ObjectView:
    def __init__(self, source_dict: Dict[str, object]):
        self.__dict__ = source_dict


def dict2obj(source_dict: Dict[str, object]) -> ObjectView:
    return ObjectView(source_dict)
