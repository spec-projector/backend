# -*- coding: utf-8 -*-

import re
from collections import OrderedDict
from typing import Dict, Optional

import graphene
from graphene.types.mutation import MutationOptions
from graphene.types.utils import yank_fields_from_attrs
from graphene_django.rest_framework.mutation import fields_for_serializer
from graphene_django.types import ErrorType
from graphql import ResolveInfo
from rest_framework.exceptions import PermissionDenied

from apps.core.graphql.security.mixins.mutation import AuthMutation
from apps.core.graphql.security.permissions import AllowAuthenticated


class SerializerMutationOptions(MutationOptions):
    serializer_class = None


class SerializerMutation(AuthMutation, graphene.Mutation):
    permission_classes = (AllowAuthenticated,)

    errors = graphene.List(
        ErrorType,
        description='May contain more than one error for same field.',
    )

    class Meta:
        abstract = True

    @classmethod
    def __init_subclass_with_meta__(
        cls,
        serializer_class=None,
        only_fields=(),
        exclude_fields=(),
        **options,
    ):
        if not serializer_class:
            raise Exception(
                'serializer_class is required for the SerializerMutation',
            )

        serializer = serializer_class()

        input_fields = fields_for_serializer(
            serializer,
            only_fields,
            exclude_fields,
            is_input=True,
        )

        input_fields = yank_fields_from_attrs(
            input_fields,
            _as=graphene.InputField,
        )

        base_name = re.sub('Payload$', '', cls.__name__)

        if not input_fields:
            input_fields = {}

        cls.Input = type(
            '{0}Input'.format(base_name),
            (graphene.InputObjectType,),
            OrderedDict(input_fields),
        )

        arguments = OrderedDict(
            input=cls.Input(required=True),
        )

        meta_options = SerializerMutationOptions(cls)
        meta_options.serializer_class = serializer_class

        super().__init_subclass_with_meta__(
            output=None,
            arguments=arguments,
            name='{0}Payload'.format(base_name),
            _meta=meta_options,
            **options,
        )

    @classmethod
    def mutate(cls, root, info, input):  # noqa: A002
        cls.check_premissions(root, info, input)

        return cls.mutate_and_get_payload(root, info, **input)

    @classmethod
    def check_premissions(cls, root, info, input) -> None:  # noqa: A002
        if not cls.has_permission(root, info, input=input):
            raise PermissionDenied()

    @classmethod
    def mutate_and_get_payload(
        cls,
        root: Optional[object],
        info: ResolveInfo,
        **input,
    ) -> 'SerializerMutation':
        kwargs = cls.get_serializer_kwargs(root, info, **input)
        serializer = cls._meta.serializer_class(**kwargs)

        if serializer.is_valid():
            return cls.perform_mutate(
                root,
                info,
                serializer.validated_data,
            )

        return cls(
            errors=ErrorType.from_errors(serializer.errors),
        )

    @classmethod
    def get_serializer_kwargs(
        cls,
        root: Optional[object],
        info: ResolveInfo,
        **input,
    ) -> Dict[str, object]:
        return {
            'data': input,
            'context': {
                'request': info.context,
            },
        }

    @classmethod
    def perform_mutate(
        cls,
        root: Optional[object],
        info: ResolveInfo,
        validated_data: Dict[str, object],
    ) -> 'SerializerMutation':
        raise NotImplementedError