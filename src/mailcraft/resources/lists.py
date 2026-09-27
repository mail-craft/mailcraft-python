from __future__ import annotations

from typing import Any, Dict, Optional

from .._client import compact
from ._base import Resource


class Lists(Resource):
    def create(
        self,
        *,
        name: str,
        description: Optional[str] = None,
        type: Optional[str] = None,
        segment_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create a list. ``type`` is ``"static"`` or ``"dynamic"`` (with a ``segment_id``)."""
        return self._client.post(
            "/lists",
            compact({"name": name, "description": description, "type": type, "segment_id": segment_id}),
        )

    def list(self) -> Dict[str, Any]:
        return self._client.get("/lists")

    def get(self, id: int) -> Dict[str, Any]:
        return self._client.get(f"/lists/{id}")

    def delete(self, id: int) -> None:
        self._client.delete(f"/lists/{id}")
