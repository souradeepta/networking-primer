# Safe shell and Python demos

These demos are observation/model exercises. They do not configure BIG-IP,
change DNS, flush caches, rotate certificates, or scan networks. Run them from
the repository root and use only local or explicitly authorized targets.

| Demo | Purpose | Default target |
| --- | --- | --- |
| `dns_observe.sh` | Capture DNS response code, answer, authority, and TTL | `example.invalid` |
| `tls_inspect.sh` | Inspect a TLS handshake and SNI selection | `127.0.0.1:8443` |
| `vip_ltm_model.py` | Model GTM selection followed by LTM member eligibility | Pure Python |
| `certificate_audit.py` | Read public PEM certificate metadata | User-provided file |
| `f5_change_planner.py` | Produce a partition-aware pool diff from fixtures | Pure Python |
| `f5_rest_pagination_tasks.py` | Exercise pagination and unknown-write handling | Pure Python |

The shell demos may report expected timeout/refusal for documentation targets;
that is useful evidence, not a production diagnosis.

For packet-level experiments, use the optional [Docker lab](docker/README.md)
and the [Wireshark/tshark workflow](wireshark.md). Capture only interfaces and
containers you own; packet captures can contain credentials and personal data.

Open the dependency-free [request journey animation](animations/request-journey.html)
or [DNS failover animation](animations/dns-failover.html) in a browser. Both
use fictional infrastructure and include reduced-motion behavior.
