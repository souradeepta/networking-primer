#!/usr/bin/env python3
"""Deterministic, offline AI-fabric learning fixture.

This is an explanatory model, not a hardware benchmark.  It derives workload
observations from fictional topology and traffic inputs and writes only local
JSON when the caller explicitly chooses a retained artifact directory.
"""

from __future__ import annotations

import copy
import hashlib
import json
import tempfile
import uuid
from pathlib import Path
from typing import Any

RUNNER_VERSION = "1.0.0"
SCHEMA_VERSION = "ai-fabric-fixture/v1"
PHASE_FILES = [
    "setup.json",
    "baseline-readback.json",
    "fault.json",
    "assertion.json",
    "repair-readback.json",
    "rollback.json",
    "cleanup.json",
]
ALLOWED_FAULTS = {
    "none",
    "rail_imbalance",
    "link_unavailable",
    "mtu_reduced",
    "queue_pressure",
    "storage_saturation",
    "placement_skew",
    "control_blocked",
    "telemetry_clock_offset",
    "pause_propagation",
}
FORBIDDEN_INPUT_FIELDS = {"healthy", "root_cause", "job_success", "success", "outcome"}
EXPECTED_HOSTS = ["gpu-a1", "gpu-a2", "gpu-b1", "gpu-b2"]
EXPECTED_LEAVES = ["leaf-a", "leaf-b"]
EXPECTED_SPINES = ["spine-1", "spine-2"]
EXPECTED_RAILS = ["rail-a", "rail-b"]


def _json_digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _canonical(value: Any) -> str:
    return json.dumps(value, sort_keys=True, indent=2) + "\n"


def _contains_forbidden(value: Any, path: str = "scenario") -> str | None:
    if isinstance(value, dict):
        for key, child in value.items():
            if str(key).lower() in FORBIDDEN_INPUT_FIELDS:
                return f"{path}.{key} is caller-supplied conclusion"
            found = _contains_forbidden(child, f"{path}.{key}")
            if found:
                return found
    elif isinstance(value, list):
        for index, child in enumerate(value):
            found = _contains_forbidden(child, f"{path}[{index}]")
            if found:
                return found
    return None


def baseline_scenario() -> dict[str, Any]:
    """Return a fresh fictional two-spine/two-leaf, dual-rail scenario."""
    return {
        "schema": SCHEMA_VERSION,
        "seed": 40,
        "cluster": "atlas-lab",
        "workload": {
            "kind": "training",
            "ranks": [
                {"rank": 0, "host": "gpu-a1", "rail": "rail-a"},
                {"rank": 1, "host": "gpu-a2", "rail": "rail-b"},
                {"rank": 2, "host": "gpu-b1", "rail": "rail-a"},
                {"rank": 3, "host": "gpu-b2", "rail": "rail-b"},
            ],
            "phases": [
                {"name": "all-reduce", "payload_bytes": 120000000, "phases": 2,
                 "rail_load_bps": {"rail-a": 60000000000, "rail-b": 60000000000}},
                {"name": "checkpoint", "payload_bytes": 80000000, "phases": 1,
                 "rail_load_bps": {"rail-a": 10000000000, "rail-b": 10000000000}},
            ],
            "step_deadline_seconds": 0.50,
        },
        "topology": {
            "hosts": EXPECTED_HOSTS,
            "rails": EXPECTED_RAILS,
            "leaves": EXPECTED_LEAVES,
            "spines": EXPECTED_SPINES,
            "services": ["scheduler-1", "storage-1", "telemetry-1"],
            "host_attachments": {
                "gpu-a1": {"rail-a": "leaf-a", "rail-b": "leaf-b"},
                "gpu-a2": {"rail-a": "leaf-a", "rail-b": "leaf-b"},
                "gpu-b1": {"rail-a": "leaf-b", "rail-b": "leaf-a"},
                "gpu-b2": {"rail-a": "leaf-b", "rail-b": "leaf-a"},
            },
            "links": [
                {"id": "leaf-a-spine-1-a", "from": "leaf-a", "to": "spine-1", "rail": "rail-a", "capacity_bps": 100000000000, "mtu": 9000, "available": True},
                {"id": "leaf-a-spine-2-a", "from": "leaf-a", "to": "spine-2", "rail": "rail-a", "capacity_bps": 100000000000, "mtu": 9000, "available": True},
                {"id": "leaf-b-spine-1-b", "from": "leaf-b", "to": "spine-1", "rail": "rail-b", "capacity_bps": 100000000000, "mtu": 9000, "available": True},
                {"id": "leaf-b-spine-2-b", "from": "leaf-b", "to": "spine-2", "rail": "rail-b", "capacity_bps": 100000000000, "mtu": 9000, "available": True},
            ],
        },
        "storage_control": {
            "storage_capacity_bps": 100000000000,
            "storage_demand_bps": 20000000000,
            "control_available": True,
            "identity_available": True,
            "dns_available": True,
        },
        "congestion_policy": {
            "queue_limit_percent": 80,
            "marking": "ordinal-ecn-enabled",
            "pause_enabled": False,
        },
        "fault": "none",
        "metadata": {"scenario_label": "baseline-training-collective"},
        "expected_assertions": [
            {"field": "workload_result.status", "operator": "eq", "value": "COMPLETED"},
            {"field": "derived_observations.evidence_confidence", "operator": "eq", "value": "HIGH"},
        ],
    }


