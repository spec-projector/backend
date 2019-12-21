# -*- coding: utf-8 -*-

from rest_framework import serializers


class CreateProjectInput(serializers.Serializer):
    title = serializers.CharField()
