from __future__ import annotations

from typing import Any, Dict, List, Optional

from .._client import compact
from ._base import Resource

class Templates(Resource):
    def create(
        self,
        *,
        name: str,
        subject: str,
        html_body: Optional[str] = None,
        text_body: Optional[str] = None,
        template_folder_id: Optional[int] = None,
        variables: Optional[List[Dict[str, Any]]] = None,
    ) -> Dict[str, Any]:
        return self._client.post(
            "/templates",
            compact(
                {
                    "name": name,
                    "subject": subject,
                    "html_body": html_body,
                    "text_body": text_body,
                    "template_folder_id": template_folder_id,
                    "variables": variables,
                }
            ),
        )

    def list(self) -> Dict[str, Any]:
        return self._client.get("/templates")

    def get(self, id: int) -> Dict[str, Any]:
        return self._client.get(f"/templates/{id}")

    def update(self, id: int, **params: Any) -> Dict[str, Any]:
        """Update a template; each save becomes a new version. Pass only the fields to change."""
        return self._client.patch(f"/templates/{id}", params)

    def delete(self, id: int) -> None:
        self._client.delete(f"/templates/{id}")

class TemplateFolders(Resource):
    def create(self, *, name: str) -> Dict[str, Any]:
        return self._client.post("/template-folders", {"name": name})

    def list(self) -> Dict[str, Any]:
        return self._client.get("/template-folders")

    def delete(self, id: int) -> None:
        self._client.delete(f"/template-folders/{id}")
