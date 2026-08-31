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
| 15 Cloud and Kubernetes | Kubernetes service networking: [Kubernetes Services](https://kubernetes.io/docs/concepts/services-networking/service/), ingress: [Kubernetes Ingress](https://kubernetes.io/docs/concepts/services-networking/ingress/); TLS: [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) | CNI, cloud load-balancer, SNAT, health-check, and controller-convergence behavior must be verified on the selected platform. |
| 16 BGP and anycast | BGP-4: [RFC 4271](https://www.rfc-editor.org/rfc/rfc4271); route selection and security: [RFC 7454](https://www.rfc-editor.org/rfc/rfc7454), [RFC 6811](https://www.rfc-editor.org/rfc/rfc6811); DNS: [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035) | Anycast health gates, convergence timing, DNS steering, and stateful-session behavior are engineering inferences requiring measurements. |
| 17 Security and zero trust | TLS and certificate validation: [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446), [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280); SSH architecture: [RFC 4251](https://datatracker.ietf.org/doc/html/rfc4251); zero trust: [NIST SP 800-207](https://csrc.nist.gov/pubs/sp/800/207/final) | WAF placement, mTLS trust boundaries, header handling, fail-open/closed choices, and policy rollout are deployment-specific inferences. |

## Case-study evidence map

| Case | Primary evidence | Inference boundary |
| --- | --- | --- |
| 01 LTM VIP/certificate migration | [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446), [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280), [F5 LTM](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/) | Cache overlap, dual certificates, and rollback sequencing are scenario inferences. |
| 02 GTM failover | [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035), [F5 Wide IP](https://clouddocs.f5.com/training/community/big-iq-cloud-edition/html/class10/module2/module2.html) | Resolver migration timing and capacity guardrails require local measurements. |
| 03 DDI drift | [RFC 2131](https://www.rfc-editor.org/rfc/rfc2131), [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035) | Ownership and reconciliation order are engineering policy. |
| 04 Certificate automation | [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280), [F5 SDK](https://github.com/F5Networks/f5-common-python) | Canary gates, overlap windows, and approval controls are inferred safeguards. |
| 05 Firewall/TCP timeout | [RFC 9293](https://www.rfc-editor.org/rfc/rfc9293), [RFC 1812](https://www.rfc-editor.org/rfc/rfc1812) | A missing response’s drop location requires captures and flow evidence. |
| 06 MTU black hole | [RFC 1191](https://www.rfc-editor.org/rfc/rfc1191), [RFC 8201](https://www.rfc-editor.org/rfc/rfc8201) | Tunnel overhead, measured PMTU, and MSS clamp choice are scenario facts/inferences. |
| 07 IPv6 migration | [RFC 8200](https://www.rfc-editor.org/rfc/rfc8200), [RFC 4861](https://www.rfc-editor.org/rfc/rfc4861) | Dual-stack rollout order and Happy-Eyeballs observations require the target estate. |
| 08 DNSSEC failure | [RFC 4033](https://www.rfc-editor.org/rfc/rfc4033), [RFC 4034](https://www.rfc-editor.org/rfc/rfc4034), [RFC 6781](https://www.rfc-editor.org/rfc/rfc6781) | Key-roll ordering and resolver cache timing are incident inferences. |
| 09 DHCP exhaustion | [RFC 2131](https://www.rfc-editor.org/rfc/rfc2131), [RFC 2132](https://www.rfc-editor.org/rfc/rfc2132) | Scope expansion, lease duration, and quarantine policy need capacity evidence. |
| 10 Duplicate IP | [RFC 826](https://www.rfc-editor.org/rfc/rfc826), [RFC 5227](https://www.rfc-editor.org/rfc/rfc5227) | Correlating ARP, IPAM, DHCP, and switch data is an operational inference. |
| 11 LTM persistence hotspot | [F5 LTM pool reference](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_pool.html), [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110) | Persistence key choice and drain limits are service-specific. |
| 12 False-positive monitor | [F5 monitor reference](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/ltm_monitor.html) | Probe depth and readiness endpoint design require application ownership. |
| 13 LTM HA failover | [F5 virtual server reference](https://clouddocs.f5.com/cli/tmsh-reference/v14/modules/ltm/ltm_virtual.html) | State-sync and failover timing must be verified on the deployed pair/version. |
| 14 GTM topology misrouting | [F5 GTM API reference](https://clouddocs.f5.com/api/icontrol-rest/APIRef_tm_gtm.html), [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035) | Resolver locality and topology rule quality are measured assumptions. |
| 15 GTM TTL migration | [RFC 1035](https://www.rfc-editor.org/rfc/rfc1035), [RFC 2308](https://www.rfc-editor.org/rfc/rfc2308) | Cache convergence and client connection reuse are inferred timelines. |
| 16 Expired TLS intermediate | [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280), [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) | Renewal overlap and trust-store rollout require inventory evidence. |
| 17 mTLS trust rotation | [RFC 5280](https://www.rfc-editor.org/rfc/rfc5280), [RFC 8446](https://www.rfc-editor.org/rfc/rfc8446) | Dual trust and client authorization mapping are policy choices. |
| 18 F5 SDK idempotency drift | [iControl REST](https://clouddocs.f5.com/api/icontrol-rest/), [F5 SDK](https://github.com/F5Networks/f5-common-python) | Normalization, preconditions, retry classification, and rollback are inferences. |
| 19 LB upgrade rollback | [F5 LTM references](https://clouddocs.f5.com/cli/tmsh-reference/latest/modules/ltm/), [NIST SP 800-61r3](https://csrc.nist.gov/pubs/sp/800/61/r3/final) | Upgrade gates, canary scope, and rollback triggers depend on local HA evidence. |

The ledger does not claim that a citation proves every sentence in a chapter;
it identifies the central evidence-backed propositions and separates them from
recommendations that require engineering judgment.
