# CCNA-to-Staff Networking Book Expansion Specification

## A. Purpose and non-goals

Add a cohesive `book/ccna-networking/` section that covers the full CCNA-style
networking foundation and the adjacent SDE2/Staff systems topics requested for
this primer. The section must teach packet paths, control/data planes,
configuration intent, verification, failure evidence, and design trade-offs.
It is not a certification cram sheet or a production runbook.

Every module must use reserved addresses, fictional devices, or local
simulators; label **Fact**, **Vendor terminology**, **Observed lab result**, and
**Engineering inference**; and explain how Cisco terminology maps (or does not
map) to AWS, GCP, A10, F5, NSO, NDFC, Linux, and generic networking.

## B. Exact file plan

| File | Required coverage |
| --- | --- |
| `00-README.md` | ordered index, prerequisites, lab safety, completion gates |
| `01-network-models-and-physical.md` | OSI/TCP-IP, encapsulation, devices, planes, topology, cabling, optics, PoE, errors |
| `02-ethernet-switching-and-vlans.md` | frames, MAC/CAM, VLANs, trunks, 802.1Q, access/voice/management, SVI, L3 switch |
| `03-stp-lacp-and-layer2-resilience.md` | STP/RSTP/MST, BPDUs, guards, PortFast, EtherChannel/LACP/PAgP, MLAG/vPC/stacking |
| `04-ipv4-subnetting-nat-and-ipv6.md` | binary, CIDR/VLSM, public/private, IPAM, NAT/PAT, IPv6 addressing, ND, SLAAC, DHCPv6, transition |
| `05-routing-static-ospf-and-vrf.md` | RIB/FIB/CEF, longest match, static/default/floating/PBR, OSPF, areas/LSAs, redistribution, VRF/leaking |
| `06-bgp-policy-and-hybrid-wan.md` | eBGP/iBGP, ASNs, best path, attributes, communities, filtering, RR, BFD, WAN/MPLS/SD-WAN/IPsec/GRE |
| `07-network-services-and-operations.md` | DHCP, DNS, NTP, SNMP, syslog, NetFlow/IPFIX, SPAN, CDP/LLDP, SSH, backups, images, licensing |
| `08-acls-aaa-and-network-security.md` | ACLs, wildcard masks, CoPP, AAA/TACACS/RADIUS, SSH hardening, NAC/802.1X, IDS/IPS/NGFW/WAF, zero trust |
| `09-wireless-and-qos.md` | RF, bands/channels, SNR/RSSI, interference, AP/WLC/CAPWAP, WPA2/3, roaming, QoS classification/marking/queues |
| `10-multicast-and-service-delivery.md` | IGMP, PIM, RP, RPF, SSM/ASM, multicast boundaries, BUM, ADC/LB service insertion |
| `11-data-center-fabrics.md` | Clos, spine-leaf, underlay/overlay, VXLAN/EVPN, VTEP/VNI, route types, anycast gateway, vPC, border, MTU |
| `12-cloud-networking-aws-gcp.md` | AWS VPC/TGW/VPN/DX/SG/NACL/PrivateLink/LB/Route53/flow logs; GCP VPC/Cloud Router/HA VPN/Interconnect/firewall/LB/Cloud DNS/logs |
| `13-private-public-hybrid-and-onprem.md` | deployment models, physical private cloud, public cloud, hybrid routing, address/identity/data gravity, migration, cost/capacity |
| `14-automation-sdn-and-iac.md` | SDN/NFV, controllers, APIs, NETCONF/RESTCONF/gNMI/YANG/OpenConfig, Ansible, Terraform, NSO, NDFC, F5/A10 APIs |
| `15-observability-troubleshooting-and-design.md` | layered diagnosis, tools, captures, counters, SLOs, capacity, HA/DR, incident response, system design, interview synthesis |

## C. Required content contract for every module

Each module must contain headings A–L or a justified equivalent:

1. **Learning objectives and prerequisites.** State what a learner can explain,
   configure in a lab, verify, and troubleshoot.
2. **Portable mental model.** Explain packet/frame/request flow and control
   plane versus forwarding/data plane before vendor syntax.
