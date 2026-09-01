# Independent Terra quality-gate audit: CCNA-to-Staff expansion

**Audit date:** 2026-09-01  
**Decision:** **NOT APPROVED**  
**Scope:** `book/ccna-networking/00-README.md`, modules `01`--`15`, the
expansion specification, TODO, prior review, `docs/references.md`,
`book/FACT-INFERENCE-LEDGER.md`, `scripts/validate.sh`, and the root/book/docs
indexes.

## A. Decision and audit boundary

This is an independent quality-gate audit of the **saved** implementation. It
does not change learning material or validators. The sole change made by this
audit is this report.

The expansion has complete topic coverage, strong discoverability, compliant
diagrams, appropriate evidence labels, and a safe local-fixture framing. The
decision remains **NOT APPROVED** because the three earlier high-severity
quality gates are only partially repaired:

1. Most lab records are runnable local state-file models, not live local
   fixtures that exercise the named network or control-plane mechanism.
2. Rubrics name artifacts and thresholds, but their claimed completed scores
   are not tied to a shown, executed artifact-and-evidence bundle.
3. The cross-track ownership table is useful, but it does not yet provide
   exclusive object-and-field ownership with an approver, rollback owner,
   paired request/read-back records, and an independent data-plane assertion.

This is a vendor-aware learning repository, not an operational runbook. The
required repair therefore remains a **safe local simulation or fixture** plus
clearly labelled illustrative vendor request/read-back examples; it does not
require credentials or mutations in AWS, GCP, NSO, NDFC, F5, A10, or production
network devices.

## B. Quantified gate results

| Gate | Result | Independent evidence |
| --- | --- | --- |
| Exact collection | **Pass: 16/16** | `00-README.md` plus exactly modules `01`--`15`; no extra module Markdown files. |
| Ordered discoverability | **Pass: 4/4** | Root `README.md`, `book/README.md`, `docs/README.md`, and collection `00-README.md` list the modules in numeric order. |
| A--L headings | **Pass: 15/15** | Every module has A--L headings. Module 05 adds section M, which is a readability concern only. |
| Mermaid diagrams | **Pass: 30/30** | Two Mermaid fences per module; repository checks confirm ASCII-only diagrams. The reviewed diagrams use the required light/background-dark-text pattern. |
| Normal and ownership/failure paths | **Pass: 15/15** | Module 06 now includes the owner/approver/evidence/repair/rollback path in section E; the remaining modules provide equivalent failure ownership paths. |
| All Section C categories | **Pass: 26/26 present** | The category-by-category map in section C identifies a primary teaching location for every TODO category. |
| Evidence labels and ledgers | **Pass: 15/15** | Each module includes Fact, Vendor terminology, Observed lab result, and Engineering inference labels; `docs/references.md` and `book/FACT-INFERENCE-LEDGER.md` carry expansion-level maps. |
| Interview progression | **Pass: 15/15** | Each module provides at least six Q&A entries with Answer, Wrong turn, Evidence, and Follow-up material, including SDE2 and Staff framing. |
| Written lab lifecycle | **Pass: 15/15** | All modules state a safety boundary, setup, baseline, fault, assertion, repair, rollback, cleanup, and no-leak check. |
| Executed fixed-path mock blocks | **Pass: 11/11** | The section-K blocks in modules 05--15 exited 0 in this audit; the audit confirmed no `/tmp/ccna05-lab` through `/tmp/ccna15-lab` directories remained. |
| Genuinely replayable mechanism lab | **Fail: 1/15 demonstrated** | Module 01 section K builds a namespace/veth fixture. Modules 02--04 describe a Linux shape but do not provide an executable end-to-end build. Modules 05--15 use runnable local text/JSON state models, explicitly not the named BGP, DHCP/DNS, ACL, RF, PIM, EVPN, cloud, controller, or incident mechanism. |
| Evidence-backed completed worked submission | **Fail: 0/15 demonstrated** | Every module now supplies a rubric with artifacts and thresholds, but each “Completed score” is a self-award over illustrative or expected evidence rather than a shown submission transcript tied to every score. |
| Object/field ownership and paired read-back | **Partial** | `00-README.md` section G names requested fields, broad owners, and required proofs, but lacks exclusive writer/approver/evidence/rollback assignments per field and request/response/read-back exemplars. |
| Independent data-plane verification | **Partial** | The materials correctly say API success is insufficient and name probes/flow tools, but the fixture results do not independently exercise or assert the described forwarding/service path. |
| Required repository checks | **Pass: 4/4** | Validation record in section F. |

