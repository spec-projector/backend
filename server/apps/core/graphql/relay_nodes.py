# -*- coding: utf-8 -*-

from contextlib import suppress

from graphene import relay


class DatasourceRelayNode(relay.Node):
    """Datasource relay node."""

    @classmethod
    def get_node_from_global_id(
            cls,
            info,  # noqa WPS110
            global_id,
            only_type=None,
    ):
        """Get node."""
        with suppress(Exception):
            object_id = cls.from_global_id(global_id)

        if not object_id or not only_type:
            return None

        # We make sure the ObjectType implements the "Node" interface
        if cls not in only_type._meta.interfaces:  # noqa WPS437
            return None

        get_node = getattr(only_type, 'get_node', None)
        if get_node:
            return get_node(info, object_id)

    @classmethod
    def from_global_id(cls, global_id: int) -> int:
        """Returns the type name and ID used to create it."""
        return global_id

    @classmethod
    def to_global_id(cls, obj_type: str, obj_id: int) -> int:
        """Takes a type name and an ID, returns a "global ID"."""
        return obj_id
