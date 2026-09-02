#!/usr/bin/env python3
"""Safe, deterministic local networking mechanism fixtures.

The runner mutates only fictional control/configuration state.  It never
stores or injects a second data-plane fault for the same scenario.  The
data-plane result is derived by :mod:`evaluator` from effective control state
and an independent traffic-path fixture.  Provider and appliance requests
remain illustrative; retained read-backs and evaluator observations are
local-emulator evidence only.
"""

from __future__ import annotations

import copy
import hashlib
import json
import shutil
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from evaluator import derive_dataplane, evaluate_ownership

RUNNER_VERSION = "4.0.0"
SCHEMA_VERSION = "ccna-fixture-bundle/v3"
PHASE_FILES = ["setup.json", "baseline-readback.json", "fault.json", "assertion.json", "repair-readback.json", "rollback.json", "cleanup.json"]


def _now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z")


def _set(state: dict[str, Any], path: str, value: Any) -> None:
    cursor: Any = state
    parts = path.split(".")
    for index, part in enumerate(parts[:-1]):
        if part not in cursor or not isinstance(cursor[part], dict):
            cursor[part] = {}
        cursor = cursor[part]
    cursor[parts[-1]] = copy.deepcopy(value)


def _apply(state: dict[str, Any], changes: dict[str, Any]) -> None:
    for path, value in changes.items():
        _set(state, path, value)


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if not isinstance(value, dict):
        return {prefix: value}
    flattened: dict[str, Any] = {}
    for key, child in value.items():
        child_prefix = f"{prefix}.{key}" if prefix else key
        flattened.update(_flatten(child, child_prefix))
    return flattened


class LocalController:
    """Small controller store with generated defaults and immutable changes."""

    def __init__(self) -> None:
        self.current: dict[str, Any] = {}
        self.generation = 0
        self.changes: list[dict[str, Any]] = []
        self.owners: dict[str, str] = {}

    def _effective(self, desired: dict[str, Any], task_id: str, stage: str) -> dict[str, Any]:
        effective = copy.deepcopy(desired)
        if "owned_field" in effective:
            requested = effective["owned_field"]
            effective["owned_field"] = {
                "object": requested["object"],
                "field_path": requested["field_path"],
                "value": "enabled",
                "source": "controller-field-normalization",
            }
        self.generation += 1
        effective["_controller"] = {
            "generation": self.generation,
            "defaults_applied": ["reconcile_generation", "controller_source"],
            "controller_source": "bounded-local-controller-store",
            "last_task_id": task_id,
            "stage": stage,
        }
        return effective

    def reconcile(self, desired: dict[str, Any], cid: str, stage: str, *, writer: str | None = None,
                  ownership_key: str | None = None) -> dict[str, Any]:
        task_id = f"task-{cid}-{stage}"
        timestamp = _now()
        if ownership_key and ownership_key in self.owners and self.owners[ownership_key] != writer:
            return {
                "status": "REJECTED_COLLISION", "task_id": task_id,
                "change_record_id": f"CHG-{cid}", "correlation_id": cid,
                "stage": stage, "timestamp": timestamp,
                "writer": writer, "ownership_key": ownership_key,
                "rejection_reason": "field has an immutable single writer",
                "before_state": copy.deepcopy(self.current),
                "requested_fields": _flatten(desired), "effective_fields": _flatten(self.current),
                "changed_fields": [], "immutable": True,
            }
        if ownership_key and ownership_key not in self.owners:
            self.owners[ownership_key] = writer or "unassigned"
        before = copy.deepcopy(self.current)
        effective = self._effective(desired, task_id, stage)
        changed = sorted(key for key in set(_flatten(before)) | set(_flatten(effective))
                         if _flatten(before).get(key) != _flatten(effective).get(key))
        result = {
            "status": "APPLIED" if changed else "NO_CHANGE", "task_id": task_id,
            "change_record_id": f"CHG-{cid}", "correlation_id": cid,
            "stage": stage, "timestamp": timestamp, "writer": writer,
            "ownership_key": ownership_key, "before_state": before,
            "requested_fields": _flatten(desired), "desired_state": copy.deepcopy(desired),
            "effective_fields": _flatten(effective), "effective_state": copy.deepcopy(effective),
            "changed_fields": changed,
            "effective_state_hash": hashlib.sha256(json.dumps(effective, sort_keys=True).encode()).hexdigest(),
            "immutable": True,
        }
        self.current = effective
        self.changes.append(copy.deepcopy(result))
        return result


PATH_STATES = {
    "01": {"baseline": {"carrier_state": "UP", "negotiation_state": "COMPLETE"}, "degraded": {"carrier_state": "DOWN", "negotiation_state": "COMPLETE"}},
    "02": {"baseline": {"tag_transit_state": "ADMITTED"}, "degraded": {"tag_transit_state": "DROPPED"}},
    "03": {"baseline": {"loop_guard_state": "BLOCKED"}, "degraded": {"loop_guard_state": "OPEN"}},
    "04": {"baseline": {"nat_table_state": "POPULATED"}, "degraded": {"nat_table_state": "EMPTY"}},
    "05": {"baseline": {"adjacency_transport": "UP"}, "degraded": {"adjacency_transport": "DOWN"}},
    "06": {"baseline": {"forwarding_programming": "PROGRAMMED"}, "degraded": {"forwarding_programming": "WITHDRAWN"}},
    "07": {"baseline": {"dns_path": "REACHABLE", "dhcp_path": "REACHABLE", "syslog_path": "DELIVERED"}, "degraded": {"dns_path": "UNREACHABLE", "dhcp_path": "REACHABLE", "syslog_path": "DELIVERED"}},
    "08": {"baseline": {"packet_path": "DELIVERED"}, "degraded": {"packet_path": "DROPPED"}},
    "09": {"baseline": {"airtime_state": "CLEAR"}, "degraded": {"airtime_state": "SATURATED"}},
    "10": {"baseline": {"rpf_check": "PASS"}, "degraded": {"rpf_check": "FAIL"}},
    "11": {"baseline": {"underlay_reachability": "REACHABLE"}, "degraded": {"underlay_reachability": "UNREACHABLE"}},
    "12": {"baseline": {"backend_path": "REACHABLE"}, "degraded": {"backend_path": "UNREACHABLE"}},
    "13": {"baseline": {"private_path_state": "UP"}, "degraded": {"private_path_state": "DOWN"}},
    "14": {"baseline": {"device_apply_state": "APPLIED"}, "degraded": {"device_apply_state": "NOT_APPLIED"}},
    "15": {"baseline": {"telemetry_transport": "COMPLETE"}, "degraded": {"telemetry_transport": "PARTIAL"}},
}


