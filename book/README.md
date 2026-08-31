# Networking Primer: Book Edition

This directory is the long-form edition. Read the chapters in order the first
time; later, use the troubleshooting and F5 chapters as a reference. Each
chapter is designed as a study session rather than a glossary entry.

## Reading contract

Every chapter contains objectives, prerequisites, a mental model, a worked
example, a failure section, an operational checklist, a diagram, and explained
questions and answers. The chapter text distinguishes protocol/vendor facts
from engineering inferences. Commands are observation-oriented and use
documentation or local addresses unless an authorized lab target is supplied.

## Planned chapters

1. TCP/IP and packet journeys
2. Addressing, subnetting, and routing
3. Ethernet, ARP, ND, and VLANs
4. TCP, UDP, QUIC, and connection behavior
5. HTTP, APIs, proxies, and application protocols
6. DNS resolution and authoritative operations
7. DHCP, IPAM, and DDI architecture
8. TLS, certificates, PKI, and mTLS
9. Reverse proxies and load-balancing design
10. F5 BIG-IP LTM in depth
11. F5 GTM/BIG-IP DNS in depth
12. Observability and layered troubleshooting
13. Automation, F5 Python SDK, REST, and SSH
14. Reliability, security, and safe change management
15. Cloud networking and Kubernetes ingress
16. BGP, anycast, and multi-region traffic engineering
17. Network security, WAF, and zero trust

The original `docs/` files remain the quick-start edition; these chapters are
the elaborated treatment.

See the [book fact and inference ledger](FACT-INFERENCE-LEDGER.md) for the
chapter-level evidence map.

The [infrastructure case studies](case-studies/README.md) apply the concepts to
fictional but operationally realistic outages and migrations.

Focused references and runnable demos are in [book/topics](topics/README.md)
and [`demos/`](../demos/README.md). These files deliberately separate VIP,
certificate, monitor, GTM, DDI, and automation concerns for targeted study.

The platform track adds cloud-native ingress, routing policy, WAF controls,
observability/SLOs, performance engineering, modern transports, overlays,
network policy, service discovery, and time synchronization. Treat these as
production design material: validate vendor behavior in a lab and preserve a
tested rollback path before making a change.
