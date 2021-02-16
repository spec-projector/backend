import factory

from apps.projects.models import GitHubIntegration
from tests.test_projects.factories.project import ProjectFactory


class GitHubIntegrationFactory(factory.django.DjangoModelFactory):
    """GitHub integration factory."""

    class Meta:
        model = GitHubIntegration

    project = factory.SubFactory(ProjectFactory)
    token = factory.Sequence(lambda index: "github_{0}".format(index))
