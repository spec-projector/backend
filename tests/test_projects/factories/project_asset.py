import factory

from apps.projects.models import ProjectAsset, ProjectAssetSource
from tests.test_projects.factories.project import ProjectFactory


class ProjectAssetFactory(factory.django.DjangoModelFactory):
    """Project asset factory."""

    class Meta:
        model = ProjectAsset

    project = factory.SubFactory(ProjectFactory)
    source = ProjectAssetSource.FIGMA
    file = factory.django.FileField(filename="file.dat")  # noqa: WPS110
