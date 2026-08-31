"""Exercise F5 REST client safety decisions with local mock responses."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Response:
    status: int
    body: dict


def collect_pages(responses: list[Response]) -> list[dict]:
    """Collect items only when every page succeeds; reject partial state."""
    items: list[dict] = []
    for response in responses:
        if response.status != 200:
            raise RuntimeError(f"read failed: HTTP {response.status}")
        items.extend(response.body.get("items", []))
        if not response.body.get("nextLink"):
            return items
    raise TimeoutError("pagination ended without a terminal page")


pages = [
    Response(200, {"items": [{"name": "member-a"}], "nextLink": "/page/2"}),
    Response(200, {"items": [{"name": "member-b"}] }),
]
print("members:", [item["name"] for item in collect_pages(pages)])
print("unknown write rule: after timeout, GET by stable partition-qualified name before retry")
