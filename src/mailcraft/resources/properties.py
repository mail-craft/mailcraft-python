from __future__ import annotations

from typing import Any, Dict, Optional

from .._client import compact
from ._base import Resource


class Properties(Resource):
    def create(self, *, key: str, label: str, type: str, default_value: Optional[Any] = None) -> Dict[str, Any]:
        """Create a custom contact property. ``type`` is text, number, boolean, date or list."""
        return self._client.post(
            "/properties",
            compact({"key": key, "label": label, "type": type, "default_value": default_value}),
        )

    def list(self) -> Dict[str, Any]:
        return self._client.get("/properties")

    def delete(self, id: int) -> None:
        self._client.delete(f"/properties/{id}")
