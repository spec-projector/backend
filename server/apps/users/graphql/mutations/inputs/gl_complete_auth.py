# -*- coding: utf-8 -*-

from rest_framework import serializers


class GitLabCompleteAuthMutationInput(serializers.Serializer):
    code = serializers.CharField()
    state = serializers.CharField()
