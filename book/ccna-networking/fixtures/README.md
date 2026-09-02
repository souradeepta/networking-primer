# CCNA local fixture runner

## A. Purpose and safety

`runner.py` is a deterministic, stdlib-only local mechanism emulator for the
15 modules. It uses fictional addresses, devices, cloud objects, and
controller state. It does not open sockets, require credentials, contact
AWS/GCP, or mutate a network device. The runner injects only control/config
changes. [`evaluator.py`](evaluator.py) derives each forwarding or service
observation from effective control state and an independent traffic fixture;
it never reads a caller-supplied health result.

## B. Lifecycle

Each scenario performs setup, captures a baseline, applies one bounded
control/config fault, records a retained assertion and negative control,
repairs the fault, replays rollback, and proves cleanup. With
`--artifacts-dir`, every run gets a unique write-once v3 bundle under
`observed/runs/<run-id>/modules/<id>/` containing setup,
baseline-readback, fault, assertion, repair-readback, rollback, cleanup, and
a content-hash manifest. Every transaction records desired request,
controller reconciliation result, effective read-back, and device/service
observation. Without that option the capture is temporary and is deleted; no
phase is claimed as retained.

```bash
python3 book/ccna-networking/fixtures/runner.py --all \
  --artifacts-dir book/ccna-networking/fixtures/observed
```

The final line must report `FIXTURE_PASS modules=15
temporary_workspace_removed=True no_leak=True`. **Observed lab result** refers
to a run of this local fixture. The negative-control record intentionally
shows that a metadata-only control change can leave the data plane healthy,
while an evaluator-only mechanism fault can fail it. Ownership probes are
derived from retained effective state and a separate traffic path; no probe
Boolean is accepted from a caller. Provider and vendor API examples elsewhere
remain **illustrative**.

| Scenario | Computed mechanism | Bounded symptom |
| --- | --- | --- |
| 01 | MTU and carrier | `MTU_MISMATCH` |
| 02 | VLAN membership and trunk allowance | `VLAN_TAG_DROPPED` |
| 03 | STP root/blocking state | `STP_LOOP_DETECTED` |
| 04 | NAT translation and IPv6 neighbor state | `NAT_TRANSLATION_MISSING` |
| 05 | OSPF adjacency and route installation | `OSPF_AREA_MISMATCH` |
| 06 | BGP policy and FIB installation | `BGP_PREFIX_FILTERED` |
| 07 | DNS, lease, time, and logging service health | `SERVICE_PLANE_DEGRADED` |
| 08 | ACL, AAA, boot chain, and flow decision | `POLICY_DENY` |
| 09 | RF utilization, marking, and queue behavior | `AIRTIME_OR_QUEUE_CONGESTION` |
| 10 | IGMP/PIM/RPF and VIP health | `MULTICAST_RPF_FAILURE` |
| 11 | EVPN MAC route and VNI state | `EVPN_MAC_ROUTE_MISSING` |
| 12 | Cloud route, policy, and reachability assertion | `CLOUD_ROUTE_OR_POLICY_FAILURE` |
| 13 | Hybrid path and controlled egress | `HYBRID_PATH_FAILOVER_REQUIRED` |
| 14 | Intent/state/device convergence and drift | `DRIFT_DEVICE_READBACK_MISMATCH` |
| 15 | Correlated metric, flow, log, and timeline evidence | `CORRELATED_SLO_BREACH` |
```
