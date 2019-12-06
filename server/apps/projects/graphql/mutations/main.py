# -*- coding: utf-8 -*-

from apps.projects.graphql.mutations.projects import (
    CreateProjectMutation,
    DeleteProjectMutation,
    UpdateProjectMutation,
)


class ProjectsMutations:
    create_project = CreateProjectMutation.Field()
    update_project = UpdateProjectMutation.Field()
    delete_project = DeleteProjectMutation.Field()
