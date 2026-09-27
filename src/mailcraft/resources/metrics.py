from __future__ import annotations

from typing import Any, Dict, Optional

from ._base import Resource


class Metrics(Resource):
    def get(self, *, start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict[str, Any]:
        """Daily sending metrics. Dates are ``YYYY-MM-DD``."""
        return self._client.get("/metrics", {"start_date": start_date, "end_date": end_date})

    def reputation(self) -> Dict[str, Any]:
        return self._client.get("/reputation")
