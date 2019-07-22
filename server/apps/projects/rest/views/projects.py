from rest_framework import mixins

from apps.core.rest.mixins.views import CreateModelMixin, UpdateModelMixin
from apps.core.rest.views import BaseGenericViewSet
from apps.projects.models import Project
from apps.projects.rest.serializers import (
    ProjectSerializer, ProjectCardSerializer, ProjectUpdateSerializer
)


class ProjectViewset(mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     UpdateModelMixin,
                     BaseGenericViewSet):
    serializer_classes = {
        'retrieve': ProjectSerializer,
        'update': ProjectSerializer,
        'partial_update': ProjectSerializer,
    }
    update_serializer_class = ProjectUpdateSerializer

    queryset = Project.objects.all()


class ProjectsViewset(mixins.ListModelMixin,
                      CreateModelMixin,
                      BaseGenericViewSet):
    serializer_classes = {
        'create': ProjectCardSerializer,
        'list': ProjectCardSerializer,
    }
    update_serializer_class = ProjectUpdateSerializer

    queryset = Project.objects.all()
