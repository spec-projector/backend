# -*- coding: utf-8 -*-

from rest_framework import serializers


class LoginMutationInput(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()
