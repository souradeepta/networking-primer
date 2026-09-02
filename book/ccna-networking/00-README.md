# CCNA-to-Staff Networking

This is the ordered networking-foundation expansion for the book. It begins
with electrons, frames, and packet models, then builds through campus routing,
security, wireless, multicast, data-center fabrics, cloud, automation, and
Staff-level design. It is networking-first: every cloud or infrastructure-as-
code example is explained in terms of interfaces, routes, policy, failure
domains, and evidence.

## A. How to use this collection

Read modules 01 through 15 in order for a full path. For interview preparation,
read the mental model, failure lab, exercise answer, and interview section in
each module. Commands are configuration-shaped, not promises of universal
syntax. Targets use RFC 5737/RFC 3849 documentation space, fictional device
names, or local simulators. Do not paste a mutation into production.

| Module | Focus | Primary interview outcome |
| --- | --- | --- |
| [01 Network models and physical](01-network-models-and-physical.md) | Layers, planes, topology, cabling, optics, PoE | Trace a fault from medium to application |
| [02 Ethernet, switching, and VLANs](02-ethernet-switching-and-vlans.md) | Frames, CAM, VLANs, trunks, L3 switching | Explain a local packet hop precisely |
| [03 STP, LACP, and Layer 2 resilience](03-stp-lacp-and-layer2-resilience.md) | Loops, convergence, bundles, FHRP | Design safe redundancy and diagnose loops |
| [04 IPv4, subnetting, NAT, and IPv6](04-ipv4-subnetting-nat-and-ipv6.md) | Addressing, translation, dual stack | Allocate and troubleshoot address space |
| [05 Routing, OSPF, and VRF](05-routing-static-ospf-and-vrf.md) | RIB/FIB, OSPF, PBR, segmentation | Prove control-plane and forwarding behavior |
| [06 BGP, policy, and hybrid WAN](06-bgp-policy-and-hybrid-wan.md) | BGP, MPLS, VPN, SD-WAN | Reason about path policy and convergence |
| [07 Network services and operations](07-network-services-and-operations.md) | DDI, time, telemetry, access | Operate a diagnosable network |
| [08 ACLs, AAA, and network security](08-acls-aaa-and-network-security.md) | Filters, identity, threats, controls | Build least-privilege network boundaries |
| [09 Wireless and QoS](09-wireless-and-qos.md) | RF, WLAN, classification, queuing | Design for airtime and latency budgets |
| [10 Multicast and service delivery](10-multicast-and-service-delivery.md) | IGMP, PIM, BUM, ADC/LB | Follow one-to-many and VIP paths |
| [11 Data-center fabrics](11-data-center-fabrics.md) | Clos, VXLAN/EVPN, borders, capacity | Design a scalable fabric and insertion point |
| [12 AWS and GCP cloud networking](12-cloud-networking-aws-gcp.md) | VPC/VPC, routes, controls, hybrid | Map packet semantics across clouds |
| [13 Private, public, hybrid, and on-prem](13-private-public-hybrid-and-onprem.md) | Deployment models and migration | Choose an operating boundary and exit plan |
| [14 SDN, automation, and IaC](14-automation-sdn-and-iac.md) | APIs, models, controllers, Terraform | Separate intent, state, and ownership |
| [15 Observability, troubleshooting, and design](15-observability-troubleshooting-and-design.md) | Evidence, SLOs, capacity, interviews | Lead a technical design and incident |

## B. Completion gates

For every module, a learner should be able to:

1. Explain the normal packet, frame, control-plane, and forwarding path.
2. Read the safe configuration shape and name what is vendor or release
   specific.
3. Collect read-only evidence before changing anything.
4. Complete the failure lab with a hypothesis, falsifier, repair, and rollback.
5. Defend the exercise answer at SDE2 depth and extend it at Staff depth.
6. Answer the numbered questions without confusing configured state with
   operational state.

## C. Lab safety and evidence labels

