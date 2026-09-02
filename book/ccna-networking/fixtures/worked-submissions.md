# Artifact-backed completed submissions

## A. Evidence contract

Every criterion names a retained artifact, a module-specific JSON pointer, the observed value, a domain threshold, and an explicit threshold decision. No score uses a generic health-only pointer. These are fictional local-emulator submissions; they do not claim AWS, GCP, controller, switch, F5, or A10 execution.

## B. Module 01 — 01-physical-mtu

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `01.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/01/baseline-readback.json#/device_service_observation/observations/path_mtu` | `1500` | `path_mtu >= packet_size` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `01.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/01/fault.json#/device_service_observation/observations/path_mtu` | `900` | `path_mtu < packet_size` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `01.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/01/repair-readback.json#/device_service_observation/observations/path_mtu` | `1500` | `path_mtu >= packet_size` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `01.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/01/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/carrier` | `False` | `carrier == false` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 02 — 02-vlan-trunk

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `02.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/02/baseline-readback.json#/device_service_observation/observations/hop_admission` | `True` | `hop_admission == true` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `02.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/02/fault.json#/device_service_observation/observations/hop_admission` | `False` | `hop_admission == false` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `02.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/02/repair-readback.json#/device_service_observation/observations/hop_admission` | `True` | `hop_admission == true` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `02.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/02/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/hop_admission` | `False` | `hop_admission == false` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 03 — 03-stp-lacp

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `03.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/03/baseline-readback.json#/device_service_observation/observations/cycle_detected` | `False` | `cycle_detected == false` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `03.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/03/fault.json#/device_service_observation/observations/cycle_detected` | `True` | `cycle_detected == true` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `03.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/03/repair-readback.json#/device_service_observation/observations/cycle_detected` | `False` | `cycle_detected == false` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `03.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/03/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/cycle_detected` | `True` | `cycle_detected == true` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 04 — 04-ipv4-nat-ipv6

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `04.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/04/baseline-readback.json#/device_service_observation/observations/translation` | `198.51.100.10` | `translation is present` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `04.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/04/fault.json#/device_service_observation/observations/translation` | `resolved by validator` | `translation is missing` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `04.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/04/repair-readback.json#/device_service_observation/observations/translation` | `198.51.100.10` | `translation is present` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `04.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/04/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/translation` | `resolved by validator` | `translation is missing` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 05 — 05-ospf-vrf

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `05.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/05/baseline-readback.json#/device_service_observation/observations/neighbor_state` | `FULL` | `neighbor_state == FULL` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `05.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/05/fault.json#/device_service_observation/observations/neighbor_state` | `DOWN` | `neighbor_state != FULL` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `05.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/05/repair-readback.json#/device_service_observation/observations/neighbor_state` | `FULL` | `neighbor_state == FULL` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `05.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/05/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/neighbor_state` | `DOWN` | `neighbor_state != FULL` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 06 — 06-bgp-policy

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `06.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/06/baseline-readback.json#/device_service_observation/observations/rib_result` | `FIB` | `rib_result == FIB` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `06.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/06/fault.json#/device_service_observation/observations/rib_result` | `FILTERED` | `rib_result != FIB` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `06.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/06/repair-readback.json#/device_service_observation/observations/rib_result` | `FIB` | `rib_result == FIB` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `06.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/06/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/rib_result` | `FILTERED` | `rib_result != FIB` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 07 — 07-network-services

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `07.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/07/baseline-readback.json#/device_service_observation/observations/dns_ok` | `True` | `dns_ok == true` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `07.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/07/fault.json#/device_service_observation/observations/dns_ok` | `False` | `dns_ok == false` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `07.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/07/repair-readback.json#/device_service_observation/observations/dns_ok` | `True` | `dns_ok == true` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `07.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/07/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/dns_ok` | `False` | `dns_ok == false` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 08 — 08-acl-aaa-security

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `08.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/08/baseline-readback.json#/device_service_observation/observations/ordered_decision` | `ALLOW` | `ordered_decision == ALLOW` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `08.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/08/fault.json#/device_service_observation/observations/ordered_decision` | `UNDECIDED` | `ordered_decision == UNDECIDED` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `08.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/08/repair-readback.json#/device_service_observation/observations/ordered_decision` | `ALLOW` | `ordered_decision == ALLOW` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `08.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/08/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/ordered_decision` | `UNDECIDED` | `ordered_decision == UNDECIDED` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 09 — 09-wireless-qos

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `09.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/09/baseline-readback.json#/device_service_observation/observations/drops` | `0` | `drops == 0` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `09.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/09/fault.json#/device_service_observation/observations/channel_utilization` | `95` | `channel_utilization >= 80` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `09.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/09/repair-readback.json#/device_service_observation/observations/drops` | `0` | `drops == 0` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `09.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/09/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/drops` | `12` | `drops > 0` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 10 — 10-multicast-service-delivery

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `10.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/10/baseline-readback.json#/device_service_observation/observations/rpf_interface` | `uplink-a` | `rpf_interface == uplink-a` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `10.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/10/fault.json#/device_service_observation/observations/rpf_interface` | `uplink-b` | `rpf_interface == uplink-b` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `10.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/10/repair-readback.json#/device_service_observation/observations/rpf_interface` | `uplink-a` | `rpf_interface == uplink-a` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `10.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/10/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/rpf_interface` | `uplink-b` | `rpf_interface == uplink-b` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 11 — 11-vxlan-evpn

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `11.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/11/baseline-readback.json#/device_service_observation/observations/evpn_type2_routes` | `2` | `evpn_type2_routes > 0` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `11.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/11/fault.json#/device_service_observation/observations/evpn_type2_routes` | `0` | `evpn_type2_routes == 0` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `11.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/11/repair-readback.json#/device_service_observation/observations/evpn_type2_routes` | `2` | `evpn_type2_routes > 0` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `11.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/11/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/underlay_reachable` | `False` | `underlay_reachable == false` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 12 — 12-cloud-networking

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `12.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/12/baseline-readback.json#/device_service_observation/observations/forwarding_next_hop` | `transit` | `forwarding_next_hop == transit` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `12.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/12/fault.json#/device_service_observation/observations/forwarding_next_hop` | `blackhole` | `forwarding_next_hop == blackhole` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `12.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/12/repair-readback.json#/device_service_observation/observations/forwarding_next_hop` | `transit` | `forwarding_next_hop == transit` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `12.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/12/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/backend_listener` | `False` | `backend_listener == false` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 13 — 13-private-public-hybrid

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `13.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/13/baseline-readback.json#/device_service_observation/observations/selected_path` | `private-a` | `selected_path == private-a` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `13.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/13/fault.json#/device_service_observation/observations/service_listener` | `False` | `service_listener == false` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `13.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/13/repair-readback.json#/device_service_observation/observations/selected_path` | `private-a` | `selected_path == private-a` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `13.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/13/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/service_listener` | `False` | `service_listener == false` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 14 — 14-automation-iac

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `14.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/14/baseline-readback.json#/device_service_observation/observations/device_route` | `route-allow` | `device_route == route-allow` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `14.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/14/fault.json#/device_service_observation/observations/device_route` | `route-deny` | `device_route == route-deny` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `14.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/14/repair-readback.json#/device_service_observation/observations/device_route` | `route-allow` | `device_route == route-allow` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `14.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/14/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/device_route` | `route-deny` | `device_route == route-deny` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## B. Module 15 — 15-observability-design

