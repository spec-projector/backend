from rest_framework import status

from apps.projects.models import Project
from tests.base import BaseAPITest
from tests.test_projects.factories import ProjectFactory


class ApiProjectsTests(BaseAPITest):
    def test_unauthorized(self):
        response = self.client.get('/api/projects')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_empty(self):
        self.set_credentials()
        response = self.client.get('/api/projects')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data['count'])

    def test_list(self):
        project = ProjectFactory.create()

        self.set_credentials()
        response = self.client.get('/api/projects')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self._check_project(response.data['results'][0], project)

        ProjectFactory.create_batch(4)

        response = self.client.get('/api/projects')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)

    def test_post(self):
        data = {
            'title': 'new test project'
        }

        self.set_credentials()
        response = self.client.post('/api/projects', data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], data['title'])
        self.assertIsNotNone(response.data['id'])
        self.assertIsNotNone(response.data['created_at'])

        project = Project.objects.first()

        response = self.client.get('/api/projects')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self._check_project(response.data['results'][0], project)

    def _check_project(self, results, project):
        self.assertEqual(results['id'], project.id)
        self.assertEqual(results['title'], project.title)
        self.assertIsNotNone(results['created_at'])