**Fact** means a protocol behavior supported by an RFC or vendor document.
**Vendor terminology** means a product-specific name that may not transfer to
another platform. **Observed lab result** is valid only for the stated fixture,
software version, and topology. **Engineering inference** is a reasoned design
conclusion, not a protocol guarantee. AWS and GCP snippets use placeholders and
are explicitly non-runnable unless a lab supplies credentials, quotas, and
provider versions.

## D. Cross-track map

Pair this sequence with the [long-form book index](../README.md), the [cloud
networking track](../../cloud-networking-interview/00-README.md), the [Terraform
track](../../terraform-interview/00-README.md), and the [integrated platform
labs](../../platform-integration-labs/00-README.md). The surrounding tracks
provide longer AWS/GCP, F5/A10, Cisco NSO/NDFC, and implementation exercises;
this collection supplies the foundational concepts those tracks assume.

## E. References and review

Use the RFC Editor, IANA registries, Cisco configuration guides, AWS VPC
documentation, Google Cloud VPC documentation, and Linux man pages as primary
evidence. Exact commands vary by release. Before marking a module complete,
run the repository validator, internal-link checker, and the examples test.

## F. Atomic concept-to-evidence crosswalk

This table is the completion map for the collection. A learner should be able
to name the mechanism, collect the read-back evidence, and state what evidence
would falsify the hypothesis. The examples are intentionally vendor-aware;
the command or API name may vary by platform and release.

| Primary module | Atomic concepts covered | Read-back evidence | Falsifier to discuss |
| --- | --- | --- | --- |
| 01 | OSI/TCP-IP, encapsulation, MTU, physical media, duplex, ARP/ND, Ethernet framing | Interface counters, negotiated speed/duplex, MTU, ARP/ND cache, packet capture | Healthy L1/L2 counters and complete neighbor resolution falsify a physical/ARP hypothesis |
| 02 | MAC learning, CAM flooding, VLANs, trunks, native VLAN, inter-VLAN gateway, broadcast domains | MAC table, VLAN/trunk state, tagged capture, gateway ARP/ND, interface counters | Correct VLAN membership and tagged frames falsify an access/trunk mismatch |
| 03 | STP/RSTP/MST, root bridge, BPDU guard, LACP, port-channel hashing, loop prevention | STP role/state, root ID, LACP members, topology changes, loop counters | Stable root, forwarding members, and no topology changes falsify a loop/convergence hypothesis |
| 04 | IPv4 classes/route classes, CIDR/VLSM, subnetting, NAT/PAT, IPv6, SLAAC, DHCPv6, NDP, RA | Route table, address/prefix assignment, NAT translations, NDP/RA capture, `ip route get` | Correct longest-prefix match and translation/ND state falsify an addressing hypothesis |
| 05 | Connected/static/default routes, administrative distance, longest prefix, OSPF areas, LSAs, network types, DR/BDR, passive interfaces, VRF, PBR | RIB/FIB, OSPF neighbors/database, LSA type and timers, VRF tables, policy counters | Matching timers/area/network type and installed FIB path falsify an OSPF adjacency hypothesis |
| 06 | eBGP/iBGP, best path, next-hop recursion, communities, route maps, RR, BFD, MPLS/VPN, GRE/IPsec, DMVPN, SD-WAN, hybrid WAN | BGP summary, received/advertised routes, attributes, RIB/FIB, tunnel/IKE/BFD, cloud route state | Established peer plus absent/filtered prefix falsifies a transport-only explanation |
| 07 | DHCP, DNS/DDI, NTP/PTP, syslog, SNMP, streaming telemetry, management plane, config backup | Lease/lookup/time state, telemetry stream, logs, management ACL and source identity | Correct service response and synchronized timestamps falsify a service-plane hypothesis |
| 08 | ACLs, stateful filtering, control/data plane protection, AAA/RBAC, TACACS+/RADIUS, PKI, hardening, signed images, secure boot, threats | Ordered policy counters, AAA logs, certificates, image signature/boot state, CoPP/drop counters | Permitted/denied flow evidence and valid identity/boot chain falsify a policy/identity hypothesis |
| 09 | WLAN architecture, RF channels, 802.11 association/authentication, roaming, WPA, controller, QoS markings, queues, WMM, congestion | Client/AP/controller state, RSSI/SNR, channel/utilization, queue drops, DSCP markings | Healthy RF and queue evidence falsify an airtime or classification hypothesis |
| 10 | IGMP, PIM-SM, RP, RPF, multicast trees, BUM, replication, CDN/LB/ADC service delivery | IGMP groups, PIM neighbors/RPF, multicast route, replication counters, VIP/health state | Correct RPF/tree and healthy backend evidence falsify a multicast or service-delivery hypothesis |
| 11 | Clos/spine-leaf, ECMP, VXLAN, VTEP, EVPN route types, BUM replication, borders, capacity, insertion points | Underlay adjacency, VTEP/EVPN tables, VNI mapping, route type, ECMP members, telemetry | Healthy underlay plus missing EVPN/VNI state falsifies a generic link-failure hypothesis |
| 12 | AWS VPC and GCP VPC, subnets, routes, security groups/firewalls, NACLs, TGW/Cloud Router, VPN, DX/Interconnect, quotas/logging | Route-table and policy API read-back, flow logs, Reachability Analyzer/Connectivity Tests, tunnel/BGP state | API state, flow evidence, and reachability proof disagreeing with the symptom falsify a local host hypothesis |
| 13 | Private, public, hybrid, on-prem, shared services, segmentation, egress, migration, exit strategy, operational boundaries | Ownership matrix, route/policy propagation, dependency map, failover and cost/latency measurements | Independent failure-domain and ownership evidence falsifies an assumption that one team controls the path |
| 14 | APIs/models, SDN intent, controllers, NSO/NDFC, Terraform state, import, drift, idempotency, retries, pagination, device read-back | Plan/state, controller intent/device operational state, API request IDs, diff and rollback artifact | Matching desired/state/device read-back falsifies a drift or controller convergence hypothesis |
| 15 | Observability, SLOs, packet path, hypothesis/falsifier method, incident command, capacity, design trade-offs, SDE2/Staff communication | Timeline, traces/flows/logs/metrics, change diff, capacity model, decision record | Cross-layer evidence that remains healthy falsifies the suspected layer and redirects investigation |

