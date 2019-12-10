# -*- coding: utf-8 -*-

import json
import re
from typing import Dict, List, Optional

import httpretty
from django.conf import settings
from httpretty.core import HTTPrettyRequest
from rest_framework.status import HTTP_200_OK

RE_GITLAB_URL = re.compile(r'https://gitlab\.com.*')
BASE_GL_API_URL = '{0}/api/v4'.format(settings.GITLAB_HOST)


class _GitlabRequestCallback:
    """Create request callback."""

    def __init__(
        self,
        body: Optional[object] = None,
        status: int = HTTP_200_OK,
    ) -> None:
        self._body = body or {}
        self._status = status

    def __call__(
        self,
        request: HTTPrettyRequest,
        uri: str,
        response_headers: Dict[str, str],
    ) -> List[object]:
        response_headers['Content-Type'] = 'application/json'

        return [self._status, response_headers, json.dumps(self._body)]


class GitlabMock:
    """Gitlab mocker."""

    def __init__(self) -> None:
        assert httpretty.is_enabled()

    def registry_get(
        self,
        path: str,
        body: Optional[object] = None,
        status: int = HTTP_200_OK,
    ) -> None:
        self._registry_url(
            method=httpretty.GET,
            uri=self._prepare_uri(path),
            request_callback=_GitlabRequestCallback(body, status),
            priority=1,
        )

    def _registry_url(
        self,
        method: str,
        uri: str,
        request_callback: _GitlabRequestCallback,
        priority: int = 0,
    ) -> None:
        httpretty.register_uri(
            method=method,
            uri=uri,
            body=request_callback,
            priority=priority,
        )

    def _prepare_uri(self, path: str) -> str:
        return '{0}{1}'.format(BASE_GL_API_URL, path)
