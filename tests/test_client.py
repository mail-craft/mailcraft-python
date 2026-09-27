"""Tests run the real client against httpx.MockTransport, so every request
goes through the same code a user's request would."""

from __future__ import annotations

import json
from typing import Any, Callable, Dict, List

import httpx
import pytest

from mailcraft import MailCraft, MailCraftApiError


def client_returning(
    handler: Callable[[httpx.Request], httpx.Response],
) -> MailCraft:
    return MailCraft(api_key="sk_test_123", transport=httpx.MockTransport(handler))


def recording(response: httpx.Response, calls: List[httpx.Request]) -> Callable[[httpx.Request], httpx.Response]:
    def handler(request: httpx.Request) -> httpx.Response:
        calls.append(request)
        return response

    return handler


def body_of(request: httpx.Request) -> Dict[str, Any]:
    return json.loads(request.content)


def test_it_requires_an_api_key() -> None:
    with pytest.raises(ValueError, match="API key is required"):
        MailCraft(api_key="")


def test_sending_an_email_posts_json_with_auth_and_maps_from() -> None:
    calls: List[httpx.Request] = []
    mailcraft = client_returning(recording(httpx.Response(201, json={"data": {"id": "em_1"}}), calls))

    result = mailcraft.emails.send(from_="hello@acme.test", to="ada@example.com", subject="Hi", html="<p>Hi</p>")

    request = calls[0]
    assert result == {"data": {"id": "em_1"}}
    assert request.method == "POST"
    assert str(request.url) == "https://api.mailcraft.host/v1/emails"
    assert request.headers["authorization"] == "Bearer sk_test_123"
    assert request.headers["user-agent"].startswith("mailcraft-python/")
    assert body_of(request) == {
        "from": "hello@acme.test",
        "to": ["ada@example.com"],
        "subject": "Hi",
        "html": "<p>Hi</p>",
    }


def test_query_parameters_skip_unset_values() -> None:
    calls: List[httpx.Request] = []
    mailcraft = client_returning(recording(httpx.Response(200, json={"data": []}), calls))

    mailcraft.contacts.list()
    mailcraft.contacts.list(limit=5)
    mailcraft.emails.validate("ada@example.com")

    assert str(calls[0].url) == "https://api.mailcraft.host/v1/contacts"
    assert calls[1].url.params["limit"] == "5"
    assert calls[2].url.path == "/v1/emails/validate"
    assert calls[2].url.params["email"] == "ada@example.com"


@pytest.mark.parametrize(
    ("call", "method", "path", "body"),
    [
        (lambda m: m.domains.verify(3), "POST", "/v1/domains/3/verify", None),
        (lambda m: m.senders.create(domain_id=3, email="hi@acme.test", name="Acme"), "POST", "/v1/senders", {"domain_id": 3, "email": "hi@acme.test", "name": "Acme"}),
        (lambda m: m.contacts.add_to_lists("ct_1", [4, 5]), "POST", "/v1/contacts/ct_1/lists", {"list_ids": [4, 5]}),
        (lambda m: m.contacts.remove_from_list("ct_1", 4), "DELETE", "/v1/contacts/ct_1/lists/4", None),
        (lambda m: m.lists.create(name="Beta", type="static"), "POST", "/v1/lists", {"name": "Beta", "type": "static"}),
        (lambda m: m.segments.create(name="Pro", filters={"conditions": []}), "POST", "/v1/segments", {"name": "Pro", "filters": {"conditions": []}}),
        (lambda m: m.properties.create(key="plan", label="Plan", type="text"), "POST", "/v1/properties", {"key": "plan", "label": "Plan", "type": "text"}),
        (lambda m: m.templates.update(7, subject="New"), "PATCH", "/v1/templates/7", {"subject": "New"}),
        (lambda m: m.template_folders.create(name="Onboarding"), "POST", "/v1/template-folders", {"name": "Onboarding"}),
        (lambda m: m.campaigns.send(9), "POST", "/v1/campaigns/9/send", None),
        (lambda m: m.webhooks.create(url="https://acme.test/hook", events=["email.delivered"]), "POST", "/v1/webhooks", {"url": "https://acme.test/hook", "events": ["email.delivered"]}),
        (lambda m: m.suppressions.add(email="x@example.com", reason="manual"), "POST", "/v1/suppressions", {"email": "x@example.com", "reason": "manual"}),
        (lambda m: m.metrics.reputation(), "GET", "/v1/reputation", None),
    ],
)
def test_each_resource_calls_the_right_endpoint(call: Any, method: str, path: str, body: Any) -> None:
    calls: List[httpx.Request] = []
    mailcraft = client_returning(recording(httpx.Response(200, json={"data": {}}), calls))

    call(mailcraft)

    assert calls[0].method == method
    assert calls[0].url.path == path
    assert (body_of(calls[0]) if calls[0].content else None) == body


def test_deletes_return_none_on_204() -> None:
    mailcraft = client_returning(lambda _: httpx.Response(204))

    assert mailcraft.domains.delete(3) is None


def test_business_rule_errors_carry_type_and_message() -> None:
    mailcraft = client_returning(
        lambda _: httpx.Response(402, json={"error": {"type": "plan_limit_reached", "message": "Upgrade to add more domains."}})
    )

    with pytest.raises(MailCraftApiError) as caught:
        mailcraft.domains.create(name="acme.test")

    assert caught.value.status == 402
    assert caught.value.type == "plan_limit_reached"
    assert str(caught.value) == "Upgrade to add more domains."


def test_validation_errors_carry_field_errors() -> None:
    mailcraft = client_returning(
        lambda _: httpx.Response(422, json={"message": "The email field is required.", "errors": {"email": ["The email field is required."]}})
    )

    with pytest.raises(MailCraftApiError) as caught:
        mailcraft.contacts.upsert(email="")

    assert caught.value.status == 422
    assert caught.value.errors == {"email": ["The email field is required."]}


def test_non_json_errors_fall_back_to_the_status() -> None:
    mailcraft = client_returning(lambda _: httpx.Response(503, text="upstream down"))

    with pytest.raises(MailCraftApiError) as caught:
        mailcraft.metrics.get()

    assert caught.value.status == 503


def test_custom_base_url_is_used_and_trailing_slash_trimmed() -> None:
    calls: List[httpx.Request] = []
    mailcraft = MailCraft(
        api_key="sk_test_123",
        base_url="https://staging.mailcraft.test/v1/",
        transport=httpx.MockTransport(recording(httpx.Response(200, json={"data": []}), calls)),
    )

    mailcraft.domains.list()

    assert str(calls[0].url) == "https://staging.mailcraft.test/v1/domains"
