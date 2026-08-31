"""Plan a partition-aware F5 pool change without contacting a device.

The fixture and planner are intentionally local. They demonstrate discovery,
normalization, approval evidence, and unknown-write reconciliation.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class PoolState:
    partition: str
    name: str
    members: tuple[str, ...]
    monitor: str


def plan(current: PoolState, desired: PoolState) -> list[str]:
    """Return a stable, minimal diff; never proposes cross-partition deletion."""
    if (current.partition, current.name) != (desired.partition, desired.name):
        raise ValueError("resource identity changed")
    changes: list[str] = []
    for member in sorted(set(desired.members) - set(current.members)):
        changes.append(f"add member {member}")
    if current.monitor != desired.monitor:
        changes.append(f"set monitor {current.monitor} -> {desired.monitor}")
    return changes


current = PoolState("Common", "orders_pool", ("10.20.1.10:8443",), "https")
desired = PoolState("Common", "orders_pool", ("10.20.1.10:8443", "10.20.1.11:8443"), "https")
print("plan:", plan(current, desired))
print("safe boundary: local fixture only; no SDK, REST, SSH, or device mutation")
