"""Official Python SDK for the MailCraft email API."""

from __future__ import annotations

from typing import Optional

import httpx

from ._client import DEFAULT_BASE_URL, HttpClient
from ._version import __version__
from .errors import MailCraftApiError
from .resources import (
    Campaigns,
    Contacts,
    Domains,
    Emails,
    Lists,
    Metrics,
    Properties,
    Segments,
    Senders,
    Suppressions,
    TemplateFolders,
    Templates,
    Webhooks,
)

__all__ = ["MailCraft", "MailCraftApiError", "__version__"]


class MailCraft:
    """The MailCraft API client.

    >>> mailcraft = MailCraft(api_key="sk_live_...")
    >>> mailcraft.emails.send(from_="hello@yourapp.com", to="user@example.com", subject="Hi", html="<p>Hi</p>")

    Use it as a context manager (or call ``close()``) to release connections.
    """

    def __init__(
        self,
        api_key: str,
        *,
        base_url: str = DEFAULT_BASE_URL,
        timeout: float = 30.0,
        transport: Optional[httpx.BaseTransport] = None,
    ) -> None:
        self._client = HttpClient(api_key, base_url=base_url, timeout=timeout, transport=transport)

        self.emails = Emails(self._client)
        self.domains = Domains(self._client)
        self.senders = Senders(self._client)
        self.contacts = Contacts(self._client)
        self.lists = Lists(self._client)
        self.segments = Segments(self._client)
        self.properties = Properties(self._client)
        self.templates = Templates(self._client)
        self.template_folders = TemplateFolders(self._client)
        self.campaigns = Campaigns(self._client)
        self.webhooks = Webhooks(self._client)
        self.suppressions = Suppressions(self._client)
        self.metrics = Metrics(self._client)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> "MailCraft":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()
