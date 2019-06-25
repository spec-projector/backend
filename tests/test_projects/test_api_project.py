from rest_framework import status

from apps.projects.models import Project
from tests.base import BaseAPITest
from tests.test_projects.factories import ProjectFactory


class ApiProjectTests(BaseAPITest):
    def test_unauthorized(self):
        response = self.client.get('/api/project/1')

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_not_found(self):
        project = ProjectFactory.create()

        self.set_credentials()
        response = self.client.get(f'/api/projects/{project.id + 1}')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_retrieve(self):
        project = ProjectFactory.create()

        self.set_credentials()
        response = self.client.get(f'/api/project/{project.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._check_project(response.data, project)

    def test_patch(self):
        project = ProjectFactory.create()

        data = {
            'title': 'new test project'
        }

        self.set_credentials()
        response = self.client.patch(f'/api/project/{project.id}', data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], data['title'])
        self.assertIsNotNone(response.data['id'])
        self.assertIsNotNone(response.data['created_at'])

        project.refresh_from_db()

        response = self.client.get(f'/api/project/{project.id}')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self._check_project(response.data, project)

    def test_delete(self):
        project = ProjectFactory.create()

        self.set_credentials()
        response = self.client.delete(f'/api/project/{project.id}')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get(f'/api/project/{project.id}')

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertFalse(Project.objects.all())

    def _check_project(self, results, project):
        self.assertEqual(results['id'], project.id)
        self.assertEqual(results['title'], project.title)
        self.assertIsNotNone(results['created_at'])
