# -*- coding: utf-8 -*-

from tests.test_projects.factories.project import ProjectFactory

GHL_QUERY_ALL_PROJECTS = """
query {
  allProjects {
    count
    edges{
      node{
        id
      }
    }
  }
}
"""


def test_query(user, ghl_client):
    """Test getting all projects query."""
    ghl_client.set_user(user)

    ProjectFactory.create_batch(5)

    result = ghl_client.execute(GHL_QUERY_ALL_PROJECTS)

    assert 'errors' not in result
    assert result['data']['allProjects']['count'] == 5