## C. Section C no-omission audit

“Found” means the category is actually taught with a primary home; it does not
claim the category has a mechanism-replayable lab or an approved worked
submission.

| TODO Section C category | Primary teaching location | Result |
| --- | --- | --- |
| Fundamentals, devices, planes, topology, domains, convergence | `01-network-models-and-physical.md` sections A--E | Found |
| Copper, fiber, optics, PoE, interface errors, MTU | `01-network-models-and-physical.md` sections C--K | Found |
| Ethernet, MAC/CAM, VLAN, trunk, SVI, L2 security, discovery | `02-ethernet-switching-and-vlans.md` sections C--E | Found |
| STP/RSTP/MST, guards, EtherChannel/LACP/PAgP, MLAG/vPC, FHRP | `03-stp-lacp-and-layer2-resilience.md` sections C--E | Found |
| IPv4, CIDR/VLSM, IPAM, public/private, overlap, exhaustion | `04-ipv4-subnetting-nat-and-ipv6.md` sections A--C | Found |
| NAT/PAT, static/dynamic, pools, hairpin, CGNAT | `04-ipv4-subnetting-nat-and-ipv6.md` sections C--G | Found |
| IPv6, GUA/link-local/ULA, SLAAC, DHCPv6, ND/DAD, transition | `04-ipv4-subnetting-nat-and-ipv6.md` sections C--E | Found |
| RIB/FIB/CEF, static/default, PBR, ECMP, redistribution, VRF, BFD | `05-routing-static-ospf-and-vrf.md` sections C--E and K | Found |
| OSPF areas/LSAs/DR-BDR/ABR-ASBR/stub-NSSA/auth/mismatch | `05-routing-static-ospf-and-vrf.md` sections D, G, and K | Found |
| BGP attributes/policy/RR/communities/filtering/MP-BGP/EVPN/convergence | `06-bgp-policy-and-hybrid-wan.md` sections C--F | Found |
| WAN/MPLS/GRE/IPsec/IKE/DMVPN/SD-WAN/VPN/DX/Interconnect | `06-bgp-policy-and-hybrid-wan.md` sections C--E | Found |
| DHCP/DNS/NTP/SNMP/syslog/flows/SPAN/CDP/LLDP/SSH/ZTP | `07-network-services-and-operations.md` sections C--E | Found |
| ACL/CoPP/AAA/TACACS/RADIUS/RBAC/802.1X/NAC/hardening | `08-acls-aaa-and-network-security.md` sections C--E | Found |
| Threats, IDS/IPS, NGFW/WAF/DDoS, segmentation, zero trust, SIEM/forensics | `08-acls-aaa-and-network-security.md` sections C--G | Found |
| Wireless RF/channels/interference/AP/WLC/CAPWAP/WPA2/3/roaming | `09-wireless-and-qos.md` sections B--E | Found |
| QoS classification/marking/DSCP/CoS/trust/policing/shaping/queues/WRED | `09-wireless-and-qos.md` sections C--E | Found |
| IGMP/PIM/RP/RPF/SSM/ASM/multicast boundaries/BUM | `10-multicast-and-service-delivery.md` sections B--E | Found |
| Clos/VXLAN/EVPN/VTEP/VNI/route types/anycast/VRF/vPC/border/MTU | `11-data-center-fabrics.md` sections B--E | Found |
| A10/F5 L4-L7/VIP/pools/health/persistence/SNAT/TLS/WAF/draining | `10-multicast-and-service-delivery.md` sections B--E and K | Found |
| AWS networking inventory and evidence paths | `12-cloud-networking-aws-gcp.md` sections C--E | Found |
| GCP networking inventory and evidence paths | `12-cloud-networking-aws-gcp.md` sections C--E | Found |
| Private/public/hybrid/on-prem, migration, cost, capacity, DR | `13-private-public-hybrid-and-onprem.md` sections B--G | Found |
| SDN/NFV/controllers/APIs/YANG/NETCONF/RESTCONF/gNMI/OpenConfig | `14-automation-sdn-and-iac.md` sections B--E | Found |
| Terraform/Ansible/NSO/NDFC/device APIs/idempotency/state/drift/testing | `14-automation-sdn-and-iac.md` sections C--E and J--M | Found |
| Observability, tools, counters, captures, hypothesis/falsifier, incidents | `15-observability-troubleshooting-and-design.md` sections C--H | Found |
| SDE2 mechanism and Staff ownership/capacity/migration/system design | `15-observability-troubleshooting-and-design.md` sections G--L and every module’s follow-ups | Found |