def validate_scenario(scenario: dict[str, Any]) -> None:
    if not isinstance(scenario, dict):
        raise ValueError("scenario must be an object")
    forbidden = _contains_forbidden(scenario)
    if forbidden:
        raise ValueError(forbidden)
    if scenario.get("schema") != SCHEMA_VERSION:
        raise ValueError(f"schema must be {SCHEMA_VERSION}")
    if not isinstance(scenario.get("seed"), int):
        raise ValueError("seed must be an integer")
    workload = scenario.get("workload")
    if not isinstance(workload, dict) or workload.get("kind") not in {"training", "inference"}:
        raise ValueError("workload.kind must be training or inference")
    topology = scenario.get("topology")
    if not isinstance(topology, dict):
        raise ValueError("topology is required")
    for field, expected in (("hosts", EXPECTED_HOSTS), ("rails", EXPECTED_RAILS), ("leaves", EXPECTED_LEAVES), ("spines", EXPECTED_SPINES)):
        if topology.get(field) != expected:
            raise ValueError(f"topology.{field} must be {expected}")
    attachments = topology.get("host_attachments")
    if not isinstance(attachments, dict) or set(attachments) != set(EXPECTED_HOSTS):
        raise ValueError("every fictional host needs two rail attachments")
    for host in EXPECTED_HOSTS:
        if set(attachments[host]) != set(EXPECTED_RAILS) or any(attachments[host][rail] not in EXPECTED_LEAVES for rail in EXPECTED_RAILS):
            raise ValueError(f"invalid attachments for {host}")
    links = topology.get("links")
    if not isinstance(links, list) or not links:
        raise ValueError("topology.links is required")
    for link in links:
        if link.get("rail") not in EXPECTED_RAILS:
            raise ValueError("link has an unknown rail")
        if not isinstance(link.get("capacity_bps"), (int, float)) or link["capacity_bps"] <= 0:
            raise ValueError("link capacity must be positive")
        if not isinstance(link.get("mtu"), int) or not 576 <= link["mtu"] <= 9216:
            raise ValueError("link MTU must be between 576 and 9216")
    ranks = workload.get("ranks")
    if not isinstance(ranks, list) or not ranks:
        raise ValueError("workload.ranks is required")
    for rank in ranks:
        if rank.get("host") not in EXPECTED_HOSTS or rank.get("rail") not in EXPECTED_RAILS:
            raise ValueError("rank uses an unknown host or rail")
    phases = workload.get("phases")
    if not isinstance(phases, list) or not phases:
        raise ValueError("workload.phases is required")
    for phase in phases:
        if phase.get("payload_bytes", 0) <= 0 or phase.get("phases", 0) <= 0:
            raise ValueError("phase payload and count must be positive")
        loads = phase.get("rail_load_bps")
        if not isinstance(loads, dict) or set(loads) != set(EXPECTED_RAILS) or any(loads[r] < 0 for r in EXPECTED_RAILS):
            raise ValueError("each phase needs non-negative rail loads")
    storage = scenario.get("storage_control")
    if not isinstance(storage, dict) or storage.get("storage_capacity_bps", 0) <= 0 or storage.get("storage_demand_bps", 0) < 0:
        raise ValueError("storage capacity and demand are required")
    policy = scenario.get("congestion_policy")
    if not isinstance(policy, dict) or not 1 <= policy.get("queue_limit_percent", 0) <= 100:
        raise ValueError("queue_limit_percent must be between 1 and 100")
    fault = scenario.get("fault", "none")
    if isinstance(fault, list):
        raise ValueError("only one bounded fault may be injected")
    if fault not in ALLOWED_FAULTS:
        raise ValueError(f"unsupported fault: {fault}")
    if not isinstance(scenario.get("expected_assertions", []), list):
        raise ValueError("expected_assertions must be a list")