3. **Concept inventory.** Define every named concept assigned in section D;
   include mechanism, purpose, limits, and adjacent terminology.
4. **Configuration shapes.** Include safe Cisco IOS-XE/NX-OS or Linux examples
   plus AWS/GCP/Terraform shapes where applicable. Mark release/provider
   variance and never imply placeholders are universally runnable.
5. **Verification.** Give read-only commands/API queries and expected evidence
   for host, switch, router, controller, ADC, AWS, and GCP layers.
6. **Failure lab.** Provide starting state, injected fault, symptom, hypothesis
   tree, falsifier, evidence order, smallest safe action, and rollback/forward
   repair.
7. **Hands-on exercise.** Include deliverables, constraints, scoring rubric,
   answer key, SDE2 follow-up, and Staff follow-up.
8. **Diagrams.** Include at least two ASCII-only Mermaid diagrams: normal path
   and ownership/failure path. Use the repository light theme and dark text.
9. **Interview Q&A.** Include at least six numbered questions with direct
   answers, common wrong turns, evidence, and progressive follow-ups.
10. **References and evidence labels.** Link primary RFC/vendor/cloud docs and
    distinguish facts from inferences.

## D. No-omission concept crosswalk

| Category | Concepts that must appear and be findable |
| --- | --- |
| Fundamentals | OSI, TCP/IP, encapsulation, routers, L2/L3 switches, firewalls, IPS, APs, controllers, endpoints, servers, hypervisors, VMs, containers, LAN/WAN/SOHO/data center/campus/branch, planes, topology, domains, convergence |
| Physical | copper, fiber, SMF/MMF, SFP/QSFP, connectors, wavelengths, loss, power, distance, speed/duplex, auto-negotiation, CRC/errors/flaps, MTU/jumbo, PoE, budgets, loops |
| Switching | frames, MAC/CAM, learning/aging, flooding, VLAN/access/trunk/802.1Q/native/voice/management, pruning, hopping, SVI/routed ports, port security, storm control, DHCP snooping, DAI, IP Source Guard, CDP/LLDP |
| L2 resilience | STP/RSTP/MST, root/roles/states/cost, BPDUs, guards, PortFast, TCN, EtherChannel/LACP/PAgP/hash, MLAG/vPC/StackWise, FHRP/HSRP/VRRP/GLBP, split brain |
| IP | IPv4/binary/subnet/CIDR/VLSM/summarization/private/public/IPAM/overlap/exhaustion; NAT/PAT/static/dynamic/pools/hairpin/CGNAT; IPv6 GUA/link-local/ULA/multicast/anycast/EUI-64/SLAAC/DHCPv6/ND/DAD/dual stack/NAT64/DNS64 |
| Routing | RIB/FIB/CEF, longest match, AD/metrics/next hop/recursive, connected/static/default/floating/PBR/null/blackhole, ECMP, redistribution, policy, VRF/VRF-Lite/leaking, BFD |
| OSPF | router ID, LSDB, SPF, LSAs, hello/dead, network types, DR/BDR, areas, ABR/ASBR, route classes, stub/NSSA, auth, passive, mismatch troubleshooting |
| BGP/WAN | e/iBGP, ASNs, AS path, local pref, MED, weight, origin, next hop, RR/confederation, communities, prepending, filters, max-prefix, MP-BGP/EVPN, convergence, graceful restart/dampening, peering/transit, MPLS, SD-WAN, GRE, IPsec, IKE, DMVPN, VPN/DX/Interconnect |
| Services | DHCP/client/server/relay/options/snooping; DNS recursive/auth/forward/reverse/cache/TTL/split/DNSSEC/failover; NTP/stratum; SNMPv2c/v3, syslog, NetFlow/IPFIX, SPAN/RSPAN/ERSPAN, TFTP/FTP/SCP/SFTP, SSH, ZTP |
| Security | standard/extended/named/IPv4/IPv6 ACLs, direction/order/implicit deny/wildcards, CoPP, AAA, TACACS+, RADIUS, LDAP/MFA/RBAC, VTY, hardening, secure boot/images, threats, ARP/DHCP/MAC/VLAN/STP/DNS/route attacks, IDS/IPS/NGFW/WAF/DDoS, segmentation/microsegmentation/NAC/802.1X/zero trust/SIEM/forensics |
| Wireless/QoS | RF/bands/channels/DFS/width, RSSI/SNR/noise/attenuation/multipath/interference, SSID/BSS/ESS, AP/WLC/CAPWAP/FlexConnect, WPA2/3/802.1X/EAP/RADIUS, guest/roaming/voice; classification/marking/DSCP/CoS/trust, policing/shaping/queues/WFQ/CBWFQ/LLQ/WRED/tail drop/jitter |
| Multicast | groups, IGMP/snooping/querier/v2/v3, PIM DM/SM/Bidir, SSM/ASM, RP/static/Auto-RP/BSR, RPF, trees, boundaries, multicast over VXLAN, BUM |
| Data center | Clos, underlay/overlay, VXLAN/VTEP/VNI, EVPN/MP-BGP, route types 2/3/5, ARP/ND suppression, host mobility/duplicate MAC, anycast gateway, VRF/VLAN/VNI, vPC/MLAG, border/service leaf, route leaking, service insertion, multicast/ingress replication, DCI/multi-site, buffering/microbursts/oversubscription/ECMP |
| Load balancing | L4/L7, VIP/listener/pool/member/node/monitor, persistence, health, SNAT/pools/automap/source preservation, one/two-arm/DSR, TLS termination/pass-through/re-encryption/SNI, WAF/rate limits/draining/slow start, A10 Thunder, F5 BIG-IP LTM/DNS, cloud LB/CDN/edge |
| Cloud | AWS VPC/subnet/AZ/route tables/IGW/NAT/ENI/SG/NACL/endpoints/PrivateLink/TGW/peering/VPN/DX/Route53/LB/flow logs/Reachability Analyzer/Network Firewall/CloudFront/Global Accelerator; GCP VPC/subnet/routes/Cloud Router/HA VPN/Interconnect/peering/PSC/Private Access/Cloud NAT/firewall/LB/Cloud DNS/logging/flow logs/Connectivity Tests/Shared VPC/Cloud Armor |
| Models/design | private/public/hybrid/on-prem, address/identity/data gravity, failure domains, HA/DR, active-active/standby, RTO/RPO/SLO, capacity/headroom/oversubscription, quotas/cost/FinOps, migration/failback, governance/ownership/exit |
| Automation | CLI/SSH, REST/SOAP, NETCONF, RESTCONF, gNMI, OpenConfig, YANG/XPath/XML/JSON/YAML, Python, Ansible, Terraform/Pulumi/CloudFormation, NSO/NED/FASTMAP/CDB, NDFC, Catalyst Center/Meraki, AS3/iControl, A10 REST, NX-API, idempotency/state/import/drift/provider/testing/policy/secrets/async/pagination/retries |
| Operations | baselines, hypothesis/falsifier, logs/metrics/traces/captures/counters, RED/USE, tools (`ping`, `mtr`, `dig`, `curl`, `ss`, `ip`, `tcpdump`, Wireshark, `ethtool`, `iperf`), route/MAC/ARP/neighbor/conntrack/session/TCAM/buffer evidence, incident/change/canary/chaos/break-glass |

## E. Quality and acceptance gates

- Every concept in section D appears in one module and in the TODO crosswalk.
- Every module meets the content contract: two diagrams, one lab, one exercise
  with answer, six Q&A entries, verification commands, and references.
- At least one Cisco IOS-XE/NX-OS and one Linux/read-only verification path is
  present where the concept is device-relevant.
- AWS and GCP examples name their distinct route, firewall, load-balancer,
  VPN, logging, and quota semantics; Terraform ownership is explicit.
- All diagrams are ASCII-only Mermaid with the repository light theme.
- All mutable commands are clearly lab-only, use fictional/reserved targets,
  and include prechecks, saved plan/config, verification, and cleanup.
- `book/README.md`, `docs/README.md`, root `README.md`, and a new section README
  link every planned file in order.
- `./scripts/validate.sh`, `python3 examples/request_path.py`, internal-link
  validation, heading validation, and `git diff --check` pass.
- Terra performs a final concept-by-concept audit and reports zero unaddressed
  rows before the expansion is marked complete.
