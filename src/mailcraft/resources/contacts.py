from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._client import compact
from ._base import Resource


class Contacts(Resource):
    def upsert(
        self,
        *,
        email: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        status: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
        **extra: Any,
    ) -> Dict[str, Any]:
        """Create a contact, or update it if one already exists for this email."""
        return self._client.post(
            "/contacts",
            compact(
                {
                    "email": email,
                    "first_name": first_name,
                    "last_name": last_name,
                    "status": status,
                    "properties": properties,
                    **extra,
                }
            ),
        )

    def list(self, *, limit: Optional[int] = None) -> Dict[str, Any]:
        return self._client.get("/contacts", {"limit": limit})

    def get(self, id: str) -> Dict[str, Any]:
        return self._client.get(f"/contacts/{id}")

    def delete(self, id: str) -> None:
        self._client.delete(f"/contacts/{id}")

    def unsubscribe(self, id: str) -> Dict[str, Any]:
        return self._client.post(f"/contacts/{id}/unsubscribe")

    def add_to_lists(self, id: str, list_ids: List[int]) -> None:
        self._client.post(f"/contacts/{id}/lists", {"list_ids": list_ids})

    def lists(self, id: str) -> Dict[str, Any]:
        return self._client.get(f"/contacts/{id}/lists")

    def remove_from_list(self, id: str, list_id: int) -> None:
        self._client.delete(f"/contacts/{id}/lists/{list_id}")
