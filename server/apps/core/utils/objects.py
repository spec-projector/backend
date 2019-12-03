# -*- coding: utf-8 -*-

from functools import reduce
from typing import Any, Dict


def deep_getattr(obj: object, attr: str, default: Any = None) -> Any:
    try:
        return reduce(getattr, attr.split('.'), obj)
    except AttributeError:
        return default


class ObjectView(object):
    def __init__(self, source_dict: Dict):
        self.__dict__ = source_dict


def dict2obj(source_dict: Dict) -> ObjectView:
    return ObjectView(source_dict)
