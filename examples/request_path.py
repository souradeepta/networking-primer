#!/usr/bin/env python3
"""Simulate the decisions that make a request path debuggable.

This is a pure-Python model, not a load balancer or DNS implementation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class Target:
    """A site endpoint with the minimum state needed for this exercise."""

    site: str
    address: str
    dns_healthy: bool
    ltm_healthy_members: int


def select_dns_target(targets: list[Target]) -> Target:
    """Return the first site eligible for a simplified global-availability policy."""
    for target in targets:
        if target.dns_healthy:
            return target
    raise RuntimeError("No GTM/BIG-IP DNS target is eligible")


def serve_request(target: Target) -> list[str]:
    """Create a trace showing the distinct DNS and LTM decisions."""
    trace = [f"DNS selected {target.site} -> {target.address}"]
    if target.ltm_healthy_members < 1:
        raise RuntimeError(f"{target.site} answer has no healthy LTM pool members")
    trace.append(f"TCP/TLS connects to VIP {target.address}:443")
    trace.append(f"LTM selected one of {target.ltm_healthy_members} healthy pool members")
    trace.append("Application returned HTTP 200")
    return trace


def main() -> None:
    """Run a failover-shaped example."""
    targets = [
        Target("east", "203.0.113.20", dns_healthy=False, ltm_healthy_members=0),
        Target("west", "203.0.113.30", dns_healthy=True, ltm_healthy_members=3),
    ]
    for event in serve_request(select_dns_target(targets)):
        print(event)


if __name__ == "__main__":
    main()
