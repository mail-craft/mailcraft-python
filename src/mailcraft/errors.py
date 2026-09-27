"""Errors raised by the MailCraft client."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

import httpx


class MailCraftApiError(Exception):
    """Raised for any non-2xx response from the MailCraft API.

    Covers both error shapes the API returns:

    - ``{"error": {"type": "...", "message": "..."}}`` for business-rule
      failures (plan limits, suppressed recipients, ...).
    - ``{"message": "...", "errors": {"field": ["..."]}}`` for validation
      failures (422 responses).
    """

    def __init__(
        self,
        status: int,
        message: str,
        *,
        type: Optional[str] = None,
        errors: Optional[Dict[str, List[str]]] = None,
    ) -> None:
        super().__init__(message)
        self.status = status
        self.message = message
        self.type = type
        self.errors = errors

    @classmethod
    def from_response(cls, response: httpx.Response) -> "MailCraftApiError":
        try:
            body: Any = response.json()
        except ValueError:
            body = None

        if isinstance(body, dict) and isinstance(body.get("error"), dict):
            error = body["error"]
            return cls(
                response.status_code,
                error.get("message") or response.reason_phrase,
                type=error.get("type"),
            )

        if isinstance(body, dict) and "message" in body:
            return cls(response.status_code, body["message"], errors=body.get("errors"))

        return cls(response.status_code, response.reason_phrase or "Request failed")

    def __repr__(self) -> str:
        return f"MailCraftApiError(status={self.status}, message={self.message!r}, type={self.type!r})"
