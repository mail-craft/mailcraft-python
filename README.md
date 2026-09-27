# mailcraft-python

Official Python SDK for the [MailCraft](https://mailcraft.host) email API: transactional email, contacts, lists, segments, templates, campaigns, webhooks and more.

Requires Python 3.9+. Built on [httpx](https://www.python-httpx.org/).

## Install

```bash
pip install mailcraft
```

## Quick start

```python
import os
from mailcraft import MailCraft

mailcraft = MailCraft(api_key=os.environ["MAILCRAFT_API_KEY"])

email = mailcraft.emails.send(
    from_="hello@yourdomain.com",   # `from` is a Python keyword, so it's `from_`
    to="person@example.com",        # a string or a list of addresses
    subject="Welcome!",
    html="<p>Thanks for signing up.</p>",
)
print(email["data"]["id"])
```

Create an API key under **Settings → API keys** in your MailCraft dashboard. Use the client as a context manager (or call `close()`) to release connections:

```python
with MailCraft(api_key=os.environ["MAILCRAFT_API_KEY"]) as mailcraft:
    mailcraft.contacts.upsert(email="ada@example.com", first_name="Ada", properties={"plan": "pro"})
```

## Resources

Every MailCraft SDK has the same resources and methods:

| Resource | Methods |
| --- | --- |
| `emails` | `send`, `list`, `get`, `validate` |
| `domains` | `create`, `list`, `get`, `verify`, `delete` |
| `senders` | `create`, `list`, `get`, `delete` |
| `contacts` | `upsert`, `list`, `get`, `delete`, `unsubscribe`, `add_to_lists`, `lists`, `remove_from_list` |
| `lists` | `create`, `list`, `get`, `delete` |
| `segments` | `create`, `list`, `get`, `delete` |
| `properties` | `create`, `list`, `delete` |
| `templates` | `create`, `list`, `get`, `update`, `delete` |
| `template_folders` | `create`, `list`, `delete` |
| `campaigns` | `create`, `list`, `get`, `send`, `delete` |
| `webhooks` | `create`, `list`, `delete` |
| `suppressions` | `add`, `list`, `delete` |
| `metrics` | `get`, `reputation` |

Responses are returned as the API's JSON (dictionaries). See the [API reference](https://docs.mailcraft.host/api-reference) for every field.

## Errors

Any non-2xx response raises `MailCraftApiError`:

```python
from mailcraft import MailCraftApiError

try:
    mailcraft.domains.create(name="acme.com")
except MailCraftApiError as error:
    print(error.status)   # e.g. 402
    print(error.type)     # e.g. "plan_limit_reached" (business-rule errors)
    print(error.errors)   # field errors for 422 validation failures
```

## Options

```python
MailCraft(
    api_key="sk_live_...",
    base_url="https://api.mailcraft.host/v1",  # override for staging or self-hosting
    timeout=30.0,                               # seconds
)
```

## Development

```bash
pip install -e ".[dev]"
pytest
```

The tests run the real client against `httpx.MockTransport`, so every request goes through the same code a user's would.

## License

MIT
