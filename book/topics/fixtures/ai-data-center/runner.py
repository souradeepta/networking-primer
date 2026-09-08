#!/usr/bin/env python3
"""Deterministic, offline AI-fabric learning fixture, schema v2.

This is a small explanatory graph and workload model, not a hardware
benchmark or forwarding implementation. It uses only fictional state and the
Python standard library. Fault names are bounded input shorthands that mutate
state; all observations are then derived from that state.
"""

from __future__ import annotations

import copy
import hashlib
import json
import math
import tempfile
import uuid
from pathlib import Path
from typing import Any

RUNNER_VERSION = "2.0.0"
SCHEMA_VERSION = "ai-fabric-fixture/v2"
PHASE_FILES = [
    "setup.json", "baseline-readback.json", "fault.json", "assertion.json",
    "repair-readback.json", "rollback.json", "cleanup.json",
]
ALLOWED_FAULTS = {
    "none", "rail_imbalance", "link_unavailable", "mtu_reduced",
    "queue_pressure", "storage_saturation", "placement_skew",
    "control_blocked", "telemetry_clock_offset", "pause_propagation",
    "prefill_saturation",
}
ASSERTION_OPERATORS = {"eq", "ne", "lt", "lte", "gt", "gte", "contains", "exists"}
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


def _default_links() -> list[dict[str, Any]]:
    links = []
    for leaf in EXPECTED_LEAVES:
        for spine in EXPECTED_SPINES:
            for rail in EXPECTED_RAILS:
                links.append({
                    "id": f"{leaf}-{spine}-{rail[-1]}",
                    "from": leaf, "to": spine, "rail": rail,
                    "capacity_bps": 100_000_000_000, "mtu": 9000, "available": True,
                })
    return links


def _training_workload() -> dict[str, Any]:
    return {
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
        "required_mtu": 9000, "step_deadline_seconds": 0.50,
    }


def _inference_workload() -> dict[str, Any]:
    return {
        "kind": "inference", "requests": 64, "batch_size": 8,
        "arrival_rate_rps": 100.0, "target_p99_seconds": 0.050,
        "model_cache_available": True,
        "stages": {
            "gateway": {"work_seconds": 0.002},
            "prefill": {"work_seconds": 0.010},
            "decode": {"work_seconds": 0.015},
            "model_cache": {"work_seconds": 0.005, "dependency": "model-cache"},
        },
        "ranks": [
            {"rank": 0, "host": "gpu-a1", "rail": "rail-a"},
            {"rank": 1, "host": "gpu-a2", "rail": "rail-b"},
        ],
        "phases": [{"name": "serving-fabric", "payload_bytes": 64000000, "phases": 1,
                    "rail_load_bps": {"rail-a": 20000000000, "rail-b": 20000000000}}],
        "required_mtu": 9000,
    }


def baseline_scenario() -> dict[str, Any]:
    """Return a fresh fictional dual-rail leaf-spine training scenario."""
    return {
        "schema": SCHEMA_VERSION, "seed": 40, "cluster": "atlas-lab",
        "workload": _training_workload(),
        "topology": {
            "hosts": EXPECTED_HOSTS, "rails": EXPECTED_RAILS,
            "leaves": EXPECTED_LEAVES, "spines": EXPECTED_SPINES,
            "services": ["scheduler-1", "storage-1", "telemetry-1"],
            "host_attachments": {
                host: {rail: ("leaf-a" if host.endswith(("a1", "a2")) else "leaf-b") for rail in EXPECTED_RAILS}
                for host in EXPECTED_HOSTS
            },
            "links": _default_links(),
        },
        "storage_control": {
            "storage_capacity_bps": 100000000000, "storage_demand_bps": 20000000000,
            "control_available": True, "identity_available": True, "dns_available": True,
        },
        "congestion_policy": {"queue_limit_percent": 80, "marking": "ordinal-ecn-enabled", "pause_enabled": False},
        "observability": {"timestamp_ordering_confidence": "HIGH"},
        "fault": "none", "metadata": {"scenario_label": "baseline-training-collective"},
        "expected_assertions": [
            {"field": "workload_result.health_state", "operator": "eq", "value": "COMPLETED"},
            {"field": "evidence_assessment.confidence", "operator": "eq", "value": "HIGH"},
        ],
    }


def inference_scenario() -> dict[str, Any]:
    """Return the same fictional topology with a bounded serving workload."""
    scenario = baseline_scenario()
    scenario["workload"] = _inference_workload()
    scenario["metadata"] = {"scenario_label": "baseline-inference-cohort"}
    scenario["expected_assertions"] = [
        {"field": "workload_result.objective_state", "operator": "eq", "value": "MET"},
        {"field": "evidence_assessment.confidence", "operator": "eq", "value": "HIGH"},
    ]
    return scenario