## D. Severity-ranked findings

| Severity | Finding | Exact citations | Required approval repair |
| --- | --- | --- | --- |
| **High** | The new lab records are much clearer and safer, but most are state-file models, not mechanism-replayable network fixtures. They mutate declared values and assert those same values; they do not generate or observe the protocol/service behavior the module teaches. | Modules 02--04 sections K/L; module 05 section L/M; modules 06--15 sections K/M. Compare the explicit disclaimer in module 06 M, “does not contact a BGP speaker,” module 12 M, “Provider logs and reachability tools remain unexecuted,” and module 14 M, “does not contact any controller, device, cloud account, or ADC.” | Preserve the safe, no-credential boundary, but add an executable local mechanism fixture for each module (for example namespaces/bridge/FRR/dnsmasq where appropriate, or a deterministic emulator with computed state transitions). It must build the fixture, capture live baseline state, inject one bounded fault, assert the observed symptom from fixture state, repair, prove rollback, and prove no residue even on failure. A labelled conceptual mock may remain as a teaching aid, not the sole replay. |
| **High** | “Completed score” statements are not independently evidenced completed submissions. The rubrics specify the desired artifact/evidence/threshold, while the adjacent prose assigns 100/100 without showing a completed artifact, transcript, or criterion-to-output mapping. This risks teaching learners to confuse an expected result with evidence. | Modules 01--04 section L; module 05 section M; modules 06--15 section L. Representative examples: module 12 L “Completed score”; module 14 L “Completed score”; module 15 L “Completed score.” | Add one fictional but completed lab submission per module. It should name saved topology/config/request artifacts, quote or link the fixture’s observed output, include fault and repair/rollback evidence, then score each rubric row only against that bundle. Keep source labels explicit: local fixture output is observed; vendor read-backs are illustrative unless a documented local emulator supplies them. |
| **High** | The ownership/read-back contract has broad coverage but is not field-level and exclusive enough for a Staff-quality control boundary. Several rows permit “Terraform or” another owner; none give per-field approver and rollback owner. The modules describe request/read-back sequences but do not show paired lab-only request and response/read-back objects with an independently derived data-plane result. | `00-README.md` section G, especially AWS/GCP route and policy rows and Terraform rows; module 10 sections J/K/M; module 11 sections J/K/M; module 12 sections J/K/M; module 14 sections J/K/M. | Add a canonical matrix containing: system, object, individual field/group, single writer, approver, evidence owner, rollback owner, mutation request sample, authoritative read-back sample, and independent data-plane/service assertion. Cover AWS/GCP route/policy/LB/VPN/private connectivity/logging/quota; Terraform state/import/drift/pagination/retry; NSO CDB/task/device; NDFC intent/task/device; F5 AS3/iControl; and A10 REST. Use fictitious IDs and response bodies; explicitly show that the local emulator computes the failed forwarding assertion rather than printing it. |
| **Medium** | Section F is labelled “Atomic concept-to-evidence crosswalk” but holds 15 aggregate module rows. It provides no individual purpose, boundary/adjacent term, module section, or per-concept evidence/falsifier for every Section C term. | `00-README.md` section F; `book/ccna-networking-expansion-todo.md` section C. | Append or replace with one canonical atomic row per Section C concept, including primary module/section, mechanism, purpose, boundary/adjacent term, read-back evidence, and falsifier. Keep the current module map as a concise navigation table if useful. |
| **Medium** | The validator checks structural markers, not the substantive quality gates. It accepts a lab because field words occur, accepts a score because “criterion” or “score” occurs, and does not execute each new lab record or check its no-leak assertion. | `scripts/validate.sh`, CCNA expansion Python block. | Add safe fixture-runner checks and static checks for the atomic crosswalk and evidence-backed worked-submission artifact fields. The validator should not make a semantic approval claim; Terra remains the semantic gate. |
| **Medium** | The TODO says Section C/D implementation gates are complete even though the saved evidence does not meet the quality definitions used in this audit. Section E correctly leaves Terra review unchecked, but the summary wording can be read as closure. | `book/ccna-networking-expansion-todo.md` sections C--E. | Change only evidence states that are justified by the repaired artifacts; retain an explicit “not Terra-approved” status until all high-severity gates close. |
| **Low** | Module 05’s content order is harder to scan than the rest of the collection because the reproducible lab is L and the worked answer is M rather than following the common placement. | `05-routing-static-ospf-and-vrf.md` sections H--M. | Normalize the order or add a short A--M semantic map. This does not block approval once the high-severity gates are met. |