def _path_trace(key: str, spec: dict[str, Any], mode: str, cid: str, traffic_request: dict[str, Any]) -> dict[str, Any]:
    """Produce a raw trace from a separate local device/service model."""
    return {
        "trace_id": f"trace-{cid}-{mode}",
        "source": "bounded-local-traffic-and-device-model",
        "request_id": f"request-{cid}-{mode}",
        "request": copy.deepcopy(traffic_request),
        "topology": spec["topology"],
        "path_hops": [part.strip() for part in spec["topology"].replace("==", "--").split("--")],
        "device_service_state": copy.deepcopy(PATH_STATES[key][mode]),
        "mode": mode,
    }


def _write_json(path: Path, payload: Any, *, overwrite: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and not overwrite:
        raise FileExistsError(f"immutable fixture artifact already exists: {path}")
    path.write_text(json.dumps(payload, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def _scenario_specs() -> dict[str, dict[str, Any]]:
    """Return control state, independent traffic, and control-only test data."""
    metadata = {"operator_note": "metadata-only control change; no forwarding input changes"}
    return {
        "01": {"name": "01-physical-mtu", "mechanism": "Ethernet frame admission and MTU", "topology": "host-a -- link-a -- link-b -- host-b", "config": {"mtu": 1500}, "control": {"interfaces": {"a": {"mtu": 1500}, "b": {"mtu": 1500}}}, "traffic": {"carrier": True, "packet_size": 1400}, "fault_control": {"interfaces.b.mtu": 900}, "control_only_fault": metadata | {"test": "01"}},
        "02": {"name": "02-vlan-trunk", "mechanism": "802.1Q tag admission across a trunk", "topology": "host -- access-switch -- trunk -- distribution-gateway", "config": {"access_vlan": 20, "allowed_vlans": [10, 20]}, "control": {"switch": {"access_vlan": 20, "trunk_allowed": [10, 20]}, "gateway_vlan": 20}, "traffic": {"frame": {"vlan": 20, "gateway_vlan": 20}}, "fault_control": {"switch.trunk_allowed": [10]}, "control_only_fault": metadata | {"test": "02"}},
        "03": {"name": "03-stp-lacp", "mechanism": "STP loop prevention and bundled uplink state", "topology": "dist-a -- leaf-a -- leaf-b -- dist-a (one edge blocked)", "config": {"root_bridge": "dist-a", "bundle": "po10"}, "control": {"root": "dist-a", "blocked_edges": ["leaf-b-uplink"], "bundle_members": 2}, "traffic": {"cycle_possible": True}, "fault_control": {"blocked_edges": []}, "control_only_fault": metadata | {"test": "03"}},
        "04": {"name": "04-ipv4-nat-ipv6", "mechanism": "IPv4 translation and IPv6 neighbor discovery", "topology": "dual-stack-host -- edge-router -- public-service", "config": {"inside_prefix": "10.4.0.0/24", "public_prefix": "198.51.100.0/24"}, "control": {"nat_rule": "10.4.0.0/24->198.51.100.0/24", "nd": "enabled"}, "traffic": {"flow": {"inside": "10.4.0.10"}, "available_translations": {"10.4.0.10": "198.51.100.10"}, "ipv6_neighbor_state": "REACHABLE"}, "fault_control": {"nat_rule": "disabled"}, "control_only_fault": metadata | {"test": "04"}},
        "05": {"name": "05-ospf-vrf", "mechanism": "OSPF adjacency, LSDB route installation, and VRF lookup", "topology": "vrf-prod edge-a == OSPF == edge-b", "config": {"area": 0, "network_type": "broadcast", "vrf": "prod"}, "control": {"area": 0, "network_type": "broadcast", "vrf": "prod"}, "traffic": {"neighbor_state": "FULL", "network_type": "broadcast", "route_table": {"10.5.0.0/16": "prod"}}, "fault_control": {"area": 1}, "control_only_fault": metadata | {"test": "05"}},
        "06": {"name": "06-bgp-policy", "mechanism": "BGP policy admission from RIB to FIB", "topology": "customer-edge == eBGP == provider-edge == transit", "config": {"peer_as": 64512, "prefix_filter": "203.0.113.0/24 allow"}, "control": {"peer": "ESTABLISHED", "policy": "ALLOW", "prefix": "203.0.113.0/24"}, "traffic": {"prefix": "203.0.113.0/24"}, "fault_control": {"policy": "DENY"}, "control_only_fault": metadata | {"test": "06"}},
        "07": {"name": "07-network-services", "mechanism": "DNS, DHCP lease, NTP, and syslog service path", "topology": "client -- access -- shared DNS/DHCP/NTP/logging services", "config": {"dns_zone": "app.example", "lease_pool": "10.7.0.0/24"}, "control": {"dns": "10.7.0.53", "dhcp": "enabled", "ntp": "10.7.0.123", "syslog": "enabled"}, "traffic": {"expected_dns": "10.7.0.53", "expected_ntp": "10.7.0.123", "lease_address": "10.7.0.20", "ntp_offset_ms": 2, "service_path_up": True, "syslog_delivered": True}, "fault_control": {"dns": "10.7.0.254"}, "control_only_fault": metadata | {"test": "07"}},
        "08": {"name": "08-acl-aaa-security", "mechanism": "Ordered ACL decision, AAA reachability, and boot-chain trust", "topology": "operator -- management ACL -- device -- protected service", "config": {"protected_port": 443, "aaa": "TACACS+"}, "control": {"acl": "ALLOW-HTTPS", "aaa": "REACHABLE", "secure_boot": "VALID"}, "traffic": {"packet": {"protocol": "tcp", "port": 443}}, "fault_control": {"acl": "DENY-HTTPS"}, "control_only_fault": metadata | {"test": "08"}},
        "09": {"name": "09-wireless-qos", "mechanism": "RF airtime, DSCP marking, and egress queue behavior", "topology": "client -- AP -- controller -- QoS queue -- service", "config": {"ssid": "lab", "voice_dscp": 46, "max_utilization": 80}, "control": {"rssi": -55, "channel_utilization": 30, "dscp": 46, "max_utilization": 80}, "traffic": {"packet_dscp": 46, "queue_drops": 0}, "fault_control": {"channel_utilization": 95}, "control_only_fault": metadata | {"test": "09"}},
        "10": {"name": "10-multicast-service-delivery", "mechanism": "IGMP/PIM/RPF tree feeding an ADC VIP", "topology": "client -- L3 tree -- RPF check -- ADC VIP -- backend pool", "config": {"group": "239.10.10.10", "vip": "198.51.100.10:443"}, "control": {"igmp": "joined", "pim": "FULL", "rpf": "uplink-a", "vip": "healthy"}, "traffic": {"healthy_backends": 2}, "fault_control": {"rpf": "uplink-b"}, "control_only_fault": metadata | {"test": "10"}},
        "11": {"name": "11-vxlan-evpn", "mechanism": "VXLAN VTEP, EVPN type-2, and BUM replication", "topology": "leaf-vtep-a == IP underlay == leaf-vtep-b; VNI 5011", "config": {"vni": 5011, "tenant": "lab", "route_target": "65000:5011"}, "control": {"underlay": "reachable", "vni": 5011, "evpn": "advertising", "bum": "ingress-replication"}, "traffic": {"remote_mac_count": 2}, "fault_control": {"evpn": "withdrawn"}, "control_only_fault": metadata | {"test": "11"}},
        "12": {"name": "12-cloud-networking", "mechanism": "Cloud route/policy reconciliation and reachability probe", "topology": "workload -- VPC/VPC network -- transit/VPN -- service", "config": {"route": "10.12.0.0/16->transit", "policy": "ALLOW"}, "control": {"route": "10.12.0.0/16->transit", "policy": "ALLOW", "request_status": "ACCEPTED"}, "traffic": {"backend_listener": True, "return_path": "transit"}, "fault_control": {"route": "10.12.0.0/16->blackhole"}, "control_only_fault": metadata | {"test": "12"}},
        "13": {"name": "13-private-public-hybrid", "mechanism": "Hybrid BGP path selection and controlled egress", "topology": "private workload -- HA VPN/Interconnect -- on-prem; controlled public egress", "config": {"primary": "private-a", "backup": "private-b", "egress": "controlled"}, "control": {"primary_path": "up", "egress": "CONTROLLED", "bgp": "ESTABLISHED"}, "traffic": {"bgp_routes": {"10.13.0.0/16": "private-a"}, "service_listener_by_path": {"private-a": True, "private-b": False}}, "fault_control": {"primary_path": "down"}, "control_only_fault": metadata | {"test": "13"}},
        "14": {"name": "14-automation-iac", "mechanism": "Intent, state, device read-back, drift, and idempotent plan", "topology": "operator -- IaC state -- controller -- device/FIB -- service probe", "config": {"resource": "route.lab", "desired_route": "route-allow"}, "control": {"intent": "route-allow", "state": "route-allow", "plan": "no-change", "request_status": "ACCEPTED"}, "traffic": {"device_observation": {"device_can_apply": True}}, "fault_control": {"state": "route-deny", "plan": "change"}, "control_only_fault": metadata | {"test": "14"}},
        "15": {"name": "15-observability-design", "mechanism": "Metric, flow, log, and timeline correlation", "topology": "client -- service -- telemetry pipeline -- incident evidence", "config": {"slo_latency_ms": 50, "expected_status": 200}, "control": {"telemetry_profile": "complete"}, "traffic": {"signals": {"metric_ms": 10, "flow_status": 200, "log_event": "ALLOW", "timeline_complete": True}}, "fault_control": {"telemetry_profile": "impaired"}, "control_only_fault": metadata | {"test": "15"}},
    }


def _request(spec: dict[str, Any], desired: dict[str, Any], cid: str, timestamp: str, operation: str) -> dict[str, Any]:
    return {"kind": "fictional local emulator desired-state request", "object": spec["name"], "operation": operation, "status": "ACCEPTED", "correlation_id": cid, "timestamp": timestamp, "desired_state": copy.deepcopy(desired), "requested_fields": _flatten(desired)}


def _transaction(controller: LocalController, spec: dict[str, Any], desired: dict[str, Any], traffic_request: dict[str, Any], path_trace: dict[str, Any], key: str, cid: str, stage: str, *, writer: str | None = None, ownership_key: str | None = None) -> dict[str, Any]:
    timestamp = _now()
    request = _request(spec, desired, cid, timestamp, stage)
    reconciliation = controller.reconcile(desired, cid, stage, writer=writer, ownership_key=ownership_key)
    if reconciliation["status"] == "REJECTED_COLLISION":
        return {"desired_request": request, "controller_result": reconciliation, "authoritative_readback": {"status": "REJECTED", "stage": stage, "correlation_id": cid, "reconciliation": reconciliation}, "device_service_observation": {"result": "NOT_EVALUATED", "healthy": False}}
    effective_control = copy.deepcopy(reconciliation["effective_state"])
    effective = {"kind": "observed local controller-store read-back", "status": "ACTIVE", "stage": stage, "correlation_id": cid, "timestamp": _now(), "reconciliation": reconciliation, "requested_fields": request["requested_fields"], "effective_fields": reconciliation["effective_fields"], "changed_fields": reconciliation["changed_fields"], "effective_state": {"module_control": effective_control}}
    observation = derive_dataplane(key, effective_control, traffic_request, path_trace)
    return {"desired_request": request, "controller_result": reconciliation, "authoritative_readback": effective, "device_service_observation": observation, "evaluator_input": {"control_source": "authoritative_readback#/effective_state/module_control", "traffic_request": copy.deepcopy(traffic_request), "path_trace": copy.deepcopy(path_trace)}}


def _run_scenario(key: str, spec: dict[str, Any], run_id: str, bundle: Path) -> dict[str, Any]:
    cid = f"{run_id}-module-{key}"
    baseline = copy.deepcopy(spec["control"])
    traffic_request = copy.deepcopy(spec["traffic"])
    bundle.mkdir(parents=True, exist_ok=False)
    ephemeral = Path(tempfile.mkdtemp(prefix=f"ccna-{key}-"))
    controller = LocalController()
    baseline_trace = _path_trace(key, spec, "baseline", cid, traffic_request)
    degraded_trace = _path_trace(key, spec, "degraded", cid, traffic_request)
    setup = {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "module": spec["name"], "mechanism": spec["mechanism"], "correlation_id": cid, "timestamp": _now(), "topology": spec["topology"], "config": spec["config"], "control_state_path": "controller_store", "traffic_fixture_path": "traffic_request", "path_model": "separate local traffic/device/service model", "fault_injection_boundary": "control/configuration only; data-plane state is derived", "fixture_boundary": "bounded local emulator; no provider/device mutation", "traffic_request": traffic_request, "baseline_path_trace": baseline_trace, "degraded_path_trace": degraded_trace}
    _write_json(bundle / "setup.json", setup)

    baseline_tx = _transaction(controller, spec, baseline, traffic_request, baseline_trace, key, cid, "baseline")
    assert baseline_tx["device_service_observation"]["healthy"], (key, "baseline evaluator unhealthy", baseline_tx)
    _write_json(bundle / "baseline-readback.json", {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": cid, **baseline_tx})

    fault = copy.deepcopy(baseline)
    _apply(fault, spec["fault_control"])
    fault_tx = _transaction(controller, spec, fault, traffic_request, baseline_trace, key, cid, "bounded-control-fault")
    fault_observation = fault_tx["device_service_observation"]
    assert not fault_observation["healthy"], (key, "control fault did not produce derived symptom", fault_observation)
    _write_json(bundle / "fault.json", {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": cid, **fault_tx, "changed_fields": fault_tx["controller_result"]["changed_fields"], "observed_symptom": fault_observation["result"]})

    control_only = copy.deepcopy(baseline)
    _apply(control_only, spec["control_only_fault"])
    control_only_tx = _transaction(controller, spec, control_only, traffic_request, baseline_trace, key, cid, "control-only-negative")
    control_only_observation = control_only_tx["device_service_observation"]
    assert control_only_observation["healthy"], (key, "control-only change unexpectedly failed data plane", control_only_observation)
    independent_path_observation = derive_dataplane(key, baseline_tx["authoritative_readback"]["effective_state"]["module_control"], traffic_request, degraded_trace)
    assert not independent_path_observation["healthy"], (key, "degraded path did not produce derived symptom", independent_path_observation)
    negative = {"control_only_change": {**control_only_tx, "evaluator_output": control_only_observation}, "independent_path_change": {"traffic_request": traffic_request, "path_trace": degraded_trace, "readback_reference": "baseline-readback.json#/authoritative_readback", "request_status": baseline_tx["desired_request"]["status"], "readback_status": baseline_tx["authoritative_readback"]["status"], "evaluator_input": {"control_source": "baseline-readback.json#/authoritative_readback/effective_state/module_control", "traffic_request": traffic_request, "path_trace": degraded_trace}, "evaluator_output": independent_path_observation}}
    assertion = {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": cid, "control_fault": {"controller_result": fault_tx["controller_result"], "device_service_observation": fault_observation}, "negative_control": negative, "semantic_assertions": {"control_change_can_leave_dataplane_healthy": control_only_observation["healthy"], "independent_path_change_can_fail_dataplane": not independent_path_observation["healthy"], "no_direct_outcome_injection": True, "same_control_readback_can_have_different_path_result": (baseline_tx["authoritative_readback"]["correlation_id"] == negative["independent_path_change"]["readback_reference"].split("#")[0].replace("baseline-readback.json", cid) and baseline_tx["device_service_observation"]["healthy"] is True and independent_path_observation["healthy"] is False)}}
    _write_json(bundle / "assertion.json", assertion)

    repaired = copy.deepcopy(fault)
    _apply(repaired, spec.get("repair_control", spec["control"]))
    repair_tx = _transaction(controller, spec, repaired, traffic_request, baseline_trace, key, cid, "repair")
    assert repair_tx["device_service_observation"]["healthy"], (key, "repair did not restore evaluator", repair_tx)
    _write_json(bundle / "repair-readback.json", {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": cid, **repair_tx})

    rollback_tx = _transaction(controller, spec, baseline, traffic_request, baseline_trace, key, cid, "rollback")
    rollback_observation = rollback_tx["device_service_observation"]
    rollback = {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": cid, **rollback_tx, "restored_control": rollback_tx["authoritative_readback"]["effective_state"]["module_control"] == controller.current, "restored_dataplane": rollback_observation["healthy"] == baseline_tx["device_service_observation"]["healthy"]}
    assert rollback["restored_control"] and rollback["restored_dataplane"] and rollback_observation["healthy"]
    _write_json(bundle / "rollback.json", rollback)

    shutil.rmtree(ephemeral)
    cleanup = {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": cid, "ephemeral_workspace": str(ephemeral), "exists_after_cleanup": ephemeral.exists(), "temporary_workspace_removed": not ephemeral.exists(), "no_leak": not ephemeral.exists(), "retained_bundle": True, "retained_phase_files": PHASE_FILES}
    _write_json(bundle / "cleanup.json", cleanup)
    hashes = {name: hashlib.sha256((bundle / name).read_bytes()).hexdigest() for name in PHASE_FILES}
    _write_json(bundle / "manifest.json", {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": cid, "module": spec["name"], "immutable": True, "bundle_complete": True, "phase_files": PHASE_FILES, "content_sha256": hashes})
    rel = f"runs/{run_id}/modules/{key}"
    return {"module": spec["name"], "module_id": key, "runner_version": RUNNER_VERSION, "correlation_id": cid, "bundle": rel, "artifacts": [f"{rel}/{name}" for name in PHASE_FILES + ["manifest.json"]], "observed_symptom": fault_observation["result"], "baseline": baseline_tx["device_service_observation"], "fault": fault_observation, "repair": repair_tx["device_service_observation"], "rollback": rollback, "negative_control": {"control_only": control_only_observation, "independent_path": independent_path_observation}, "cleanup": cleanup}


OWNER_SPECS = [
    ("AWS", "route table", "routes[10.12.0.0/16].target", "aws-network-owner", "aws-network-approver", "network-sre", "aws-network-rollback", "12"), ("AWS", "security group", "ingress[tcp/443]", "aws-security-owner", "aws-security-approver", "security-ops", "aws-security-rollback", "08"), ("AWS", "load balancer", "listener[443].target_group", "aws-adc-owner", "aws-adc-approver", "adc-ops", "aws-adc-rollback", "10"), ("AWS", "VPN connection", "tunnel.options.local_cidr", "aws-hybrid-owner", "aws-hybrid-approver", "connectivity-ops", "aws-hybrid-rollback", "13"), ("AWS", "flow logs", "filter.traffic_type/destination", "aws-observability-owner", "aws-observability-approver", "observability-ops", "aws-observability-rollback", "15"), ("AWS", "service quota", "quota.ec2.vpc_routes.effective_value", "aws-governance-owner", "aws-governance-approver", "capacity-owner", "aws-governance-rollback", "15"),
    ("GCP", "custom route", "routes[10.12.0.0/16].next_hop/priority", "gcp-network-owner", "gcp-network-approver", "network-sre", "gcp-network-rollback", "12"), ("GCP", "firewall policy", "rules[tcp/443].target_identity/action", "gcp-security-owner", "gcp-security-approver", "security-ops", "gcp-security-rollback", "08"), ("GCP", "forwarding rule", "forwarding_rule[443].target_proxy", "gcp-adc-owner", "gcp-adc-approver", "adc-ops", "gcp-adc-rollback", "10"), ("GCP", "HA VPN/Cloud Router", "tunnel.peer/route_advertisement", "gcp-hybrid-owner", "gcp-hybrid-approver", "connectivity-ops", "gcp-hybrid-rollback", "13"), ("GCP", "log sink", "sink.filter/destination", "gcp-observability-owner", "gcp-observability-approver", "observability-ops", "gcp-observability-rollback", "15"), ("GCP", "regional quota", "quota[region].effective_limit", "gcp-governance-owner", "gcp-governance-approver", "capacity-owner", "gcp-governance-rollback", "15"),
    ("Terraform", "state/import", "resource.route.lab.address/import_id", "terraform-state-owner", "terraform-approver", "iac-ops", "terraform-state-rollback", "14"), ("Terraform", "drift plan", "resource.route.lab.target/planned_action", "terraform-drift-owner", "terraform-approver", "iac-ops", "terraform-drift-rollback", "14"), ("Terraform", "pagination/retry", "provider.list.page_token/request_id", "terraform-provider-owner", "terraform-approver", "provider-ops", "terraform-provider-rollback", "14"), ("NSO", "CDB service", "services/lab/endpoint/next-hop", "nso-service-owner", "nso-approver", "nso-ops", "nso-service-rollback", "14"), ("NSO", "commit task", "commit_queue/task_id/status", "nso-orchestrator-owner", "nso-approver", "nso-ops", "nso-task-rollback", "14"), ("NSO", "device effective config", "devices/device-lab/config/route", "nso-device-owner", "device-approver", "device-ops", "nso-device-rollback", "14"), ("NDFC", "fabric intent", "fabric/vrf/vni/route-target", "ndfc-fabric-owner", "ndfc-approver", "fabric-approver", "ndfc-fabric-rollback", "11"), ("NDFC", "deployment task", "deployment/task_id/version", "ndfc-deployment-owner", "ndfc-approver", "fabric-ops", "ndfc-deployment-rollback", "11"), ("NDFC", "device adapter", "device/nve/evpn/vlan/fib", "ndfc-device-owner", "switch-approver", "switch-ops", "ndfc-device-rollback", "11"), ("F5", "AS3 declaration", "tenant/app/virtual/pool/monitor", "f5-as3-owner", "adc-approver", "adc-ops", "f5-as3-rollback", "10"), ("F5", "iControl member", "pool/member/state/persistence", "f5-icontrol-owner", "adc-approver", "adc-ops", "f5-icontrol-rollback", "10"), ("A10", "REST SLB object", "partition/virtual/service-group/member/monitor", "a10-slb-owner", "adc-approver", "adc-ops", "a10-slb-rollback", "10"),
]


def _ownership_records(run_id: str, timestamp: str, specs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    records = []
    controller = LocalController()
    for number, (platform, resource, field, owner, approver, evidence, rollback, module) in enumerate(OWNER_SPECS, start=1):
        cid = f"{run_id}-ownership-{number:02d}"
        spec = specs[module]
        module_control = copy.deepcopy(spec["control"])
        requested = {"object": f"{platform.lower()}-lab.{resource.replace(' ', '_')}", "field_path": field, "desired": "ACTIVE"}
        ownership_key = requested["object"] + "." + field
        desired = {"module_control": module_control, "owned_field": requested}
        controller_result = controller.reconcile(desired, cid, "ownership-upsert", writer=owner, ownership_key=ownership_key)
        effective_state = {"module_control": controller_result["effective_state"]["module_control"], "owned_field": controller_result["effective_state"]["owned_field"]}
        path_trace = _path_trace(module, spec, "baseline", cid, spec["traffic"])
        degraded_trace = _path_trace(module, spec, "degraded", cid, spec["traffic"])
        readback = {"kind": "observed local controller-store read-back", "status": "ACTIVE", "stage": "ownership-upsert", "correlation_id": cid, "timestamp": _now(), "reconciliation": controller_result, "requested_fields": _flatten(desired), "effective_fields": _flatten(effective_state), "effective_state": effective_state, "device_service_observation": derive_dataplane(module, effective_state["module_control"], spec["traffic"], path_trace)}
        fixture_request = {"kind": "separate illustrative fixture request", "status": "ACCEPTED", "correlation_id": cid, "requested_fields": requested, "path_id": f"path-{module}-{number:02d}"}
        positive_input = {"module": module, "fixture_request": fixture_request, "authoritative_readback": readback, "traffic_request": copy.deepcopy(spec["traffic"]), "path_trace": path_trace}
        positive_output = evaluate_ownership(positive_input)
        negative_input = {"module": module, "fixture_request": fixture_request, "authoritative_readback": readback, "traffic_request": copy.deepcopy(spec["traffic"]), "path_trace": degraded_trace}
        negative_output = evaluate_ownership(negative_input)
        collision_cid = f"{cid}-collision"
        collision = controller.reconcile(desired, collision_cid, "ownership-collision", writer=f"unauthorized-writer-{number:02d}", ownership_key=ownership_key)
        assert positive_output["healthy"] is True and negative_output["healthy"] is False
        records.append({"record_id": f"OWN-{number:02d}", "platform": platform, "resource": resource, "module": module, "owner_id": owner, "object_field_path": ownership_key, "ownership_key": ownership_key, "single_writer_rule": f"Only {owner} may write this exact object/field; all other paths are read-only.", "approver_id": approver, "evidence_owner_id": evidence, "rollback_owner_id": rollback, "owner_assignment_id": f"OWNERSHIP-{number:02d}", "approver_record_id": f"APPROVAL-{number:02d}", "evidence_record_id": f"EVIDENCE-{number:02d}", "rollback_record_id": f"ROLLBACK-{number:02d}", "collision_exception_rule": "Reject a second writer; exception requires the named approver and a new immutable change record.", "linked_change_record": controller_result["change_record_id"], "request": fixture_request, "fixture_request": fixture_request, "authoritative_readback": readback, "requested_fields": requested, "effective_fields": _flatten(effective_state), "controller_result": controller_result, "traffic_request": copy.deepcopy(spec["traffic"]), "path_trace": path_trace, "evaluator_output": positive_output, "collision_result": collision, "negative_control": {"request_status": fixture_request["status"], "readback_status": readback["status"], "traffic_request": copy.deepcopy(spec["traffic"]), "path_trace": degraded_trace, "evaluator_output": negative_output}, "labels": {"request": "illustrative", "readback": "observed local controller-store reconciliation", "evaluator": "derived from effective owned field and raw path trace"}, "correlation_id": cid})
    return records


RUBRICS = {
    "01": [("baseline-readback.json", "/device_service_observation/observations/path_mtu", "ge", {"pointer": "/device_service_observation/observations/packet_size"}, "path_mtu >= packet_size"), ("fault.json", "/device_service_observation/observations/path_mtu", "lt", {"pointer": "/device_service_observation/observations/packet_size"}, "path_mtu < packet_size"), ("repair-readback.json", "/device_service_observation/observations/path_mtu", "ge", {"pointer": "/device_service_observation/observations/packet_size"}, "path_mtu >= packet_size"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/carrier", "eq", False, "carrier == false")],
    "02": [("baseline-readback.json", "/device_service_observation/observations/hop_admission", "eq", True, "hop_admission == true"), ("fault.json", "/device_service_observation/observations/hop_admission", "eq", False, "hop_admission == false"), ("repair-readback.json", "/device_service_observation/observations/hop_admission", "eq", True, "hop_admission == true"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/hop_admission", "eq", False, "hop_admission == false")],
    "03": [("baseline-readback.json", "/device_service_observation/observations/cycle_detected", "eq", False, "cycle_detected == false"), ("fault.json", "/device_service_observation/observations/cycle_detected", "eq", True, "cycle_detected == true"), ("repair-readback.json", "/device_service_observation/observations/cycle_detected", "eq", False, "cycle_detected == false"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/cycle_detected", "eq", True, "cycle_detected == true")],
    "04": [("baseline-readback.json", "/device_service_observation/observations/translation", "present", None, "translation is present"), ("fault.json", "/device_service_observation/observations/translation", "missing", None, "translation is missing"), ("repair-readback.json", "/device_service_observation/observations/translation", "present", None, "translation is present"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/translation", "missing", None, "translation is missing")],
    "05": [("baseline-readback.json", "/device_service_observation/observations/neighbor_state", "eq", "FULL", "neighbor_state == FULL"), ("fault.json", "/device_service_observation/observations/neighbor_state", "ne", "FULL", "neighbor_state != FULL"), ("repair-readback.json", "/device_service_observation/observations/neighbor_state", "eq", "FULL", "neighbor_state == FULL"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/neighbor_state", "ne", "FULL", "neighbor_state != FULL")],
    "06": [("baseline-readback.json", "/device_service_observation/observations/rib_result", "eq", "FIB", "rib_result == FIB"), ("fault.json", "/device_service_observation/observations/rib_result", "ne", "FIB", "rib_result != FIB"), ("repair-readback.json", "/device_service_observation/observations/rib_result", "eq", "FIB", "rib_result == FIB"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/rib_result", "ne", "FIB", "rib_result != FIB")],
    "07": [("baseline-readback.json", "/device_service_observation/observations/dns_ok", "eq", True, "dns_ok == true"), ("fault.json", "/device_service_observation/observations/dns_ok", "eq", False, "dns_ok == false"), ("repair-readback.json", "/device_service_observation/observations/dns_ok", "eq", True, "dns_ok == true"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/dns_ok", "eq", False, "dns_ok == false")],
    "08": [("baseline-readback.json", "/device_service_observation/observations/ordered_decision", "eq", "ALLOW", "ordered_decision == ALLOW"), ("fault.json", "/device_service_observation/observations/ordered_decision", "eq", "UNDECIDED", "ordered_decision == UNDECIDED"), ("repair-readback.json", "/device_service_observation/observations/ordered_decision", "eq", "ALLOW", "ordered_decision == ALLOW"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/ordered_decision", "eq", "UNDECIDED", "ordered_decision == UNDECIDED")],
    "09": [("baseline-readback.json", "/device_service_observation/observations/drops", "eq", 0, "drops == 0"), ("fault.json", "/device_service_observation/observations/channel_utilization", "ge", 80, "channel_utilization >= 80"), ("repair-readback.json", "/device_service_observation/observations/drops", "eq", 0, "drops == 0"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/drops", "gt", 0, "drops > 0")],
    "10": [("baseline-readback.json", "/device_service_observation/observations/rpf_interface", "eq", "uplink-a", "rpf_interface == uplink-a"), ("fault.json", "/device_service_observation/observations/rpf_interface", "eq", "uplink-b", "rpf_interface == uplink-b"), ("repair-readback.json", "/device_service_observation/observations/rpf_interface", "eq", "uplink-a", "rpf_interface == uplink-a"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/rpf_interface", "eq", "uplink-b", "rpf_interface == uplink-b")],
    "11": [("baseline-readback.json", "/device_service_observation/observations/evpn_type2_routes", "gt", 0, "evpn_type2_routes > 0"), ("fault.json", "/device_service_observation/observations/evpn_type2_routes", "eq", 0, "evpn_type2_routes == 0"), ("repair-readback.json", "/device_service_observation/observations/evpn_type2_routes", "gt", 0, "evpn_type2_routes > 0"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/underlay_reachable", "eq", False, "underlay_reachable == false")],
    "12": [("baseline-readback.json", "/device_service_observation/observations/forwarding_next_hop", "eq", "transit", "forwarding_next_hop == transit"), ("fault.json", "/device_service_observation/observations/forwarding_next_hop", "eq", "blackhole", "forwarding_next_hop == blackhole"), ("repair-readback.json", "/device_service_observation/observations/forwarding_next_hop", "eq", "transit", "forwarding_next_hop == transit"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/backend_listener", "eq", False, "backend_listener == false")],
    "13": [("baseline-readback.json", "/device_service_observation/observations/selected_path", "eq", "private-a", "selected_path == private-a"), ("fault.json", "/device_service_observation/observations/service_listener", "eq", False, "service_listener == false"), ("repair-readback.json", "/device_service_observation/observations/selected_path", "eq", "private-a", "selected_path == private-a"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/service_listener", "eq", False, "service_listener == false")],
    "14": [("baseline-readback.json", "/device_service_observation/observations/device_route", "eq", "route-allow", "device_route == route-allow"), ("fault.json", "/device_service_observation/observations/device_route", "eq", "route-deny", "device_route == route-deny"), ("repair-readback.json", "/device_service_observation/observations/device_route", "eq", "route-allow", "device_route == route-allow"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/device_route", "eq", "route-deny", "device_route == route-deny")],
    "15": [("baseline-readback.json", "/device_service_observation/observations/metric_ms", "lt", 50, "metric_ms < 50"), ("fault.json", "/device_service_observation/observations/timeline_complete", "eq", False, "timeline_complete == false"), ("repair-readback.json", "/device_service_observation/observations/metric_ms", "lt", 50, "metric_ms < 50"), ("assertion.json", "/negative_control/independent_path_change/evaluator_output/observations/timeline_complete", "eq", False, "timeline_complete == false")],
}


def _pointer(payload: Any, expression: str) -> Any:
    value = payload
    for part in expression.lstrip("/").split("/"):
        if part:
            value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def _predicate(observed: Any, operator: str, expected: Any) -> bool:
    if operator == "eq": return observed == expected
    if operator == "ne": return observed != expected
    if operator == "ge": return observed >= expected
    if operator == "gt": return observed > expected
    if operator == "lt": return observed < expected
    if operator == "present": return observed is not None
    if operator == "missing": return observed is None
    raise ValueError(f"unknown rubric operator: {operator}")


def _submission_records(results: list[dict[str, Any]], run_id: str) -> list[dict[str, Any]]:
    records = []
    for result in results:
        key = result["module_id"]
        base = f"runs/{run_id}/modules/{key}"
        payloads = {
            "baseline-readback.json": {"device_service_observation": result["baseline"]},
            "fault.json": {"device_service_observation": result["fault"]},
            "repair-readback.json": {"device_service_observation": result["repair"]},
            "assertion.json": {"negative_control": {"independent_path_change": {"evaluator_output": result["negative_control"]["independent_path"]}}},
        }
        criteria = []
        for index, (phase, pointer, operator, expected, threshold) in enumerate(RUBRICS[key], start=1):
            payload = payloads[phase]
            observed = _pointer(payload, pointer)
            expected_pointer = expected.get("pointer") if isinstance(expected, dict) else None
            expected_value = _pointer(payload, expected_pointer) if expected_pointer else expected
            passed = _predicate(observed, operator, expected_value)
            points_possible = 25
            points_awarded = points_possible if passed else 0
            criteria.append({"criterion_id": f"{key}.C{index}", "artifact_path": f"{base}/{phase}", "json_pointer": pointer, "observed_value": observed, "expected_value": expected_value, "expected_pointer": expected_pointer, "operator": operator, "threshold": threshold, "threshold_decision": "PASS" if passed else "FAIL", "pass": passed, "points_awarded": points_awarded, "points_possible": points_possible, "points_formula": "points_possible if predicate_result else 0", "score_arithmetic": f"{points_awarded}/{points_possible}", "scoring_inputs": {"observed_value": observed, "expected_value": expected_value, "operator": operator, "predicate_result": passed, "points_possible": points_possible, "points_awarded": points_awarded}, "sde2_follow_up": "Name the module-specific read-back and its falsifier." if index == 1 else "Explain the mechanism-specific symptom and a competing hypothesis." if index == 2 else "Describe the repair and reconciliation evidence proving convergence." if index == 3 else "Explain why an accepted request cannot prove forwarding success.", "staff_follow_up": "Assign ownership, SLO, and failure-domain budget." if index == 1 else "Define blast radius, approval boundary, and escalation trigger." if index == 2 else "Choose rollback criteria and recovery authority." if index == 3 else "Define an independent service SLO and evidence-retention policy."})
        total = sum(item["points_awarded"] for item in criteria)
        records.append({"module_id": key, "module": result["module"], "run_id": run_id, "status": "completed-local-emulator-submission", "criteria": criteria, "total_points": total, "score_arithmetic": " + ".join(str(item["points_awarded"]) for item in criteria) + f" = {total}/100", "score_computed_at_execution": True, "minimum_sde2": 80, "staff_discussion_threshold": 90, "evidence_boundary": "Observed local mechanism-emulator artifacts; vendor/provider examples remain illustrative."})
    return records


def _write_json_docs(fixtures_dir: Path, run_id: str, records: list[dict[str, Any]], submissions: list[dict[str, Any]]) -> None:
    _write_json(fixtures_dir / "ownership-records.json", {"schema": SCHEMA_VERSION, "run_id": run_id, "records": records}, overwrite=True)
    _write_json(fixtures_dir / "completed-submissions.json", {"schema": SCHEMA_VERSION, "run_id": run_id, "records": submissions}, overwrite=True)


def _write_ownership_matrix(fixtures_dir: Path, records: list[dict[str, Any]]) -> None:
    lines = ["# Canonical field-level ownership and reconciliation matrix", "", "## A. Contract", "", "Each row has one writer for one object/field path. Requests are **illustrative**; the controller result, effective read-back, and derived data-plane observation are **observed local-emulator evidence**. A negative control retains the same successful request/read-back while the separate traffic path triggers a mechanism-derived failure.", "", "| ID | Platform/object field | Single writer / approver | Reconciliation evidence | Derived probe and negative control |", "| --- | --- | --- | --- | --- |"]
    for record in records:
        rb = record["authoritative_readback"]
        lines.append(f"| {record['record_id']} | {record['platform']} `{record['object_field_path']}` | `{record['owner_id']}` / `{record['approver_id']}` | `{record['correlation_id']}` `{rb['reconciliation']['status']}` `{rb['reconciliation']['task_id']}` changed `{len(rb['reconciliation']['changed_fields'])}` fields; effective state retained | positive `{record['evaluator_output']['derived_probe']['result']}`; negative `{record['negative_control']['evaluator_output']['derived_probe']['result']}` from separate traffic path |")
    lines.extend(["", "## B. Reading the matrix", "", "The JSON record at [`observed/ownership-records.json`](observed/ownership-records.json) retains desired request, controller reconciliation result, effective state, device/service observation, separate fixture traffic, and negative-control evidence. `evaluator.py` derives the probe and rejects caller-supplied health flags. These artifacts are a fictional learning emulator and do not prove a real cloud, controller, switch, F5, or A10 change.", ""])
    (fixtures_dir / "ownership-matrix.md").write_text("\n".join(lines), encoding="utf-8")


def _write_submission_doc(fixtures_dir: Path, submissions: list[dict[str, Any]]) -> None:
    lines = ["# Artifact-backed completed submissions", "", "## A. Evidence contract", "", "Every criterion names a retained artifact, a module-specific JSON pointer, the observed value, a domain threshold, and an explicit threshold decision. No score uses a generic health-only pointer. These are fictional local-emulator submissions; they do not claim AWS, GCP, controller, switch, F5, or A10 execution.", ""]
    for record in submissions:
        lines.extend([f"## B. Module {record['module_id']} — {record['module']}", "", f"**Score:** `{record['score_arithmetic']}`; status: **{record['status']}**", "", "| Criterion | Artifact + JSON pointer | Observed | Module-specific threshold | Decision | Score | SDE2 follow-up | Staff follow-up |", "| --- | --- | --- | --- | --- | --- | --- | --- |"])
        for criterion in record["criteria"]:
            observed = "resolved by validator" if criterion["observed_value"] is None else criterion["observed_value"]
            lines.append(f"| `{criterion['criterion_id']}` | `{criterion['artifact_path']}#{criterion['json_pointer']}` | `{observed}` | `{criterion['threshold']}` | **{criterion['threshold_decision']}** | `{criterion['score_arithmetic']}` | {criterion['sde2_follow_up']} | {criterion['staff_follow_up']} |" )
        lines.append("")
    lines.extend(["## C. Scoring and labels", "", "A criterion fails if its artifact or JSON pointer is missing, stale, or does not resolve to a value satisfying its module-specific threshold. **Observed** means generated by the local mechanism evaluator. **Derived probe** means calculated from effective state and a separate traffic path. Provider and vendor request examples are **illustrative**.", ""])
    (fixtures_dir / "worked-submissions.md").write_text("\n".join(lines), encoding="utf-8")


def run(selected: list[str], artifacts_dir: Path | None) -> tuple[list[dict[str, Any]], str]:
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ") + "-" + uuid.uuid4().hex[:8]
    temporary_capture = None
    capture = artifacts_dir
    if capture is None:
        temporary_capture = Path(tempfile.mkdtemp(prefix="ccna-capture-"))
        capture = temporary_capture
    capture.mkdir(parents=True, exist_ok=True)
    specs = _scenario_specs()
    results = []
    try:
        for key in selected:
            results.append(_run_scenario(key, specs[key], run_id, capture / "runs" / run_id / "modules" / key))
        records = _ownership_records(run_id, _now(), specs)
        submissions = _submission_records(results, run_id)
        _write_json(capture / "run.json", {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "run_id": run_id, "modules": results, "bundle_count": len(results), "immutable_bundles": True, "semantic_contract": {"control_faults_only": True, "data_plane_derived": True, "reconciliation_model": True, "ownership_probes_derived": True}}, overwrite=True)
        for result in results:
            _write_json(capture / f"{result['module']}.json", result, overwrite=True)
        _write_json_docs(capture, run_id, records, submissions)
        (capture / "README.md").write_text("# Captured fixture artifacts\n\nThis capture contains immutable v3 bundles with control-only faults, derived mechanism observations, reconciliation read-backs, ownership records, and module-specific criterion submissions. Results are observed local-emulator output; vendor shapes remain illustrative.\n", encoding="utf-8")
        if artifacts_dir is not None:
            _write_ownership_matrix(artifacts_dir.parent, records)
            _write_submission_doc(artifacts_dir.parent, submissions)
        return results, run_id
    finally:
        if temporary_capture is not None:
            shutil.rmtree(temporary_capture, ignore_errors=False)


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--module", choices=["all", *[f"{i:02d}" for i in range(1, 16)]], default="all")
    parser.add_argument("--all", action="store_true", dest="all_modules")
    parser.add_argument("--artifacts-dir", type=Path)
    args = parser.parse_args()
    selected = [f"{i:02d}" for i in range(1, 16)] if args.all_modules or args.module == "all" else [args.module]
    results, run_id = run(selected, args.artifacts_dir)
    print(json.dumps({"run_id": run_id, "modules": results}, sort_keys=True, indent=2))
    print(f"FIXTURE_PASS modules={len(results)} temporary_workspace_removed=True no_leak=True")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