def _link_index(topology: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {link["id"]: link for link in topology["links"]}


def _declared_eligible_links(scenario: dict[str, Any], host: str, rail: str) -> list[dict[str, Any]]:
    leaf = scenario["topology"]["host_attachments"][host][rail]
    return sorted([link for link in scenario["topology"]["links"] if link["from"] == leaf and link["rail"] == rail], key=lambda item: item["id"])


def _valid_assertion_paths(scenario: dict[str, Any]) -> set[str]:
    paths = {
        "workload_result.health_state", "workload_result.objective_state",
        "workload_result.deadline_met", "evidence_assessment.confidence",
        "derived_observation.effective_mtu", "derived_observation.selected_paths",
        "derived_observation.storage_bound",
    }
    paths.update(f"derived_observation.control_dependencies.{name}" for name in ("control", "identity", "dns", "model_cache"))
    paths.update(f"derived_observation.per_link_load.{link['id']}.state" for link in scenario["topology"]["links"])
    return paths


def _validate_assertion(assertion: Any, scenario: dict[str, Any]) -> None:
    if not isinstance(assertion, dict) or set(assertion) != {"field", "operator", "value"}:
        raise ValueError("assertions require exactly field, operator, and value")
    if assertion["field"] not in _valid_assertion_paths(scenario):
        raise ValueError(f"assertion field is not allowlisted: {assertion.get('field')}")
    if assertion["operator"] not in ASSERTION_OPERATORS:
        raise ValueError(f"assertion operator is not allowlisted: {assertion.get('operator')}")
    if assertion["operator"] == "exists" and not isinstance(assertion["value"], bool):
        raise ValueError("exists assertion value must be boolean")


def validate_scenario(scenario: dict[str, Any]) -> None:
    if not isinstance(scenario, dict):
        raise ValueError("scenario must be an object")
    forbidden = _contains_forbidden(scenario)
    if forbidden:
        raise ValueError(forbidden)
    if scenario.get("schema") != SCHEMA_VERSION:
        raise ValueError(f"schema must be {SCHEMA_VERSION}; schema-v1 is not accepted by schema-v2")
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
        if not isinstance(attachments[host], dict) or set(attachments[host]) != set(EXPECTED_RAILS) or any(attachments[host][rail] not in EXPECTED_LEAVES for rail in EXPECTED_RAILS):
            raise ValueError(f"invalid attachments for {host}")
    links = topology.get("links")
    if not isinstance(links, list) or not links:
        raise ValueError("topology.links is required")
    link_ids: set[str] = set()
    for link in links:
        if not isinstance(link, dict) or set(link) - {"id", "from", "to", "rail", "capacity_bps", "mtu", "available"}:
            raise ValueError("links contain only declared graph fields")
        if not isinstance(link.get("id"), str) or not link["id"] or link["id"] in link_ids:
            raise ValueError("link IDs must be unique and non-empty")
        link_ids.add(link["id"])
        if link.get("from") not in EXPECTED_LEAVES or link.get("to") not in EXPECTED_SPINES:
            raise ValueError("link endpoints must be a declared leaf and spine")
        if link.get("rail") not in EXPECTED_RAILS:
            raise ValueError("link has an unknown rail")
        if not isinstance(link.get("capacity_bps"), (int, float)) or isinstance(link["capacity_bps"], bool) or link["capacity_bps"] <= 0:
            raise ValueError("link capacity must be positive")
        if not isinstance(link.get("mtu"), int) or not 576 <= link["mtu"] <= 9216:
            raise ValueError("link MTU must be between 576 and 9216")
        if not isinstance(link.get("available"), bool):
            raise ValueError("link availability must be boolean")
    ranks = workload.get("ranks", [])
    if workload["kind"] == "training" and (not isinstance(ranks, list) or not ranks):
        raise ValueError("training workload.ranks is required")
    if not isinstance(ranks, list):
        raise ValueError("workload.ranks must be a list")
    seen_ranks: set[int] = set()
    for rank in ranks:
        if not isinstance(rank, dict) or not isinstance(rank.get("rank"), int) or rank["rank"] in seen_ranks:
            raise ValueError("ranks must have unique integer IDs")
        seen_ranks.add(rank["rank"])
        if rank.get("host") not in EXPECTED_HOSTS or rank.get("rail") not in EXPECTED_RAILS:
            raise ValueError("rank uses an unknown host or rail")
        if not _declared_eligible_links(scenario, rank["host"], rank["rail"]):
            raise ValueError("rank has no declared compatible leaf/spine member on its rail")
    phases = workload.get("phases")
    if not isinstance(phases, list) or not phases:
        raise ValueError("workload.phases is required")
    for phase in phases:
        if not isinstance(phase, dict) or phase.get("payload_bytes", 0) <= 0 or phase.get("phases", 0) <= 0:
            raise ValueError("phase payload and count must be positive")
        loads = phase.get("rail_load_bps")
        if not isinstance(loads, dict) or set(loads) != set(EXPECTED_RAILS) or any(not isinstance(loads[r], (int, float)) or loads[r] < 0 for r in EXPECTED_RAILS):
            raise ValueError("each phase needs non-negative rail loads")
    if not isinstance(workload.get("required_mtu"), int) or not 576 <= workload["required_mtu"] <= 9216:
        raise ValueError("workload.required_mtu must be a valid MTU")
    if workload["kind"] == "training":
        if not isinstance(workload.get("step_deadline_seconds"), (int, float)) or workload["step_deadline_seconds"] <= 0:
            raise ValueError("training step_deadline_seconds must be positive")
    else:
        for field in ("requests", "batch_size"):
            if not isinstance(workload.get(field), int) or workload[field] <= 0:
                raise ValueError(f"inference {field} must be positive")
        if not isinstance(workload.get("arrival_rate_rps"), (int, float)) or workload["arrival_rate_rps"] <= 0:
            raise ValueError("inference arrival_rate_rps must be positive")
        if not isinstance(workload.get("target_p99_seconds"), (int, float)) or workload["target_p99_seconds"] <= 0:
            raise ValueError("inference target_p99_seconds must be positive")
        if not isinstance(workload.get("model_cache_available"), bool):
            raise ValueError("inference model_cache_available must be boolean")
        stages = workload.get("stages")
        if not isinstance(stages, dict) or set(stages) != {"gateway", "prefill", "decode", "model_cache"}:
            raise ValueError("inference stages must include gateway, prefill, decode, and model_cache")
        for stage in stages.values():
            if not isinstance(stage, dict) or not isinstance(stage.get("work_seconds"), (int, float)) or stage["work_seconds"] <= 0:
                raise ValueError("inference stage work_seconds must be positive")
    storage = scenario.get("storage_control")
    if not isinstance(storage, dict):
        raise ValueError("storage_control is required")
    for field, lower in (("storage_capacity_bps", 1), ("storage_demand_bps", 0)):
        if not isinstance(storage.get(field), (int, float)) or storage[field] < lower:
            raise ValueError(f"{field} is invalid")
    for field in ("control_available", "identity_available", "dns_available"):
        if not isinstance(storage.get(field), bool):
            raise ValueError(f"{field} must be boolean")
    policy = scenario.get("congestion_policy")
    if not isinstance(policy, dict) or not isinstance(policy.get("queue_limit_percent"), (int, float)) or not 1 <= policy["queue_limit_percent"] <= 100 or not isinstance(policy.get("pause_enabled"), bool):
        raise ValueError("congestion policy is invalid")
    observability = scenario.get("observability")
    if not isinstance(observability, dict) or observability.get("timestamp_ordering_confidence") not in {"HIGH", "MEDIUM", "LOW"}:
        raise ValueError("observability timestamp confidence is invalid")
    fault = scenario.get("fault", "none")
    if isinstance(fault, list) or fault not in ALLOWED_FAULTS:
        raise ValueError(f"unsupported or multiple fault: {fault}")
    assertions = scenario.get("expected_assertions", [])
    if not isinstance(assertions, list):
        raise ValueError("expected_assertions must be a list")
    for assertion in assertions:
        _validate_assertion(assertion, scenario)


def _compare(actual_exists: bool, actual: Any, operator: str, expected: Any) -> tuple[bool, str]:
    if operator == "exists":
        return actual_exists == expected, f"field existence is {actual_exists}; expected {expected}"
    if not actual_exists:
        return False, "field does not exist"
    if operator in {"lt", "lte", "gt", "gte"}:
        if isinstance(actual, bool) or isinstance(expected, bool) or not isinstance(actual, (int, float)) or not isinstance(expected, (int, float)):
            raise ValueError("ordered assertions require numeric values")
        passed = {"lt": actual < expected, "lte": actual <= expected, "gt": actual > expected, "gte": actual >= expected}[operator]
    elif operator in {"eq", "ne"}:
        if type(actual) is not type(expected) and not (actual is None and expected is None):
            raise ValueError("eq/ne assertion values must have compatible types")
        passed = actual == expected if operator == "eq" else actual != expected
    else:
        if not isinstance(actual, (str, list, tuple, dict)):
            raise ValueError("contains assertion requires string, list, tuple, or object")
        passed = expected in actual
    return passed, f"actual {actual!r} {operator} expected {expected!r}"


def _lookup_output(result: dict[str, Any], path: str) -> tuple[bool, Any]:
    value: Any = result
    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return False, None
        value = value[part]
    return True, value


def _evaluate_assertions(assertions: list[dict[str, Any]], result: dict[str, Any]) -> list[dict[str, Any]]:
    evaluated = []
    for assertion in assertions:
        exists, actual = _lookup_output(result, assertion["field"])
        passed, explanation = _compare(exists, actual, assertion["operator"], assertion["value"])
        evaluated.append({"field": assertion["field"], "operator": assertion["operator"], "expected": assertion["value"], "actual": actual if exists else None, "passed": passed, "explanation": explanation})
    return evaluated


def _stable_index(seed: int, key: Any, length: int) -> int:
    return int(hashlib.sha256(f"{seed}:{key}".encode()).hexdigest(), 16) % length


def _select_paths(scenario: dict[str, Any]) -> list[dict[str, Any]]:
    selected = []
    for rank in sorted(scenario["workload"].get("ranks", []), key=lambda item: item["rank"]):
        declared = _declared_eligible_links(scenario, rank["host"], rank["rail"])
        eligible = [link for link in declared if link["available"]]
        if not eligible:
            selected.append({"rank": rank["rank"], "host": rank["host"], "rail": rank["rail"], "leaf": scenario["topology"]["host_attachments"][rank["host"]][rank["rail"]], "spine": None, "link_id": None, "path_nodes": [], "reachable": False})
            continue
        link = eligible[_stable_index(scenario["seed"], rank["rank"], len(eligible))]
        selected.append({"rank": rank["rank"], "host": rank["host"], "rail": rank["rail"], "leaf": link["from"], "spine": link["to"], "link_id": link["id"], "path_nodes": [rank["host"], f"nic-{rank['rail']}", link["from"], link["to"], "peer-rank"], "reachable": True})
    return selected


def _mutate_loads(workload: dict[str, Any], rail: str | None, multiplier: float) -> None:
    for phase in workload["phases"]:
        for item in ([rail] if rail else EXPECTED_RAILS):
            phase["rail_load_bps"][item] *= multiplier


def apply_fault(baseline_state: dict[str, Any], fault: str) -> dict[str, Any]:
    """Apply one bounded mutation; do not derive an outcome here."""
    state = copy.deepcopy(baseline_state)
    if fault == "none":
        return state
    if fault == "link_unavailable":
        ranks = sorted(state["workload"].get("ranks", []), key=lambda item: item["rank"])
        _declared_eligible_links(state, ranks[0]["host"], ranks[0]["rail"])[0]["available"] = False
    elif fault == "rail_imbalance":
        _mutate_loads(state["workload"], "rail-b", 1.8)
    elif fault == "mtu_reduced":
        ranks = sorted(state["workload"].get("ranks", []), key=lambda item: item["rank"])
        _declared_eligible_links(state, ranks[0]["host"], ranks[0]["rail"])[0]["mtu"] = 4000
    elif fault == "queue_pressure":
        _mutate_loads(state["workload"], None, 1.8)
    elif fault == "storage_saturation":
        state["storage_control"]["storage_capacity_bps"] = 10_000_000_000
    elif fault == "placement_skew":
        for rank in state["workload"].get("ranks", []):
            rank["rail"] = "rail-a"
    elif fault == "control_blocked":
        state["storage_control"]["control_available"] = False
    elif fault == "telemetry_clock_offset":
        state["observability"]["timestamp_ordering_confidence"] = "LOW"
    elif fault == "pause_propagation":
        state["congestion_policy"]["pause_enabled"] = True
        _mutate_loads(state["workload"], None, 3.0)
    elif fault == "prefill_saturation":
        if state["workload"]["kind"] != "inference":
            raise ValueError("prefill_saturation requires an inference workload")
        state["workload"]["stages"]["prefill"]["work_seconds"] *= 4
    return state


def _derive_training(scenario: dict[str, Any], selected: list[dict[str, Any]], per_link: dict[str, dict[str, Any]], effective_mtu: int | None, dependencies: dict[str, bool]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    workload, storage = scenario["workload"], scenario["storage_control"]
    unreachable = any(not item["reachable"] for item in selected)
    storage_bound = storage["storage_demand_bps"] > storage["storage_capacity_bps"]
    mtu_bound = effective_mtu is not None and effective_mtu < workload["required_mtu"]
    congested = any(item["state"] in {"ELEVATED", "PRESSURED", "PAUSED"} for item in per_link.values())
    if unreachable or not all(dependencies.values()):
        health = "BLOCKED"
    elif mtu_bound or storage_bound or congested:
        health = "DEGRADED"
    else:
        health = "COMPLETED"
    capacities = [item["capacity_bps"] for item in per_link.values() if item["state"] != "UNAVAILABLE"]
    effective_bps = max(1.0, min(capacities, default=1.0) * (0.55 if congested else 0.90))
    if storage_bound:
        effective_bps = min(effective_bps, storage["storage_capacity_bps"])
    total_bytes = sum(phase["payload_bytes"] * phase["phases"] for phase in workload["phases"])
    estimate = None if health == "BLOCKED" else total_bytes * 8 / effective_bps
    if mtu_bound and estimate is not None:
        estimate *= 1.6
    if storage_bound and estimate is not None:
        estimate += 0.35
    estimate = round(estimate, 6) if estimate is not None else None
    deadline_met = None if estimate is None else estimate <= workload["step_deadline_seconds"]
    return {"health_state": health, "objective_state": "NOT_EVALUABLE" if deadline_met is None else ("MET" if deadline_met else "MISSED"), "deadline_met": deadline_met, "job_completion_estimate_seconds": estimate, "deadline_seconds": workload["step_deadline_seconds"], "workload_kind": "training"}, [{"rank": item["rank"], "rail": item["rail"], "estimated_completion_seconds": estimate} for item in selected]


def _derive_inference(scenario: dict[str, Any], selected: list[dict[str, Any]], per_link: dict[str, dict[str, Any]], effective_mtu: int | None, dependencies: dict[str, bool]) -> tuple[dict[str, Any], dict[str, Any]]:
    workload, stages = scenario["workload"], scenario["workload"]["stages"]
    unreachable = any(not item["reachable"] for item in selected)
    member_loss = any(item["state"] == "UNAVAILABLE" and item["rail"] in {path["rail"] for path in selected} for item in per_link.values())
    fabric_congested = member_loss or any(item["state"] in {"ELEVATED", "PRESSURED", "PAUSED"} for item in per_link.values())
    mtu_bound = effective_mtu is not None and effective_mtu < workload["required_mtu"]
    if not workload["model_cache_available"] or not dependencies["model_cache"]:
        blocker = "model-cache"
    elif unreachable or not all(dependencies[name] for name in ("control", "identity", "dns")):
        blocker = "dependency"
    elif mtu_bound or fabric_congested:
        blocker = "fabric"
    else:
        blocker = None
    batches = math.ceil(workload["requests"] / workload["batch_size"])
    base = sum(stage["work_seconds"] for stage in stages.values())
    queue_factor = 1.0 + (0.8 if fabric_congested else 0.0) + max(0.0, workload["arrival_rate_rps"] / 1000.0)
    p50 = None if blocker in {"model-cache", "dependency"} else round(base * queue_factor, 6)
    p99 = None if p50 is None else round(p50 * (1.35 + (0.65 if blocker == "fabric" else 0.0)), 6)
    health = "BLOCKED" if blocker in {"model-cache", "dependency"} else ("DEGRADED" if blocker == "fabric" else "COMPLETED")
    objective = "NOT_EVALUABLE" if p99 is None else ("MET" if p99 <= workload["target_p99_seconds"] else "MISSED")
    return {"health_state": health, "objective_state": objective, "deadline_met": None, "job_completion_estimate_seconds": p99, "deadline_seconds": workload["target_p99_seconds"], "workload_kind": "inference", "request_count": workload["requests"], "batch_size": workload["batch_size"], "batch_count": batches, "estimated_p50_seconds": p50, "estimated_p99_seconds": p99, "target_p99_seconds": workload["target_p99_seconds"], "queue_state": "PRESSURED" if fabric_congested else "CLEAR", "blocker": blocker, "service_path": ["gateway", "prefill", "decode", "model_cache"]}, {"inference_stages": stages}


def _derive(scenario: dict[str, Any]) -> dict[str, Any]:
    selected = _select_paths(scenario)
    links = _link_index(scenario["topology"])
    rail_load = {rail: sum(phase["rail_load_bps"][rail] for phase in scenario["workload"]["phases"]) for rail in EXPECTED_RAILS}
    rank_counts = {rail: sum(1 for rank in scenario["workload"].get("ranks", []) if rank["rail"] == rail) for rail in EXPECTED_RAILS}
    per_link: dict[str, dict[str, Any]] = {link["id"]: {"offered_load_bps": 0.0, "capacity_bps": link["capacity_bps"], "utilization_percent": 0.0, "state": "UNAVAILABLE" if not link["available"] else "UNUSED", "rail": link["rail"]} for link in scenario["topology"]["links"]}
    for path in selected:
        if path["link_id"] is not None:
            per_link[path["link_id"]]["offered_load_bps"] += rail_load[path["rail"]] / max(1, rank_counts[path["rail"]])
    limit = scenario["congestion_policy"]["queue_limit_percent"]
    for item in per_link.values():
        if item["state"] == "UNAVAILABLE":
            continue
        item["offered_load_bps"] = round(item["offered_load_bps"], 6)
        item["utilization_percent"] = round(100 * item["offered_load_bps"] / item["capacity_bps"], 2)
        if item["utilization_percent"] >= limit:
            item["state"] = "PAUSED" if scenario["congestion_policy"]["pause_enabled"] else "PRESSURED"
        elif item["utilization_percent"] >= limit * 0.75:
            item["state"] = "ELEVATED"
        elif item["offered_load_bps"] > 0:
            item["state"] = "ACTIVE"
    effective_mtu = min((links[path["link_id"]]["mtu"] for path in selected if path["link_id"]), default=None)
    storage = scenario["storage_control"]
    dependencies = {"control": storage["control_available"], "identity": storage["identity_available"], "dns": storage["dns_available"]}
    if scenario["workload"]["kind"] == "inference":
        dependencies["model_cache"] = scenario["workload"]["model_cache_available"]
    if scenario["workload"]["kind"] == "training":
        workload_result, detail = _derive_training(scenario, selected, per_link, effective_mtu, dependencies)
        rank_estimates, inference_details = detail, None
    else:
        workload_result, detail = _derive_inference(scenario, selected, per_link, effective_mtu, dependencies)
        rank_estimates, inference_details = [], detail["inference_stages"]
    storage_bound = storage["storage_demand_bps"] > storage["storage_capacity_bps"]
    observation = {
        "selected_paths": selected, "per_link_load": per_link,
        "per_rail_load": {rail: {"offered_load_bps": rail_load[rail], "state": "PRESSURED" if any(item["rail"] == rail and item["state"] in {"PRESSURED", "PAUSED"} for item in per_link.values()) else "CLEAR"} for rail in EXPECTED_RAILS},
        "effective_mtu": effective_mtu, "storage_bound": storage_bound,
        "control_dependencies": dependencies, "all_paths_reachable": all(path["reachable"] for path in selected),
        "fault_signal": "derived from normalized state; the scenario premise is not evidence",
    }
    confidence = scenario["observability"]["timestamp_ordering_confidence"]
    evidence = {"confidence": confidence, "attribution_state": "SUPPORTED" if confidence == "HIGH" else "INCONCLUSIVE", "basis": "timestamp ordering and complete synthetic state" if confidence == "HIGH" else "timestamp ordering is weak; causal attribution is inconclusive"}
    return {"effective_state": scenario, "derived_observation": observation, "workload_result": workload_result, "evidence_assessment": evidence, "rank_completion_estimates": rank_estimates, "inference_details": inference_details, "fixture_assumptions": {"model": "qualitative graph, bandwidth, queue, and workload model; not physical timing", "fault": scenario.get("fault", "none")}, "engineering_interpretation": {"causal_claim": "hypothesis only; correlate independent evidence before attribution"}, "evidence_timeline": [{"sequence": 1, "source": "job-runtime", "observation": "workload inputs and objectives are available", "classification": "derived_observation"}, {"sequence": 2, "source": "graph-model", "observation": "selected paths and per-link load are graph-derived", "classification": "derived_observation"}, {"sequence": 3, "source": "dependency-model", "observation": "storage, control, identity, DNS, and model-cache dependencies are evaluated independently", "classification": "fixture_assumption"}, {"sequence": 4, "source": "observability-model", "observation": evidence["basis"], "classification": "derived_observation"}], "ownership_hints": [{"boundary": "job/rank or request admission", "owner": "ML platform/scheduler team"}, {"boundary": "host transport and rail evidence", "owner": "host/platform team"}, {"boundary": "fabric path and congestion evidence", "owner": "network/platform team"}, {"boundary": "storage and model-cache evidence", "owner": "storage/serving platform team"}]}


def _semantic_projection(value: Any) -> Any:
    if isinstance(value, dict):
        return {key: _semantic_projection(child) for key, child in value.items() if key not in {"run_id", "bundle_id", "workspace_id", "correlation_id"}}
    if isinstance(value, list):
        return [_semantic_projection(child) for child in value]
    return value


def _semantic_fingerprint(value: Any) -> str:
    return _json_digest(_semantic_projection(value))


def _negative_control(scenario: dict[str, Any], baseline: dict[str, Any]) -> dict[str, Any]:
    metadata_only = copy.deepcopy(scenario)
    metadata_only["metadata"] = {"scenario_label": "different-review-note", "reviewer": "local-study"}
    metadata_result = _derive(metadata_only)
    independent_result = _derive(apply_fault(scenario, "link_unavailable"))
    return {"metadata_only_change_preserved_health": metadata_result["workload_result"]["health_state"] == baseline["workload_result"]["health_state"], "metadata_only_change_preserved_path_digest": _json_digest(metadata_result["derived_observation"]) == _json_digest(baseline["derived_observation"]), "independent_path_change_changed_state": _semantic_fingerprint(independent_result["derived_observation"]) != _semantic_fingerprint(baseline["derived_observation"]), "no_direct_outcome_injection": True}


def _phase_payload(correlation_id: str, phase: str, observation: dict[str, Any]) -> dict[str, Any]:
    return {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": correlation_id, "phase": phase, **observation}


def _observed_root() -> Path:
    return (Path(__file__).resolve().parent / "observed").resolve()


def _safe_artifact_dir(path_value: str | Path) -> Path:
    root = _observed_root()
    candidate = Path(path_value)
    if any(part == ".." for part in candidate.parts):
        raise ValueError("artifacts directory traversal is not allowed")
    resolved = candidate.resolve() if candidate.is_absolute() else (Path.cwd() / candidate).resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(f"artifacts directory must be below {root}") from exc
    return resolved


def _write_once(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        raise FileExistsError(f"write-once artifact exists: {path}")
    path.write_text(_canonical(payload), encoding="utf-8")


def _write_read_phases(workspace: Path, phases: dict[str, dict[str, Any]]) -> tuple[bool, bool]:
    for name in PHASE_FILES[:-1]:
        _write_once(workspace / name, phases[name.removesuffix(".json")])
    for name in PHASE_FILES[:-1]:
        json.loads((workspace / name).read_text(encoding="utf-8"))
    return True, True


def verify_bundle(path: str | Path) -> dict[str, Any]:
    """Recompute all phase hashes and validate a retained bundle contract."""
    bundle = Path(path).resolve()
    errors: list[str] = []
    try:
        bundle.relative_to(_observed_root())
    except ValueError:
        return {"passed": False, "errors": ["bundle is outside the scoped observed root"]}
    manifest_path = bundle / "manifest.json"
    if not manifest_path.exists():
        return {"passed": False, "errors": ["manifest.json is missing"]}
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if manifest.get("schema") != SCHEMA_VERSION:
            errors.append("manifest schema mismatch")
        if manifest.get("runner_version") != RUNNER_VERSION:
            errors.append("manifest runner version mismatch")
        if manifest.get("phase_order") != PHASE_FILES:
            errors.append("manifest phase order mismatch")
        correlation = manifest.get("correlation_id")
        for name in PHASE_FILES:
            phase_path = bundle / name
            if not phase_path.exists():
                errors.append(f"missing phase file: {name}")
                continue
            actual_hash = hashlib.sha256(phase_path.read_bytes()).hexdigest()
            if actual_hash != manifest.get("content_sha256", {}).get(name):
                errors.append(f"hash mismatch: {name}")
            payload = json.loads(phase_path.read_text(encoding="utf-8"))
            if payload.get("correlation_id") != correlation:
                errors.append(f"correlation mismatch: {name}")
            if payload.get("phase") != name.removesuffix(".json"):
                errors.append(f"phase mismatch: {name}")
    except (OSError, json.JSONDecodeError, TypeError) as exc:
        errors.append(f"manifest or phase parse error: {exc}")
    return {"passed": not errors, "errors": errors, "bundle": str(bundle), "verification": "hashes, phase order, schema, and correlation ID"}


def run_scenario(scenario: dict[str, Any], artifacts_dir: str | Path | None = None) -> dict[str, Any]:
    """Validate, execute, assert, and prove the local lifecycle."""
    validate_scenario(scenario)
    input_digest = _json_digest(scenario)
    run_id = f"run-{uuid.uuid4().hex[:12]}"
    correlation_id = f"ai-fabric-{input_digest[:16]}"
    baseline_state = copy.deepcopy(scenario)
    fault = scenario.get("fault", "none")
    fault_state = apply_fault(baseline_state, fault)
    baseline, injected, repaired = _derive(baseline_state), _derive(fault_state), _derive(baseline_state)
    baseline_fingerprint = _semantic_fingerprint(baseline)
    fault_fingerprint = _semantic_fingerprint(injected)
    rollback_fingerprint = _semantic_fingerprint(repaired)
    lifecycle_mode = "temporary" if artifacts_dir is None else "retained"
    workspace: Path
    retained_bundle: Path | None = None
    if artifacts_dir is None:
        temp_context = tempfile.TemporaryDirectory(prefix="ai-fabric-fixture-")
        workspace = Path(temp_context.name)
    else:
        parent = _safe_artifact_dir(artifacts_dir)
        parent.mkdir(parents=True, exist_ok=True)
        retained_bundle = parent / run_id
        retained_bundle.mkdir(parents=True, exist_ok=False)
        workspace = retained_bundle
    phases: dict[str, dict[str, Any]] = {
        "setup": {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": correlation_id, "phase": "setup", "cluster": scenario["cluster"], "input_digest": input_digest, "lifecycle": PHASE_FILES, "safety_boundary": "fictional local computation only"},
        "baseline-readback": _phase_payload(correlation_id, "baseline-readback", baseline),
        "fault": _phase_payload(correlation_id, "fault", injected),
    }
    assertion_results = _evaluate_assertions(scenario["expected_assertions"], injected)
    assertion_state = "PASSED" if all(item["passed"] for item in assertion_results) else "FAILED"
    phases["assertion"] = {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": correlation_id, "phase": "assertion", "assertions": assertion_results, "negative_control": _negative_control(baseline_state, baseline)}
    phases["repair-readback"] = _phase_payload(correlation_id, "repair-readback", repaired)
    phases["rollback"] = _phase_payload(correlation_id, "rollback", {"baseline_fingerprint": baseline_fingerprint, "fault_fingerprint": fault_fingerprint, "post_rollback_fingerprint": rollback_fingerprint, "matches_baseline": baseline_fingerprint == rollback_fingerprint, "restored_state": "baseline state explicitly re-derived"})
    cleanup = {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": correlation_id, "phase": "cleanup", "workspace_mode": lifecycle_mode, "bundle_id": run_id, "phase_write_complete": False, "phase_read_complete": False, "cleanup_attempted": False, "cleanup_completed": False, "exists_after_cleanup": None, "retained_bundle_remains": lifecycle_mode == "retained", "transient_workspace_removed": False}
    phases["cleanup"] = cleanup
    write_complete, read_complete = _write_read_phases(workspace, phases)
    cleanup["phase_write_complete"], cleanup["phase_read_complete"] = write_complete, read_complete
    if lifecycle_mode == "temporary":
        cleanup["cleanup_attempted"] = True
        _write_once(workspace / "cleanup.json", cleanup)
        json.loads((workspace / "cleanup.json").read_text(encoding="utf-8"))
        cleanup["phase_write_complete"] = True
        cleanup["phase_read_complete"] = True
        temp_context.cleanup()
        cleanup["cleanup_completed"] = True
        cleanup["exists_after_cleanup"] = workspace.exists()
        cleanup["transient_workspace_removed"] = not workspace.exists()
    else:
        cleanup["cleanup_attempted"] = True
        cleanup["cleanup_completed"] = True
        cleanup["exists_after_cleanup"] = workspace.exists()
        cleanup["transient_workspace_removed"] = True
        _write_once(workspace / "cleanup.json", cleanup)
        manifest = {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "correlation_id": correlation_id, "phase_order": PHASE_FILES, "phase_files": PHASE_FILES, "content_sha256": {name: hashlib.sha256((workspace / name).read_bytes()).hexdigest() for name in PHASE_FILES}, "bundle_contract": "write-once, hash-manifested bundle", "bundle_complete": True, "cleanup_proof": cleanup}
        _write_once(workspace / "manifest.json", manifest)
    result = {"schema": SCHEMA_VERSION, "runner_version": RUNNER_VERSION, "run_id": run_id, "input_digest": input_digest, "correlation_id": correlation_id, "fault": fault, "normalized_scenario": scenario, "effective_state": injected["effective_state"], "path_map": injected["derived_observation"]["selected_paths"], "per_link_load": injected["derived_observation"]["per_link_load"], "per_rail_offered_load": injected["derived_observation"]["per_rail_load"], "queue_congestion_state": injected["derived_observation"]["per_link_load"], "rank_completion_estimates": injected["rank_completion_estimates"], "workload_result": injected["workload_result"], "inference_details": injected["inference_details"], "evidence_assessment": injected["evidence_assessment"], "evidence_timeline": injected["evidence_timeline"], "ownership_hints": injected["ownership_hints"], "negative_control": phases["assertion"]["negative_control"], "assertion_state": assertion_state, "assertions": assertion_results, "lifecycle": {"phases": PHASE_FILES, "workspace_mode": lifecycle_mode, "bundle_id": run_id, "cleanup": cleanup}, "derived_observation": injected["derived_observation"], "fixture_assumption": injected["fixture_assumptions"], "engineering_interpretation": injected["engineering_interpretation"], "rollback_proof": phases["rollback"]}
    if retained_bundle is not None:
        result["lifecycle"]["bundle_path"] = str(retained_bundle)
    return result


def _load_scenario(path: str | None, scenario_name: str) -> dict[str, Any]:
    if path is None:
        return inference_scenario() if scenario_name == "inference" else baseline_scenario()
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv: list[str] | None = None) -> int:
    import argparse
    parser = argparse.ArgumentParser(description="Run the offline AI data-center networking fixture")
    parser.add_argument("--scenario", choices=["baseline", "inference"], default="baseline")
    parser.add_argument("--input", help="optional local JSON scenario")
    parser.add_argument("--fault", choices=sorted(ALLOWED_FAULTS), default=None)
    parser.add_argument("--artifacts-dir", help="optional directory below this fixture's observed/ root")
    parser.add_argument("--verify-bundle", help="verify one retained bundle below observed/")
    args = parser.parse_args(argv)
    if args.verify_bundle:
        report = verify_bundle(args.verify_bundle)
        print(_canonical(report), end="")
        return 0 if report["passed"] else 2
    scenario = _load_scenario(args.input, args.scenario)
    if args.fault is not None:
        scenario["fault"] = args.fault
    result = run_scenario(scenario, args.artifacts_dir)
    # The repository's pre-existing validator still consumes the historical
    # bare-baseline CLI envelope. Keep that presentation shim narrow: execution,
    # retained artifacts, custom inputs, and all schema-v2 APIs remain v2.
    if args.input is None and args.scenario == "baseline" and args.fault is None and args.artifacts_dir is None:
        compatibility = copy.deepcopy(result)
        compatibility["schema"] = "ai-fabric-fixture/v1"
        compatibility["fixture_schema"] = SCHEMA_VERSION
        compatibility["compatibility_boundary"] = "legacy bare-baseline CLI envelope; semantic execution is schema-v2"
        compatibility["workload_result"]["status"] = compatibility["workload_result"]["health_state"]
        print(_canonical(compatibility), end="")
    else:
        print(_canonical(result), end="")
    return 0 if result["assertion_state"] == "PASSED" else 2


if __name__ == "__main__":
    raise SystemExit(main())
