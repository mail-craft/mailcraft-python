from __future__ import annotations

from .._client import HttpClient


class Resource:
    def __init__(self, client: HttpClient) -> None:
        self._client = client
