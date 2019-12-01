from typing import Dict

from rest_framework.test import APIRequestFactory

from apps.users.services.token import create_user_token


class MockStorageMessages:
    def add(self, level, message, extra_tags):
        return


class Client:
    def __init__(self, user=None) -> None:
        self.user = user
        self._factory = APIRequestFactory()
        self._credentials: Dict[str, str] = {}

    def get(self, url, data=None, **extra):
        request = self._factory.get(url, data, **extra)
        request.user = self.user
        request.META.update(**self._credentials)

        return request

    def post(self, url, data, **extra):
        request = self._factory.post(url, data, **extra)
        request.user = self.user
        request.META.update(**self._credentials)

        if self.user and self.user.is_superuser:
            request._messages = MockStorageMessages()

        return request

    def put(self, url, data, **extra):
        request = self._factory.put(url, data, **extra)
        request.user = self.user
        request.META.update(**self._credentials)

        return request

    def patch(self, url, data, **extra):
        request = self._factory.patch(url, data, **extra)
        request.user = self.user
        request.META.update(**self._credentials)

        return request

    def delete(self, url, data, **extra):
        request = self._factory.delete(url, data, **extra)
        request.user = self.user
        request.META.update(**self._credentials)

        return request

    def set_credentials(self, user=None, token=None):
        if not user:
            user = self.user

        if token is None:
            token = create_user_token(user)

        self._credentials = {
            'HTTP_AUTHORIZATION': f'Bearer {token.key}',
        }