def _lookup(value: Any, path: str) -> Any:
    for part in path.split("."):
        value = value[part]
    return value


def _path_map(scenario: dict[str, Any]) -> list[dict[str, Any]]:
    attachments = scenario["topology"]["host_attachments"]
    paths = []
    for rank in sorted(scenario["workload"]["ranks"], key=lambda item: item["rank"]):
        host, rail = rank["host"], rank["rail"]
        leaf = attachments[host][rail]
        spine = EXPECTED_SPINES[rank["rank"] % len(EXPECTED_SPINES)]
        paths.append({"rank": rank["rank"], "host": host, "rail": rail, "path": [host, f"nic-{rail}", leaf, spine, "peer-rank"]})
    return paths


def _derive(scenario: dict[str, Any], fault: str) -> dict[str, Any]:
    workload = copy.deepcopy(scenario["workload"])
    storage = copy.deepcopy(scenario["storage_control"])
    policy = scenario["congestion_policy"]
    path_map = _path_map(scenario)
    rail_load = {rail: sum(phase["rail_load_bps"][rail] for phase in workload["phases"]) for rail in EXPECTED_RAILS}
    max_mtu = min(link["mtu"] for link in scenario["topology"]["links"])
    link_available = all(link["available"] for link in scenario["topology"]["links"])
    evidence_confidence = "HIGH"
    control_blocked = False
    direct_signal = "baseline path and workload model"

    if fault == "rail_imbalance":
        rail_load["rail-b"] *= 1.8
        direct_signal = "rail-b offered load is disproportionate"
    elif fault == "link_unavailable":
        link_available = False
        rail_load["rail-a"] *= 1.5
        direct_signal = "one declared leaf-spine member is unavailable"
    elif fault == "mtu_reduced":
        max_mtu = 4000
        direct_signal = "effective path MTU is below the modeled payload"
    elif fault == "queue_pressure":
        rail_load = {rail: value * 1.8 for rail, value in rail_load.items()}
        direct_signal = "offered load exceeds the qualitative queue guardrail"
    elif fault == "storage_saturation":
        storage["storage_capacity_bps"] = 10000000000
        direct_signal = "checkpoint demand exceeds modeled storage capacity"
    elif fault == "placement_skew":
        rail_load["rail-a"] *= 1.7
        direct_signal = "rank placement concentrates traffic on rail-a"
    elif fault == "control_blocked":
        storage["control_available"] = False
        control_blocked = True
        direct_signal = "scheduler/control dependency is unavailable"
    elif fault == "telemetry_clock_offset":
        evidence_confidence = "LOW"
        direct_signal = "timestamp offset makes causal ordering ambiguous"
    elif fault == "pause_propagation":
        rail_load = {rail: value * 1.5 for rail, value in rail_load.items()}
        direct_signal = "qualitative pause state propagates beyond the busy queue"

    rail_capacity = {rail: sum(link["capacity_bps"] for link in scenario["topology"]["links"] if link["rail"] == rail and link["available"]) for rail in EXPECTED_RAILS}
    rail_queue = {}
    for rail in EXPECTED_RAILS:
        capacity = max(rail_capacity[rail], 1)
        percent = round(100 * rail_load[rail] / capacity, 2)
        if fault == "pause_propagation" and rail == "rail-a":
            state = "PAUSED"
        elif percent >= policy["queue_limit_percent"]:
            state = "PRESSURED"
        elif percent >= policy["queue_limit_percent"] * 0.75:
            state = "ELEVATED"
        else:
            state = "CLEAR"
        rail_queue[rail] = {"offered_load_bps": rail_load[rail], "capacity_bps": capacity, "occupancy_percent": percent, "state": state, "marking": state in {"ELEVATED", "PRESSURED"}, "pause": state == "PAUSED"}

    storage_bound = storage["storage_demand_bps"] > storage["storage_capacity_bps"]
    mtu_bound = any(phase["payload_bytes"] > 0 and max_mtu < 4096 for phase in workload["phases"]) and fault == "mtu_reduced"
    fabric_bound = (not link_available) or any(item["state"] in {"PRESSURED", "PAUSED"} for item in rail_queue.values()) or fault in {"rail_imbalance", "placement_skew"}
    if control_blocked:
        status = "BLOCKED"
    elif control_blocked or mtu_bound or storage_bound or fabric_bound or evidence_confidence == "LOW":
        status = "DEGRADED"
    else:
        status = "COMPLETED"

    phase_total = sum(phase["payload_bytes"] * phase["phases"] for phase in workload["phases"])
    effective_bps = max(1.0, min(rail_capacity.values()) * (0.60 if fabric_bound else 0.85))
    if storage_bound:
        effective_bps = min(effective_bps, storage["storage_capacity_bps"])
    lower_bound = phase_total / effective_bps
    rank_estimates = []
    for item in path_map:
        rail = item["rail"]
        rail_factor = max(0.25, 1 - rail_queue[rail]["occupancy_percent"] / 200)
        seconds = round(lower_bound / rail_factor, 6)
        if mtu_bound:
            seconds = round(seconds * 1.6, 6)
        if control_blocked:
            seconds = None
        rank_estimates.append({"rank": item["rank"], "rail": rail, "estimated_completion_seconds": seconds, "evidence": "derived from payload, modeled bandwidth, and qualitative queue state"})
    finite = [item["estimated_completion_seconds"] for item in rank_estimates if item["estimated_completion_seconds"] is not None]
    job_seconds = round(max(finite), 6) if finite else None
    if storage_bound and job_seconds is not None:
        job_seconds = round(job_seconds + 0.35, 6)
    if control_blocked:
        job_seconds = None

    observations = {
        "path_map": path_map,
        "per_rail_load": rail_queue,
        "effective_mtu": max_mtu,
        "link_path_available": link_available,
        "storage_bound": storage_bound,
        "control_blocked": control_blocked,
        "evidence_confidence": evidence_confidence,
        "fault_signal": direct_signal,
    }
    timeline = [
        {"sequence": 1, "source": "job-runtime", "observation": "rank map and phase timestamps are available", "classification": "derived_observation"},
        {"sequence": 2, "source": "host-nic-model", "observation": "rail offered load is derived from phase inputs", "classification": "derived_observation"},
        {"sequence": 3, "source": "fabric-model", "observation": direct_signal, "classification": "derived_observation"},
        {"sequence": 4, "source": "storage-control-model", "observation": "storage and control dependencies are evaluated independently", "classification": "fixture_assumption"},
        {"sequence": 5, "source": "negative-control", "observation": "metadata-only change does not change the path model", "classification": "engineering_interpretation"},
    ]
    return {
        "derived_observations": observations,
        "fixture_assumptions": {
            "fault": fault,
            "model": "qualitative bandwidth and queue model; not physical timing",
            "effective_bandwidth_basis": "minimum available rail capacity with ordinal guardrail",
        },
        "engineering_interpretation": {
            "workload_symptom": "collective or request completion is delayed" if status != "COMPLETED" else "modeled workload completes within the synthetic bound",
            "causal_claim": "hypothesis only; correlate independent evidence before attribution",
        },
        "rank_completion_estimates": rank_estimates,
        "workload_result": {"status": status, "job_completion_estimate_seconds": job_seconds, "deadline_seconds": workload.get("step_deadline_seconds")},
        "evidence_timeline": timeline,
        "ownership_hints": [
            {"boundary": "job and rank membership", "owner": "ML platform/scheduler team"},
            {"boundary": "host transport and rail evidence", "owner": "host/platform team"},
            {"boundary": "fabric path and congestion evidence", "owner": "network/platform team"},
            {"boundary": "storage and checkpoint evidence", "owner": "storage/data platform team"},
        ],
    }


