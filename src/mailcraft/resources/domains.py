from __future__ import annotations

from typing import Any, Dict, Optional

from .._client import compact
from ._base import Resource


class Domains(Resource):
    def create(self, *, name: str, region: Optional[str] = None) -> Dict[str, Any]:
        return self._client.post("/domains", compact({"name": name, "region": region}))

    def list(self) -> Dict[str, Any]:
        return self._client.get("/domains")

    def get(self, id: int) -> Dict[str, Any]:
        return self._client.get(f"/domains/{id}")

    def verify(self, id: int) -> Dict[str, Any]:
        return self._client.post(f"/domains/{id}/verify")

    def delete(self, id: int) -> None:
        self._client.delete(f"/domains/{id}")
