# -*- coding: utf-8 -*-

from apps.projects.graphql.mutations import projects


class ProjectsMutations:
    create_project = projects.CreateProjectMutation.Field()
    update_project = projects.UpdateProjectMutation.Field()
    delete_project = projects.DeleteProjectMutation.Field()
