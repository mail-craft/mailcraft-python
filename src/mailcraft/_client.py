"""The HTTP client shared by every resource."""

from __future__ import annotations

from typing import Any, Dict, Optional

import httpx

from ._version import __version__
from .errors import MailCraftApiError

DEFAULT_BASE_URL = "https://api.mailcraft.host/v1"


class HttpClient:
    """Thin wrapper around ``httpx.Client``. Internal: use the resources on ``MailCraft``."""

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        transport: Optional[httpx.BaseTransport] = None,
    ) -> None:
        if not api_key:
            raise ValueError("MailCraft: an API key is required. Find yours under Settings > API Keys.")

        self._http = httpx.Client(
            base_url=base_url.rstrip("/"),
            timeout=timeout,
            transport=transport,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Accept": "application/json",
                "User-Agent": f"mailcraft-python/{__version__}",
            },
        )

    def get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("GET", path, params=params)

    def post(self, path: str, body: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("POST", path, body=body)

    def patch(self, path: str, body: Optional[Dict[str, Any]] = None) -> Any:
        return self._request("PATCH", path, body=body)

    def delete(self, path: str) -> Any:
        return self._request("DELETE", path)

    def close(self) -> None:
        self._http.close()

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        body: Optional[Dict[str, Any]] = None,
    ) -> Any:
        query = {key: _query_value(value) for key, value in (params or {}).items() if value is not None}

        response = self._http.request(
            method,
            path,
            params=query or None,
            json=body if body is not None else None,
        )

        if response.is_error:
            raise MailCraftApiError.from_response(response)

        if response.status_code == 204 or not response.content:
            return None

        return response.json()


def _query_value(value: Any) -> Any:
    if isinstance(value, bool):
        return "true" if value else "false"
    return value


def compact(params: Dict[str, Any]) -> Dict[str, Any]:
    """Drop keyword arguments that were left as ``None``."""
    return {key: value for key, value in params.items() if value is not None}