**Score:** `25 + 25 + 25 + 25 = 100/100`; status: **completed-local-emulator-submission**

| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `15.C1` | `runs/20260902T031542.717447Z-c145ed02/modules/15/baseline-readback.json#/device_service_observation/observations/metric_ms` | `10` | `metric_ms < 50` | **PASS** | `25/25` | Name the module-specific read-back and its falsifier. | Assign ownership, SLO, and failure-domain budget. |
| `15.C2` | `runs/20260902T031542.717447Z-c145ed02/modules/15/fault.json#/device_service_observation/observations/timeline_complete` | `False` | `timeline_complete == false` | **PASS** | `25/25` | Explain the mechanism-specific symptom and a competing hypothesis. | Define blast radius, approval boundary, and escalation trigger. |
| `15.C3` | `runs/20260902T031542.717447Z-c145ed02/modules/15/repair-readback.json#/device_service_observation/observations/metric_ms` | `10` | `metric_ms < 50` | **PASS** | `25/25` | Describe the repair and reconciliation evidence proving convergence. | Choose rollback criteria and recovery authority. |
| `15.C4` | `runs/20260902T031542.717447Z-c145ed02/modules/15/assertion.json#/negative_control/independent_path_change/evaluator_output/observations/timeline_complete` | `False` | `timeline_complete == false` | **PASS** | `25/25` | Explain why an accepted request cannot prove forwarding success. | Define an independent service SLO and evidence-retention policy. |

## C. Scoring and labels

A criterion fails if its artifact or JSON pointer is missing, stale, or does not resolve to a value satisfying its module-specific threshold. **Observed** means generated by the local mechanism evaluator. **Derived probe** means calculated from effective state and a separate traffic path. Provider and vendor request examples are **illustrative**.
