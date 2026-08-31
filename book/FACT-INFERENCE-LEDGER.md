# Book fact and inference ledger

This ledger maps the central claims of each chapter to evidence. A **fact** is
an externally specified protocol, documented vendor behavior, or explicitly
measured observation. An **inference** is a design recommendation derived from
those facts; it must be validated against the target service and platform.

| Chapter | Central fact(s) and evidence | Central inference(s) to validate |
| --- | --- | --- |
| 01 TCP/IP | IP forwarding and TCP behavior: [RFC 791](https://www.rfc-editor.org/rfc/rfc791), [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293) | A packet-path evidence sequence narrows fault scope; confirm with captures and route state. |
| 02 Addressing | CIDR and private address allocation: [RFC 4632](https://www.rfc-editor.org/rfc/rfc4632), [RFC 1918](https://www.rfc-editor.org/rfc/rfc1918) | Prefix plans and NAT boundaries reduce ambiguity only when ownership and routes are consistent. |
| 03 Ethernet | Ethernet/VLAN framing: [IEEE 802.1Q](https://standards.ieee.org/ieee/802.1Q/); ARP: [RFC 826](https://www.rfc-editor.org/rfc/rfc826); IPv6 ND: [RFC 4861](https://www.rfc-editor.org/rfc/rfc4861) | MTU and VLAN checks are portable evidence categories; exact commands are vendor-specific. |
| 04 Transport | TCP, UDP, and QUIC: [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293), [RFC 768](https://www.rfc-editor.org/rfc/rfc768), [RFC 9000](https://www.rfc-editor.org/rfc/rfc9000) | Protocol choice follows application loss/order/latency needs; measure the real workload. |
| 05 HTTP | HTTP semantics and caching: [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110), [RFC 9111](https://www.rfc-editor.org/rfc/rfc9111) | Cache keys and retries must be designed around identity and method semantics. |
| 06 DNS | DNS hierarchy and transport: [RFC 1034](https://www.rfc-editor.org/rfc/rfc1034), [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035); negative caching: [RFC 2308](https://www.rfc-editor.org/rfc/rfc2308) | Resolver-aware troubleshooting and TTL planning are operational inferences. |
| 07 DDI | DHCP behavior: [RFC 2131](https://www.rfc-editor.org/rfc/rfc2131); DNS behavior: [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035) | IPAM ownership and reconciliation order reduce drift; validate with the estate’s source-of-truth model. |
| 08 TLS | TLS: [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446); X.509: [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280); SNI: [RFC 6066](https://www.rfc-editor.org/rfc/rfc6066) | Termination and rotation boundaries need two-sided tests and local key-management controls. |
| 09 Proxies | HTTP proxy semantics: [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110); F5 objects: [LTM virtual servers](https://clouddocs.f5.com/cli/tmsh-reference/v14/modules/ltm/ltm_virtual.html) | Health depth, retry limits, persistence, and SNAT are service-specific design decisions. |
| 10 LTM | F5 virtual servers, pools, and monitors: [F5 LTM references](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/) | Object separation and monitor choice improve diagnosis; test behavior on the deployed BIG-IP version. |
| 11 GTM/DNS | F5 Wide IP terminology: [F5 Wide IP guide](https://clouddocs.f5.com/training/community/big-iq-cloud-edition/html/class10/module2/module2.html); DNS caching: [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035) | DNS failover is staggered by cache and connection reuse; confirm with resolver measurements. |
| 12 Observability | HTTP problem details: [RFC 9457](https://www.rfc-editor.org/rfc/rfc9457); telemetry concepts: [OpenTelemetry](https://opentelemetry.io/docs/concepts/observability-primer/) | Correlating independent signals raises confidence; sampling and retention require local SLO/privacy decisions. |
| 13 Automation | F5 API/SDK interfaces: [iControl REST](https://clouddocs.f5.com/api/icontrol-rest/), [F5 Python SDK](https://github.com/F5Networks/f5-common-python); SSH architecture: [RFC 4251](https://datatracker.ietf.org/doc/html/rfc4251) | Read-before-write, least privilege, preconditions, and rollback are safety inferences to encode in CI. |
| 14 Reliability | SLO practice: [Google SRE Workbook](https://sre.google/workbook/implementing-slos/); incident response: [NIST SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Failure-domain, retry-budget, canary, and rollback choices must be tied to service evidence and ownership. |

The ledger does not claim that a citation proves every sentence in a chapter;
it identifies the central evidence-backed propositions and separates them from
recommendations that require engineering judgment.
