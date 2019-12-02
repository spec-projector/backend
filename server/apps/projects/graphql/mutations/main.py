# -*- coding: utf-8 -*-

from apps.projects.graphql.mutations.projects import (
    CreateProject,
    DeleteProject,
    UpdateProject,
)


class ProjectMutations:
    create_project = CreateProject.Field()
    update_project = UpdateProject.Field()
    delete_project = DeleteProject.Field()
