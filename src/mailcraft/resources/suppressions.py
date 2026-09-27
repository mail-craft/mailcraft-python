from __future__ import annotations

from typing import Any, Dict, Optional

from .._client import compact
from ._base import Resource


class Suppressions(Resource):
    def add(self, *, email: str, reason: Optional[str] = None) -> Dict[str, Any]:
        return self._client.post("/suppressions", compact({"email": email, "reason": reason}))

    def list(self, *, limit: Optional[int] = None) -> Dict[str, Any]:
        return self._client.get("/suppressions", {"limit": limit})

    def delete(self, id: int) -> None:
        self._client.delete(f"/suppressions/{id}")
