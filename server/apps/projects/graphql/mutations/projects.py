import graphene
from rest_framework.generics import get_object_or_404

from apps.core.graphql.mutations import BaseMutation
from apps.projects.models.project import Project
from apps.projects.graphql.types.project import ProjectType


class CreateProject(BaseMutation):
    class Arguments:
        title = graphene.String()

    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, title):
        project = Project(title=title)
        project.save()

        return CreateProject(project=project)


class UpdateProject(BaseMutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()

    project = graphene.Field(ProjectType)

    @classmethod
    def mutate(cls, root, info, id, title):
        project = get_object_or_404(
            Project.objects.all(),
            pk=id
        )

        project.title = title
        project.save(update_fields=['title'])

        return UpdateProject(project=project)


class DeleteProject(BaseMutation):
    class Arguments:
        id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        project = get_object_or_404(
            Project.objects.all(),
            pk=id
        )

        project.delete()

        return DeleteProject(ok=True)
