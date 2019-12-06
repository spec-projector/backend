# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.projects.models import Project


class UpdateProjectInput(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
    title = serializers.CharField(required=False)
    description = serializers.CharField(required=False)
