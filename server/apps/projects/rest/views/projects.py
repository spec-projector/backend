from rest_framework import mixins

from apps.core.rest.mixins.views import CreateModelMixin, UpdateModelMixin
from apps.core.rest.views import BaseGenericViewSet
from apps.projects.models import Project
from apps.projects.rest.serializers import (
    ProjectSerializer, ProjectCardSerializer, ProjectUpdateSerializer
)


class ProjectsViewset(mixins.ListModelMixin,
                      CreateModelMixin,
                      mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin,
                      UpdateModelMixin,
                      BaseGenericViewSet):
    serializer_classes = {
        'create': ProjectCardSerializer,
        'list': ProjectCardSerializer,
        'partial_update': ProjectSerializer,
        'retrieve': ProjectSerializer,
        'update': ProjectSerializer,
    }
    update_serializer_class = ProjectUpdateSerializer

    queryset = Project.objects.all()
