# -*- coding: utf-8 -*-

from rest_framework import serializers

from apps.projects.models import Project


class DeleteProjectInput(serializers.Serializer):
    project = serializers.PrimaryKeyRelatedField(queryset=Project.objects.all())