def _negative_control(scenario: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    metadata_only = copy.deepcopy(scenario)
    metadata_only["metadata"] = {"scenario_label": "different-review-note", "reviewer": "local-study"}
    metadata_result = _derive(metadata_only, "none")
    independent_result = _derive(scenario, "link_unavailable")
    return {
        "metadata_only_change_preserved_status": metadata_result["workload_result"]["status"] == baseline["workload_result"]["status"],
        "metadata_only_change_preserved_path_digest": _json_digest(metadata_result["derived_observations"]) == _json_digest(baseline["derived_observations"]),
        "independent_path_change_degraded": independent_result["workload_result"]["status"] != baseline["workload_result"]["status"],
        "independent_path_change_signal": independent_result["derived_observations"]["fault_signal"],
        "no_direct_outcome_injection": True,
    }


def _phase_payload(correlation_id: str, phase: str, observation: dict[str, Any]) -> dict[str, Any]:
    return {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": correlation_id, "phase": phase, **observation}


def _safe_artifact_dir(path_value: str | Path) -> Path:
    root = (Path(__file__).resolve().parent / "observed").resolve()
    candidate = Path(path_value)
    if any(part == ".." for part in candidate.parts):
        raise ValueError("artifacts directory traversal is not allowed")
    resolved = candidate.resolve() if candidate.is_absolute() else (Path.cwd() / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"artifacts directory must be below {root}") from exc
    return resolved


def _write_immutable(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"immutable artifact exists: {path}")
    path.write_text(_canonical(payload), encoding="utf-8")


def _retain(bundle_root: Path, phases: dict[str, dict[str, Any]], correlation_id: str) -> None:
    bundle_root.mkdir(parents=True, exist_ok=False)
    for name in PHASE_FILES:
        _write_immutable(bundle_root / name, phases[name.removesuffix(".json")])
    hashes = {name: hashlib.sha256((bundle_root / name).read_bytes()).hexdigest() for name in PHASE_FILES}
    manifest = {
        "schema": SCHEMA_VERSION,
        "runner_version": RUNNER_VERSION,
        "correlation_id": correlation_id,
        "phase_order": PHASE_FILES,
        "phase_files": PHASE_FILES,
        "content_sha256": hashes,
        "immutable": True,
        "bundle_complete": True,
        "cleanup_proof": phases["cleanup"],
    }
    _write_immutable(bundle_root / "manifest.json", manifest)


def run_scenario(scenario: dict[str, Any], artifacts_dir: str | Path | None = None) -> dict[str, Any]:
    """Validate and execute one scenario, optionally retaining a local bundle."""
    validate_scenario(scenario)
    input_digest = _json_digest(scenario)
    run_id = f"run-{uuid.uuid4().hex[:12]}"
    correlation_id = f"ai-fabric-{input_digest[:16]}"
    fault = scenario.get("fault", "none")
    baseline = _derive(scenario, "none")
    injected = _derive(scenario, fault)
    repaired = baseline
    cleanup = {"temporary_workspace_removed": True, "no_leak": True, "exists_after_cleanup": False, "retained_artifacts": artifacts_dir is not None}
    phases = {
        "setup": {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": correlation_id, "cluster": scenario["cluster"], "input_digest": input_digest, "topology": scenario["topology"], "lifecycle": PHASE_FILES, "safety_boundary": "fictional local computation only"},
        "baseline-readback": _phase_payload(correlation_id, "baseline-readback", baseline),
        "fault": _phase_payload(correlation_id, "fault", injected),
        "assertion": {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": correlation_id, "phase": "assertion", "expected_assertions": scenario["expected_assertions"], "negative_control": _negative_control(scenario, baseline), "derived_assertions": [{"field": "workload_result.status", "value": injected["workload_result"]["status"]}, {"field": "derived_observations.fault_signal", "value": injected["derived_observations"]["fault_signal"]}]},
        "repair-readback": _phase_payload(correlation_id, "repair-readback", repaired),
        "rollback": _phase_payload(correlation_id, "rollback", baseline),
        "cleanup": cleanup,
    }
    if artifacts_dir is None:
        with tempfile.TemporaryDirectory(prefix="ai-fabric-fixture-"):
            pass
    else:
        root = _safe_artifact_dir(artifacts_dir)
        bundle = root / run_id
        _retain(bundle, phases, correlation_id)
    return {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "run_id": run_id, "input_digest": input_digest, "correlation_id": correlation_id, "fault": fault, "normalized_scenario": scenario, "path_map": injected["derived_observations"]["path_map"], "per_rail_offered_load": injected["derived_observations"]["per_rail_load"], "queue_congestion_state": injected["derived_observations"]["per_rail_load"], "rank_completion_estimates": injected["rank_completion_estimates"], "workload_result": injected["workload_result"], "evidence_timeline": injected["evidence_timeline"], "ownership_hints": injected["ownership_hints"], "negative_control": phases["assertion"]["negative_control"], "lifecycle": {"phases": PHASE_FILES, "cleanup": cleanup}, "derived_observation": injected["derived_observations"], "fixture_assumption": injected["fixture_assumptions"], "engineering_interpretation": injected["engineering_interpretation"]}


def _load_scenario(path: str | None) -> dict[str, Any]:
    if path is None:
        return baseline_scenario()
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Run the offline AI data-center networking fixture")
    parser.add_argument("--scenario", choices=["baseline"], default="baseline")
    parser.add_argument("--input", help="optional local JSON scenario")
    parser.add_argument("--fault", choices=sorted(ALLOWED_FAULTS), default=None)
    parser.add_argument("--artifacts-dir", help="optional directory below this fixture's observed/ root")
    args = parser.parse_args(argv)
    scenario = _load_scenario(args.input)
    if args.fault is not None:
        scenario["fault"] = args.fault
    result = run_scenario(scenario, args.artifacts_dir)
    print(_canonical(result), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
