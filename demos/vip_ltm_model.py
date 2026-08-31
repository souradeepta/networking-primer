#!/usr/bin/env python3
"""Model global answer selection followed by local LTM eligibility."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Member:
    """A simplified LTM pool member."""

    name: str
    monitor_healthy: bool
    administratively_enabled: bool

    @property
    def eligible(self) -> bool:
        """A member is eligible only when enabled and monitor-healthy."""
        return self.monitor_healthy and self.administratively_enabled


@dataclass(frozen=True)
class Site:
    """A simplified GTM target containing LTM members."""

    name: str
    dns_healthy: bool
    vip: str
    members: tuple[Member, ...]

    @property
    def eligible(self) -> bool:
        """Require both DNS health and at least one eligible local member."""
        return self.dns_healthy and any(member.eligible for member in self.members)


def choose(sites: tuple[Site, ...]) -> tuple[Site, Member]:
    """Choose the first eligible site and its first eligible LTM member."""
    for site in sites:
        if site.eligible:
            return site, next(member for member in site.members if member.eligible)
    raise RuntimeError("No site and LTM member are jointly eligible")


def main() -> None:
    """Print a deterministic failover-shaped decision trace."""
    sites = (
        Site("east", False, "203.0.113.20", (Member("east-a", False, True),)),
        Site("west", True, "203.0.113.30", (Member("west-a", True, True),)),
    )
    site, member = choose(sites)
    print(f"GTM/BIG-IP DNS answer: {site.name} -> {site.vip}")
    print(f"LTM eligible member: {member.name}")


if __name__ == "__main__":
    main()
