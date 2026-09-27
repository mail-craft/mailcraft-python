from __future__ import annotations

from typing import Any, Dict, List, Optional, Union

from .._client import compact
from ._base import Resource


class Emails(Resource):
    def send(
        self,
        *,
        from_: str,
        to: Union[str, List[str]],
        subject: str,
        html: Optional[str] = None,
        text: Optional[str] = None,
        cc: Optional[List[str]] = None,
        bcc: Optional[List[str]] = None,
        reply_to: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
        tags: Optional[List[str]] = None,
        **extra: Any,
    ) -> Dict[str, Any]:
        """Send a transactional email. ``from_`` is sent as ``from`` (a Python keyword)."""
        return self._client.post(
            "/emails",
            compact(
                {
                    "from": from_,
                    "to": [to] if isinstance(to, str) else to,
                    "subject": subject,
                    "html": html,
                    "text": text,
                    "cc": cc,
                    "bcc": bcc,
                    "reply_to": reply_to,
                    "headers": headers,
                    "tags": tags,
                    **extra,
                }
            ),
        )

    def list(self, *, limit: Optional[int] = None) -> Dict[str, Any]:
        return self._client.get("/emails", {"limit": limit})

    def get(self, id: str) -> Dict[str, Any]:
        return self._client.get(f"/emails/{id}")

    def validate(self, email: str) -> Dict[str, Any]:
        return self._client.get("/emails/validate", {"email": email})
