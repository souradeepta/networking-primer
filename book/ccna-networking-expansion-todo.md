# CCNA-to-Staff Networking Expansion TODO

Use `[ ]` for incomplete, `[~]` for in progress, and `[x]` only after the
implementation and evidence checks pass. The spec is the source of truth.

## A. Planning and scaffolding

- [x] Create `book/ccna-networking/00-README.md` with ordered index and gates.
- [x] Create modules `01` through `15` with stable numeric filenames.
- [x] Add book/docs/root index links and related-track links.
- [x] Add validator checks for exact files, headings, diagrams, labs, answers,
  crosswalk terms, and link integrity.
- [x] Add or update `book/FACT-INFERENCE-LEDGER.md` for new facts and inferences.

## B. Module implementation matrix

For each row, all six boxes must be checked: `[C]` concepts, `[L]` lab,
`[E]` exercise+answer, `[D]` diagrams, `[Q]` Q&A, `[R]` references.

- [x] 01 Network models/physical: [C] [L] [E] [D] [Q] [R]
- [x] 02 Ethernet/switching/VLANs: [C] [L] [E] [D] [Q] [R]
- [x] 03 STP/LACP/L2 resilience: [C] [L] [E] [D] [Q] [R]
- [x] 04 IPv4/NAT/IPv6: [C] [L] [E] [D] [Q] [R]
- [x] 05 Routing/OSPF/VRF: [C] [L] [E] [D] [Q] [R]
- [x] 06 BGP/policy/WAN: [C] [L] [E] [D] [Q] [R]
- [x] 07 IP services/operations: [C] [L] [E] [D] [Q] [R]
- [x] 08 ACL/AAA/security: [C] [L] [E] [D] [Q] [R]
- [x] 09 Wireless/QoS: [C] [L] [E] [D] [Q] [R]
- [x] 10 Multicast/service delivery: [C] [L] [E] [D] [Q] [R]
- [x] 11 Data-center fabrics: [C] [L] [E] [D] [Q] [R]
- [x] 12 AWS/GCP cloud networking: [C] [L] [E] [D] [Q] [R]
- [x] 13 Private/public/hybrid/on-prem: [C] [L] [E] [D] [Q] [R]
- [x] 14 SDN/automation/IaC: [C] [L] [E] [D] [Q] [R]
- [x] 15 Observability/troubleshooting/design: [C] [L] [E] [D] [Q] [R]

## C. Crosswalk completion checks

- [x] Fundamentals, devices, planes, topology, domains, convergence
- [x] Copper/fiber/optics/PoE/interface errors/MTU
- [x] Ethernet/MAC/CAM/VLAN/trunk/SVI/L2 security/discovery
- [x] STP/RSTP/MST/BPDU guards/EtherChannel/LACP/PAgP/MLAG/vPC/FHRP
- [x] IPv4/subnetting/CIDR/VLSM/IPAM/public-private/overlap/exhaustion
- [x] NAT/PAT/static/dynamic/pools/hairpin/CGNAT
- [x] IPv6/GUA/link-local/ULA/multicast/EUI-64/SLAAC/DHCPv6/ND/DAD/transition
- [x] RIB/FIB/CEF/static/default/PBR/ECMP/redistribution/policy/VRF/BFD
- [x] OSPF areas/LSAs/DR-BDR/ABR-ASBR/stub-NSSA/auth/mismatch diagnosis
- [x] BGP attributes/policy/RR/communities/filtering/MP-BGP/EVPN/convergence
- [x] WAN/MPLS/GRE/IPsec/IKE/DMVPN/SD-WAN/VPN/DX/Interconnect
- [x] DHCP/DNS/NTP/SNMP/syslog/flows/SPAN/CDP/LLDP/SSH/ZTP
- [x] ACL/CoPP/AAA/TACACS/RADIUS/RBAC/802.1X/NAC/device hardening
- [x] Threats/IDS/IPS/NGFW/WAF/DDoS/segmentation/zero trust/SIEM/forensics
- [x] Wireless RF/channels/interference/AP/WLC/CAPWAP/WPA2/3/roaming
- [x] QoS classification/marking/DSCP/CoS/trust/policing/shaping/queues/WRED
- [x] IGMP/PIM/RP/RPF/SSM/ASM/multicast boundaries/BUM
- [x] Clos/VXLAN/EVPN/VTEP/VNI/route types/anycast/VRF/vPC/border/MTU
- [x] A10/F5 L4-L7/VIP/pools/health/persistence/SNAT/TLS/WAF/draining
- [x] AWS complete networking inventory and evidence paths
- [x] GCP complete networking inventory and evidence paths
- [x] Private/public/hybrid/on-prem setup, migration, cost, capacity, DR
- [x] SDN/NFV/controllers/APIs/YANG/NETCONF/RESTCONF/gNMI/OpenConfig
- [x] Terraform/Ansible/NSO/NDFC/device APIs/idempotency/state/drift/testing
- [x] Observability, tools, counters, captures, hypothesis/falsifier, incidents
- [x] SDE2 mechanism and Staff ownership/capacity/migration/system design

