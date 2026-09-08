#!/usr/bin/env python3
"""Standard-library contract tests for the schema-v2 AI-fabric fixture."""

from __future__ import annotations

import copy
import contextlib
import io
import json
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import runner  # noqa: E402


class FixtureContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.scenario = runner.baseline_scenario()

    def test_t01_baseline_paths_and_load_conservation(self) -> None:
        result = runner.run_scenario(self.scenario)
        links = {item["id"]: item for item in self.scenario["topology"]["links"]}
        for path in result["derived_observation"]["selected_paths"]:
            self.assertTrue(path["reachable"])
            link = links[path["link_id"]]
            self.assertTrue(link["available"])
            self.assertEqual(link["rail"], path["rail"])
            self.assertEqual(link["from"], path["leaf"])
        for rail in runner.EXPECTED_RAILS:
            offered = result["derived_observation"]["per_rail_load"][rail]["offered_load_bps"]
            selected = sum(item["offered_load_bps"] for item in result["per_link_load"].values() if item["rail"] == rail)
            self.assertAlmostEqual(offered, selected)

    def test_t02_alternate_attachment_uses_declared_members(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["topology"]["host_attachments"]["gpu-a1"]["rail-a"] = "leaf-b"
        result = runner.run_scenario(scenario)
        path = next(item for item in result["path_map"] if item["host"] == "gpu-a1")
        self.assertEqual(path["leaf"], "leaf-b")
        self.assertIn(path["link_id"], {link["id"] for link in scenario["topology"]["links"] if link["from"] == "leaf-b" and link["rail"] == "rail-a"})

    def test_t03_missing_compatible_member_rejected(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["topology"]["links"] = [link for link in scenario["topology"]["links"] if not (link["from"] == "leaf-a" and link["rail"] == "rail-a")]
        with self.assertRaises(ValueError):
            runner.run_scenario(scenario)

    def test_t04_link_fault_reroutes(self) -> None:
        baseline = runner.run_scenario(self.scenario)
        result = runner.run_scenario({**copy.deepcopy(self.scenario), "fault": "link_unavailable"})
        affected = next(item for item in baseline["path_map"] if item["rank"] == 0)
        rerouted = next(item for item in result["path_map"] if item["rank"] == 0)
        self.assertNotEqual(affected["link_id"], rerouted["link_id"])
        self.assertTrue(rerouted["reachable"])
        self.assertEqual(result["effective_state"]["topology"]["links"][0]["available"], False)

    def test_t05_all_members_unavailable_blocks(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        for link in scenario["topology"]["links"]:
            if link["from"] == "leaf-a" and link["rail"] == "rail-a":
                link["available"] = False
        result = runner.run_scenario(scenario)
        self.assertEqual(result["workload_result"]["health_state"], "BLOCKED")
        self.assertFalse(result["derived_observation"]["all_paths_reachable"])

    def test_t06_direct_mtu_state_with_none_fault(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["topology"]["links"][0]["mtu"] = 4000
        result = runner.run_scenario(scenario)
        self.assertEqual(result["fault"], "none")
        self.assertEqual(result["derived_observation"]["effective_mtu"], 4000)
        self.assertEqual(result["workload_result"]["health_state"], "DEGRADED")

    def test_t07_dependencies_are_live(self) -> None:
        for field, name in (("dns_available", "dns"), ("identity_available", "identity")):
            scenario = copy.deepcopy(self.scenario)
            scenario["storage_control"][field] = False
            result = runner.run_scenario(scenario)
            self.assertEqual(result["workload_result"]["health_state"], "BLOCKED")
            self.assertFalse(result["derived_observation"]["control_dependencies"][name])

    def test_t08_pause_requires_policy_and_overload(self) -> None:
        no_policy = copy.deepcopy(self.scenario)
        for phase in no_policy["workload"]["phases"]:
            phase["rail_load_bps"]["rail-a"] = 200_000_000_000
        result = runner.run_scenario(no_policy)
        self.assertNotIn("PAUSED", {item["state"] for item in result["per_link_load"].values()})
        paused = copy.deepcopy(no_policy)
        paused["congestion_policy"]["pause_enabled"] = True
        result = runner.run_scenario(paused)
        self.assertIn("PAUSED", {item["state"] for item in result["per_link_load"].values()})

    def test_t09_telemetry_is_not_health(self) -> None:
        baseline = runner.run_scenario(self.scenario)
        scenario = copy.deepcopy(self.scenario)
        scenario["fault"] = "telemetry_clock_offset"
        offset = runner.run_scenario(scenario)
        self.assertEqual(offset["workload_result"], baseline["workload_result"])
        self.assertEqual(offset["evidence_assessment"]["confidence"], "LOW")
        self.assertEqual(offset["evidence_assessment"]["attribution_state"], "INCONCLUSIVE")

    def test_t10_deadline_is_independent(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["workload"]["step_deadline_seconds"] = 0.001
        result = runner.run_scenario(scenario)
        self.assertEqual(result["workload_result"]["health_state"], "COMPLETED")
        self.assertFalse(result["workload_result"]["deadline_met"])
        self.assertEqual(result["workload_result"]["objective_state"], "MISSED")

    def test_t11_false_assertion_is_visible(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["expected_assertions"][0]["value"] = "BLOCKED"
        result = runner.run_scenario(scenario)
        self.assertEqual(result["assertion_state"], "FAILED")
        self.assertFalse(result["assertions"][0]["passed"])
        self.assertEqual(result["assertions"][0]["actual"], "COMPLETED")
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(runner.main(["--input", self._write_scenario(scenario)]), 2)

    def test_t12_assertion_grammar(self) -> None:
        path_value = runner.run_scenario(self.scenario)["path_map"][0]
        for operator, value in (("eq", "COMPLETED"), ("ne", "BLOCKED"), ("contains", path_value), ("exists", True)):
            scenario = copy.deepcopy(self.scenario)
            field = "workload_result.health_state" if operator != "contains" else "derived_observation.selected_paths"
            if operator == "exists":
                field = "derived_observation.storage_bound"
            scenario["expected_assertions"] = [{"field": field, "operator": operator, "value": value}]
            self.assertEqual(runner.run_scenario(scenario)["assertion_state"], "PASSED")
        unknown = copy.deepcopy(self.scenario)
        unknown["expected_assertions"] = [{"field": "workload_result.status", "operator": "eq", "value": "COMPLETED"}]
        with self.assertRaises(ValueError):
            runner.run_scenario(unknown)
        malformed = copy.deepcopy(self.scenario)
        malformed["expected_assertions"] = [{"field": "workload_result.health_state", "operator": "eq", "value": "COMPLETED", "extra": True}]
        with self.assertRaises(ValueError):
            runner.run_scenario(malformed)
        type_mismatch = copy.deepcopy(self.scenario)
        type_mismatch["expected_assertions"] = [{"field": "workload_result.health_state", "operator": "eq", "value": True}]
        with self.assertRaises(ValueError):
            runner.run_scenario(type_mismatch)

    def _write_scenario(self, scenario: dict[str, object]) -> str:
        handle = tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False)
        json.dump(scenario, handle)
        handle.close()
        self.addCleanup(Path(handle.name).unlink, missing_ok=True)
        return handle.name

    def test_t13_temporary_lifecycle(self) -> None:
        result = runner.run_scenario(self.scenario)
        cleanup = result["lifecycle"]["cleanup"]
        self.assertTrue(cleanup["phase_write_complete"])
        self.assertTrue(cleanup["phase_read_complete"])
        self.assertTrue(cleanup["cleanup_completed"])
        self.assertFalse(cleanup["exists_after_cleanup"])

    def test_t14_retained_lifecycle_and_verify(self) -> None:
        observed = Path(runner.__file__).resolve().parent / "observed"
        with tempfile.TemporaryDirectory(dir=observed, prefix="test-run-") as parent:
            result = runner.run_scenario(self.scenario, parent)
            bundle = Path(result["lifecycle"]["bundle_path"])
            self.assertTrue((bundle / "manifest.json").exists())
            self.assertTrue(runner.verify_bundle(bundle)["passed"])
            cleanup = json.loads((bundle / "cleanup.json").read_text(encoding="utf-8"))
            self.assertTrue(cleanup["retained_bundle_remains"])
            self.assertTrue(cleanup["transient_workspace_removed"])

    def test_t15_manifest_tamper(self) -> None:
        observed = Path(runner.__file__).resolve().parent / "observed"
        with tempfile.TemporaryDirectory(dir=observed, prefix="test-tamper-") as parent:
            result = runner.run_scenario(self.scenario, parent)
            bundle = Path(result["lifecycle"]["bundle_path"])
            phase = bundle / "fault.json"
            phase.write_text(phase.read_text(encoding="utf-8") + "\n", encoding="utf-8")
            report = runner.verify_bundle(bundle)
            self.assertFalse(report["passed"])
            self.assertIn("hash mismatch: fault.json", report["errors"])

    def test_t16_repair_and_rollback(self) -> None:
        scenario = copy.deepcopy(self.scenario)
        scenario["fault"] = "storage_saturation"
        result = runner.run_scenario(scenario)
        self.assertNotEqual(result["rollback_proof"]["fault_fingerprint"], result["rollback_proof"]["baseline_fingerprint"])
        self.assertTrue(result["rollback_proof"]["matches_baseline"])

    def test_t17_baseline_inference(self) -> None:
        result = runner.run_scenario(runner.inference_scenario())
        workload = result["workload_result"]
        self.assertEqual(workload["workload_kind"], "inference")
        self.assertEqual(workload["request_count"], 64)
        self.assertEqual(workload["batch_count"], 8)
        self.assertIsNotNone(workload["estimated_p50_seconds"])
        self.assertIsNotNone(workload["estimated_p99_seconds"])

    def test_t18_inference_competing_faults(self) -> None:
        cache = runner.inference_scenario()
        cache["workload"]["model_cache_available"] = False
        cache_result = runner.run_scenario(cache)
        fabric = runner.inference_scenario()
        fabric["fault"] = "link_unavailable"
        fabric_result = runner.run_scenario(fabric)
        self.assertEqual(cache_result["workload_result"]["blocker"], "model-cache")
        self.assertEqual(fabric_result["workload_result"]["blocker"], "fabric")
        prefill = runner.inference_scenario()
        prefill["fault"] = "prefill_saturation"
        prefill_result = runner.run_scenario(prefill)
        self.assertEqual(prefill_result["workload_result"]["workload_kind"], "inference")

    def test_t19_semantic_determinism(self) -> None:
        first = runner.run_scenario(self.scenario)
        second = runner.run_scenario(copy.deepcopy(self.scenario))
        self.assertEqual(runner._semantic_fingerprint(first), runner._semantic_fingerprint(second))

    def test_t20_caller_conclusion_rejected_for_both_kinds(self) -> None:
        for scenario in (runner.baseline_scenario(), runner.inference_scenario()):
            scenario["metadata"]["root_cause"] = "network"
            with self.assertRaises(ValueError):
                runner.run_scenario(scenario)

    def test_invalid_graph_and_schema_are_rejected(self) -> None:
        duplicate = copy.deepcopy(self.scenario)
        duplicate["topology"]["links"][1]["id"] = duplicate["topology"]["links"][0]["id"]
        with self.assertRaises(ValueError):
            runner.run_scenario(duplicate)
        invalid_endpoint = copy.deepcopy(self.scenario)
        invalid_endpoint["topology"]["links"][0]["to"] = "gpu-a1"
        with self.assertRaises(ValueError):
            runner.run_scenario(invalid_endpoint)
        old = copy.deepcopy(self.scenario)
        old["schema"] = "ai-fabric-fixture/v1"
        with self.assertRaises(ValueError):
            runner.run_scenario(old)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=1).run(unittest.defaultTestLoader.loadTestsFromTestCase(FixtureContractTests))
    raise SystemExit(0 if result.wasSuccessful() else 1)
