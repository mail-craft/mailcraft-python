from __future__ import annotations

from typing import Any, Dict, Optional

from .._client import compact
from ._base import Resource


class Campaigns(Resource):
    def create(
        self,
        *,
        name: str,
        subject: str,
        template_id: int,
        sender_id: int,
        list_id: Optional[int] = None,
        segment_id: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Create a draft campaign for a list or a segment."""
        return self._client.post(
            "/campaigns",
            compact(
                {
                    "name": name,
                    "subject": subject,
                    "template_id": template_id,
                    "sender_id": sender_id,
                    "list_id": list_id,
                    "segment_id": segment_id,
                }
            ),
        )

    def list(self) -> Dict[str, Any]:
        return self._client.get("/campaigns")

    def get(self, id: int) -> Dict[str, Any]:
        return self._client.get(f"/campaigns/{id}")

    def send(self, id: int) -> Dict[str, Any]:
        return self._client.post(f"/campaigns/{id}/send")

    def delete(self, id: int) -> None:
        self._client.delete(f"/campaigns/{id}")
