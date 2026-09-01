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

## A. Read in order

1. [TCP/IP and packet journeys](01-tcp-ip-and-packet-journeys.md)
2. [Addressing, subnetting, and routing](02-addressing-subnetting-routing.md)
3. [Ethernet, ARP, ND, and VLANs](03-ethernet-arp-vlans.md)
4. [TCP, UDP, QUIC, and connection behavior](04-transport-protocols.md)
5. [HTTP, APIs, proxies, and application protocols](05-http-apis-and-proxies.md)
6. [DNS resolution and authoritative operations](06-dns-resolution-and-operations.md)
7. [DHCP, IPAM, and DDI architecture](07-ddi-dns-dhcp-ipam.md)
8. [TLS, certificates, PKI, and mTLS](08-tls-certificates-pki-mtls.md)
9. [Reverse proxies and load-balancing design](09-reverse-proxies-and-load-balancing.md)
10. [F5 BIG-IP LTM in depth](10-f5-ltm-in-depth.md)
11. [F5 GTM/BIG-IP DNS in depth](11-f5-gtm-bigip-dns-in-depth.md)
12. [Observability and layered troubleshooting](12-observability-and-troubleshooting.md)
13. [Automation, F5 Python SDK, REST, and SSH](13-automation-f5-sdk-rest-ssh.md)
14. [Reliability, security, and safe change management](14-reliability-security-change-management.md)
15. [Cloud networking and Kubernetes ingress](15-cloud-networking-and-kubernetes-ingress.md)
16. [BGP, anycast, and multi-region traffic engineering](16-bgp-anycast-and-multi-region.md)
17. [Network security, WAF, and zero trust](17-network-security-waf-zero-trust.md)

## B. Choose by objective

- **Packet and protocol foundations:** chapters 1–8.
- **Traffic delivery and F5:** chapters 9–11, then [focused topics](topics/README.md).
- **Operations and automation:** chapters 12–14, then [case studies](case-studies/README.md).
- **Cloud and Staff design:** chapters 15–17, then the [cloud track](../cloud-networking-interview/00-README.md) and [integrated labs](../platform-integration-labs/00-README.md).

The original `docs/` files remain the quick-start edition; these chapters are
the elaborated treatment. Use the [documentation index](../docs/README.md) for
the logical order of quick-start, interview, infra-engineer, and governance
material.

See the [book fact and inference ledger](FACT-INFERENCE-LEDGER.md) for the
chapter-level evidence map.

The [infrastructure case studies](case-studies/README.md) apply the concepts to
fictional but operationally realistic outages and migrations.

Focused references and runnable demos are in [book/topics](topics/README.md)
and [`demos/`](../demos/README.md). These files deliberately separate VIP,
certificate, monitor, GTM, DDI, and automation concerns for targeted study.

For a complete CCNA-to-Staff networking path, continue with the [CCNA-to-Staff
networking expansion](ccna-networking/00-README.md). It covers switching,
routing, BGP/WAN, security, wireless, QoS, multicast, EVPN/VXLAN, AWS/GCP,
private/public/hybrid networking, automation, and observability.

The expansion's ordered modules are [01](ccna-networking/01-network-models-and-physical.md),
[02](ccna-networking/02-ethernet-switching-and-vlans.md),
[03](ccna-networking/03-stp-lacp-and-layer2-resilience.md),
[04](ccna-networking/04-ipv4-subnetting-nat-and-ipv6.md),
[05](ccna-networking/05-routing-static-ospf-and-vrf.md),
[06](ccna-networking/06-bgp-policy-and-hybrid-wan.md),
[07](ccna-networking/07-network-services-and-operations.md),
[08](ccna-networking/08-acls-aaa-and-network-security.md),
[09](ccna-networking/09-wireless-and-qos.md),
[10](ccna-networking/10-multicast-and-service-delivery.md),
[11](ccna-networking/11-data-center-fabrics.md),
[12](ccna-networking/12-cloud-networking-aws-gcp.md),
[13](ccna-networking/13-private-public-hybrid-and-onprem.md),
[14](ccna-networking/14-automation-sdn-and-iac.md), and
[15](ccna-networking/15-observability-troubleshooting-and-design.md).

The platform track adds cloud-native ingress, routing policy, WAF controls,
observability/SLOs, performance engineering, modern transports, overlays,
network policy, service discovery, and time synchronization. Treat these as
production design material: validate vendor behavior in a lab and preserve a
tested rollback path before making a change.