## E. Accepted strengths and prior-blocker progress

- The 26 requested networking categories are all represented with an explicit
  primary home and are substantially more complete than a CCNA-only outline.
- `00-README.md` sections F and G materially improve navigation and cross-track
  thinking. The request-field/read-back table is a sound base for the required
  field-level matrix.
- All modules now state the complete lab lifecycle and label mock versus
  observed behavior. This is an important safety improvement and follows the
  vendor-aware learning policy.
- The 11 fixed-path mock blocks in modules 05--15 were re-executed in this
  audit. They all exited successfully and left no fixed `/tmp/ccnaXX-lab`
  directory. This establishes **safe local replay of the models**, not protocol
  fidelity.
- The prior Python `false` versus `False` fixture defect is repaired.
- The BGP owner/evidence/repair/rollback diagram concern is repaired.
- Provider and product terms are kept separate from portable engineering
  advice in `docs/references.md` and the facts/inferences ledger.

## F. Validation record

Executed from the repository root on 2026-09-01:

~~~text
./scripts/validate.sh                         PASS
python3 examples/request_path.py              PASS
python3 scripts/check_internal_links.py       PASS
git diff --check                              PASS
~~~

The validation suite reported, among other checks:

~~~text
CCNA expansion checks passed: 15 modules and exact index.
Repository structure and Mermaid ASCII checks passed.
Internal Markdown link checks passed.
Markdown heading hierarchy checks passed for all Markdown files.
~~~

The audit also executed the fixed-path local mock blocks in modules 05--15.
All eleven exited `0`; their expected model outputs appeared and no respective
temporary lab directory remained. Modules 01--04 were inspected but their new
reproducible-record prose was not executable as a complete equivalent
mechanism fixture.

## G. Explicit remaining approval gates

The collection can receive an **APPROVED** Terra decision only when all of the
following are visible and verified in the repository:

1. Every module has an executable, safe, local mechanism fixture (or a
   deterministic local emulator that derives behavior from the configured
   state), with setup, live baseline, bounded fault, computed assertion,
   repair, rollback, cleanup, and no-leak proof.
2. Every module has one completed worked submission whose criterion-level score
   is linked to named artifacts and observed fixture evidence, including SDE2
   and Staff follow-up evaluation.
3. The collection contains a field-level, single-writer ownership matrix with
   approver, evidence owner, and rollback owner for AWS/GCP/Terraform/NSO/NDFC/
   F5/A10 objects; each required class has paired illustrative request and
   authoritative read-back records plus a locally computed independent
   data-plane/service assertion.
4. The canonical crosswalk is atomic for every TODO Section C concept and
   includes mechanism, purpose, boundary/adjacent term, primary module/section,
   read-back evidence, and falsifier.
5. `scripts/validate.sh` is strengthened to prevent marker-only closure and
   safely runs the local fixture checks, including no-leak assertions.
6. The TODO evidence states reflect the actual artifacts, all repository checks
   pass again, and a fresh independent Terra audit finds no high-severity
   omission or misleading ownership claim.

Until those gates close, the correct independent quality-gate status is
**NOT APPROVED**.
