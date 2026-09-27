from __future__ import annotations

from typing import Any, Dict, Optional

from .._client import compact
from ._base import Resource


class Senders(Resource):
    def create(self, *, domain_id: int, email: str, name: str, reply_to: Optional[str] = None) -> Dict[str, Any]:
        return self._client.post(
            "/senders",
            compact({"domain_id": domain_id, "email": email, "name": name, "reply_to": reply_to}),
        )

    def list(self) -> Dict[str, Any]:
        return self._client.get("/senders")

    def get(self, id: int) -> Dict[str, Any]:
        return self._client.get(f"/senders/{id}")

    def delete(self, id: int) -> None:
        self._client.delete(f"/senders/{id}")