## D. Final quality review

- [x] Every module has two compliant Mermaid diagrams.
- [x] Every lab has starting state, reserved targets, steps, expected evidence,
  cleanup, and safety boundary.
- [x] Every exercise has detailed answer, rubric, SDE2 follow-up, and Staff
  follow-up.
- [x] Every module has six or more Q&A entries with wrong turns and evidence.
- [x] Provider/vendor/version claims are labeled and referenced.
- [x] No duplicate Terraform/controller/device ownership is taught implicitly.
- [x] AWS/GCP differences are technically explicit, not simple renamings.
- [x] Links and indexes cover every file exactly once.
- [x] `./scripts/validate.sh` passes.
- [x] `python3 examples/request_path.py` passes.
- [x] `python3 scripts/check_internal_links.py` passes.
- [x] `git diff --check` passes.

### D.1 Terra semantic remediation checklist

- [x] Runner injects only control/config faults; no paired plane-fault field is
  stored for a scenario.
- [x] Pure module-specific evaluator derives forwarding/service observations
  from effective control plus a separate traffic fixture.
- [x] Negative test proves a metadata-only control change can remain healthy
  while an evaluator-only mechanism fault fails the data plane.
- [x] Ownership probes are derived from retained read-back and traffic-path
  inputs; caller-supplied probe status is rejected.
- [x] Read-backs model desired state -> reconciliation -> effective state with
  status, changed fields, task ID, and effective-state hash.
- [x] Completed submissions use module-specific JSON pointers and thresholds;
  generic health-only pointers are rejected.
- [x] Stale v2 retained bundles were removed; one v3 tracked run remains.

## E. Terra final-review gates

Local implementation gates are now recorded as complete for this pass. Terra
semantic approval is still pending; do not treat these implementation checks
as Terra approval.

- [ ] Terra checks every section D concept against the rendered book.
- [ ] Terra checks every module against the content contract.
- [ ] Terra checks lab realism, networking depth, and answer correctness.
- [ ] Terra checks AWS/GCP/Terraform examples and ownership boundaries.
- [ ] Terra checks all diagrams for readability, ASCII, and accurate paths.
- [ ] Terra checks SDE2 versus Staff progression and missing follow-ups.
- [ ] Terra reports no high-severity omission or misleading claim.
- [x] Owner implements the latest Terra repairs and records the retained artifacts.
- [ ] Owner requests a later independent Terra pass.
- [ ] Terra signs off with a dated coverage report.

## F. Current progress snapshot

Updated 2026-09-01 after the latest Terra audit and semantic remediation pass.

- **Implementation:** The semantic remediation is saved in the fixture runner
  and evaluator. It includes control-only faults, derived mechanism
  observations, reconciliation-model read-backs, 15 four-criterion
  module-specific submissions, and 24 ownership records with derived negative
  controls.
- **Retained evidence:** run
  `20260901T172659.876804Z-b746b7bb`, schema `ccna-fixture-bundle/v3`, with 15
  module bundles, 24 ownership records, and 15 submission records.
- **Automated quality:** repository validation, the Python request-path example,
  internal-link checks, Mermaid checks, heading checks, and `git diff --check`
  pass.
- **Terra quality gate:** **NOT APPROVED** until Terra verifies the new saved
  bundles, evaluator semantics, reconciliation model, module-specific
  thresholds, ownership pairs, and independent negative controls.
- **Publication:** this repair pass is currently uncommitted. Commit/push only
  after the full checks below pass and the user requests publication.

## G. Latest remediation handoff

The current implementation is saved in
[`ccna-terra-remediation-handoff.md`](ccna-terra-remediation-handoff.md).
The shared fixture runner now covers all 15 modules and produces captured
JSON evidence under `book/ccna-networking/fixtures/observed/`; the canonical
field-level ownership matrix and criterion-backed submissions are linked from
the collection README. These are implementation artifacts, not Terra sign-off.
The status remains **NOT APPROVED** until Terra independently reruns the
fixture, validates the evidence, and closes the quality gates in section E.
