from __future__ import annotations

from typing import Any, Dict, Optional

from .._client import compact
from ._base import Resource


class Segments(Resource):
    def create(self, *, name: str, filters: Dict[str, Any], description: Optional[str] = None) -> Dict[str, Any]:
        return self._client.post("/segments", compact({"name": name, "description": description, "filters": filters}))

    def list(self) -> Dict[str, Any]:
        return self._client.get("/segments")

    def get(self, id: int) -> Dict[str, Any]:
        return self._client.get(f"/segments/{id}")

    def delete(self, id: int) -> None:
        self._client.delete(f"/segments/{id}")