For the hardening row, explicitly distinguish vendor terminology from portable
principles: secure boot and signed images are platform features, while chain of
trust, least privilege, patch verification, and recovery testing are portable
engineering practices. For VXLAN, distinguish control-plane EVPN signaling from
the BUM replication method; ingress replication and multicast underlay are not
interchangeable implementations.

## G. Cross-track object, field, and read-back contract

The [canonical field-level ownership matrix](fixtures/ownership-matrix.md) is
the source of truth for single-writer boundaries, approvers, evidence owners,
rollback owners, request samples, authoritative read-backs, and independent
data-plane assertions. The shorthand table below is a navigation summary;
when it differs in detail, the canonical matrix wins.

The [artifact-backed worked submissions](fixtures/worked-submissions.md) and
the [local fixture runner](fixtures/README.md) provide the saved evidence for
each module. Run the runner before treating an output as an observed result.

### G.1 Fixture evidence semantics

The local fixture is deliberately bounded. The runner injects only a
control/configuration change; [`evaluator.py`](fixtures/evaluator.py) derives
the module-specific forwarding or service observation from the reconciled
effective state and a separate traffic path. Each module also retains a
negative test in which a metadata-only control change stays healthy while a
mechanism-only evaluator fault fails. Read-backs are reconciliation outputs
with desired state, computed changed fields, status, task ID, effective state,
and device/service observation. These local results are learning evidence,
not proof of a real AWS, GCP, NSO, NDFC, F5, or A10 mutation.

