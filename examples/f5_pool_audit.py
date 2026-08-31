#!/usr/bin/env python3
"""Read-only pool-member audit using the F5 Python SDK.

Install `f5-sdk`, provide F5_HOST, F5_USER, F5_PASSWORD, and a verified CA
bundle path in F5_CA_BUNDLE. This script intentionally has no write operation.
"""

import os
import sys


def require(name: str) -> str:
    """Read a required setting without printing secret values."""
    value = os.environ.get(name)
    if not value:
        raise SystemExit(f"Missing required environment variable: {name}")
    return value


def main() -> None:
    """Print the observed state of members in one partitioned pool."""
    if len(sys.argv) != 2 or not sys.argv[1].startswith("/"):
        raise SystemExit("Usage: f5_pool_audit.py /Partition/pool_name")
    try:
        from f5.bigip import ManagementRoot
    except ImportError as error:
        raise SystemExit("Install the optional dependency: python3 -m pip install f5-sdk") from error

    partition, pool_name = sys.argv[1].strip("/").split("/", maxsplit=1)
    ca_bundle = require("F5_CA_BUNDLE")
    if not os.path.isfile(ca_bundle):
        raise SystemExit("F5_CA_BUNDLE must name an existing CA bundle")

    bigip = ManagementRoot(require("F5_HOST"), require("F5_USER"), require("F5_PASSWORD"))
    bigip._meta_data["icr_session"].verify = ca_bundle
    pool = bigip.tm.ltm.pools.pool.load(name=pool_name, partition=partition)
    print(f"Pool: /{partition}/{pool.name}")
    for member in pool.members_s.get_collection():
        print(f"{member.name}: session={member.session}, state={member.state}")


if __name__ == "__main__":
    main()
