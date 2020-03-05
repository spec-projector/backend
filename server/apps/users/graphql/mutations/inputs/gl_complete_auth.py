# -*- coding: utf-8 -*-

from rest_framework import serializers


class GitLabCompleteAuthMutationInput(serializers.Serializer):
    """Gitlab complete auth mutation input."""

    code = serializers.CharField()
    state = serializers.CharField()