Use this table when connecting the primer to the cloud, Terraform, controller,
and ADC tracks. **Fact** means the named product exposes an object or concept
of this general kind; exact field names, API versions, permissions, and response
shapes vary. **Vendor terminology** identifies a product label. **Engineering
inference** is the ownership rule proposed for the exercise, not a provider
guarantee. Every mutation in a real lab must be paired with a read-after-write
check and a separately recorded forwarding or service assertion.

| Track/object | Request fields to capture | Authoritative owner for the exercise | Required read-back and forwarding proof |
| --- | --- | --- | --- |
| AWS route | route table ID, destination CIDR/prefix, target type/ID, propagation flag | Terraform or the named cloud-network owner, never both | AWS route-table response, TGW/VPN propagation state, `Reachability Analyzer` result, and a bounded probe |
| AWS policy | security-group ID/rule tuple, NACL number/action/direction, Network Firewall policy revision | Security owner for policy; Terraform only when imported and declared | rule response plus ordered flow-log accept/reject evidence in both directions |
| AWS load balancer | LB ARN/type, listener protocol/port, target group ARN, health thresholds | ADC/cloud service owner | listener and target-health response, access log sample, and client-to-VIP/backend assertion |
| AWS VPN/logging/quota | tunnel options/BGP ASN, flow-log destination/filter, service quota name/value | Hybrid-network owner for VPN; observability owner for logs; cloud governance for quota | tunnel/BGP state, flow-log delivery/readback, quota response, and measured failover headroom |
| GCP route | VPC, destination range, priority, next hop, dynamic/static origin | Terraform or GCP network owner by explicit contract | route list/API response, Cloud Router learned route where relevant, Connectivity Test, and a bounded probe |
| GCP policy | target tag/service account, source range/identity, protocol/port, priority/action, hierarchical scope | GCP security owner or imported Terraform state | firewall-policy response, rule hit/flow-log evidence, and reverse-path test |
| GCP load balancer | forwarding rule, target proxy, URL/map, backend service, health check | GCP service/ADC owner | forwarding-rule and backend-health responses, request log, and VIP assertion |
| GCP VPN/logging/quota | HA VPN gateway/tunnel, Cloud Router peer/BGP fields, log sink/filter, quota metric/limit | Hybrid, observability, and governance owners respectively | tunnel/BGP status, audit/logging readback, quota response, and failure-path measurement |
| Terraform plan/state/import | resource address, provider identity, planned action, state serial/backend lock, import ID | One Terraform workspace/state owner per object | saved plan, `terraform show`, state address/ID, second plan, and provider object read-back |
| Terraform drift/pagination/retry | refresh result, page token, retry class/backoff, request ID, partial-apply marker | Terraform/provider integration owner | repeated list completeness, bounded retry trace, post-apply state, and device/cloud forwarding proof |
| NSO CDB/task/device | service path, YANG leaf, commit/task ID, transaction status, device target | NSO service owner; device team owns unsupported local escape hatch | task/CDB read-back, device effective config, operational counters, and service probe |
| NDFC intent/device | fabric/VRF/VNI/route-target fields, intent version, task ID, device diff | NDFC fabric owner for fabric objects | intent/task state, switch NVE/EVPN/VLAN read-back, FIB/ECMP state, and endpoint probe |
| F5 AS3/iControl | tenant/application/service, virtual address/port, pool/member/monitor, declaration or URI | F5/ADC owner; Terraform records ownership when delegated | AS3 declaration/task or iControl response, BIG-IP effective config, pool health, and VIP request |
| A10 REST | partition, virtual-server/service-group/member, template/health-monitor fields, request ID | A10/ADC owner | REST response plus Thunder effective object, SLB stats/health, and VIP/backend assertion |

For all rows, a successful HTTP/API response is **not** sufficient evidence of
forwarding. A learner must show the authoritative object, the effective device
or provider state, and a bounded data-plane or service result. **Illustrative
result:** a mock may print `REQUEST_ACCEPTED READ_BACK_MISMATCH`; this teaches
the evidence shape and must not be reported as execution against AWS, GCP,
NSO, NDFC, F5, or A10. **Observed lab result:** only the local fixture output
and the repository checks are observed in this book.
