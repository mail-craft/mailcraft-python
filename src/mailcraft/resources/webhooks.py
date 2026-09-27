from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._client import compact
from ._base import Resource


class Webhooks(Resource):
    def create(self, *, url: str, events: List[str], description: Optional[str] = None) -> Dict[str, Any]:
        return self._client.post("/webhooks", compact({"url": url, "events": events, "description": description}))

    def list(self) -> Dict[str, Any]:
        return self._client.get("/webhooks")

    def delete(self, id: int) -> None:
        self._client.delete(f"/webhooks/{id}")
