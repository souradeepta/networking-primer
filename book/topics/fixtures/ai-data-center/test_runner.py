#!/usr/bin/env python3
"""Dependency-free contract tests for the AI data-center fixture."""

from __future__ import annotations

import copy
import hashlib
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

    def test_deterministic_normalized_result(self) -> None:
        first = runner.run_scenario(self.scenario)
        second = runner.run_scenario(copy.deepcopy(self.scenario))
        first["run_id"] = second["run_id"] = "ignored-non-semantic-run-id"
        self.assertEqual(runner._canonical(first), runner._canonical(second))

    def test_invalid_inputs_are_rejected(self) -> None:
        cases = []
        missing = copy.deepcopy(self.scenario)
        del missing["topology"]["hosts"]
        cases.append(missing)
        unknown_rail = copy.deepcopy(self.scenario)
        unknown_rail["workload"]["ranks"][0]["rail"] = "rail-z"
        cases.append(unknown_rail)
        negative_capacity = copy.deepcopy(self.scenario)
        negative_capacity["topology"]["links"][0]["capacity_bps"] = -1
        cases.append(negative_capacity)
        invalid_mtu = copy.deepcopy(self.scenario)
        invalid_mtu["topology"]["links"][0]["mtu"] = 100
        cases.append(invalid_mtu)
        multiple_faults = copy.deepcopy(self.scenario)
        multiple_faults["fault"] = ["rail_imbalance", "storage_saturation"]
        cases.append(multiple_faults)
        unsupported = copy.deepcopy(self.scenario)
        unsupported["workload"]["kind"] = "quantum"
        cases.append(unsupported)
        for case in cases:
            with self.assertRaises(ValueError):
                runner.run_scenario(case)

    def test_allowlisted_faults_derive_a_difference(self) -> None:
        baseline = runner.run_scenario(self.scenario)
        baseline_digest = hashlib.sha256(runner._canonical(baseline["derived_observation"]).encode()).hexdigest()
        for fault in sorted(runner.ALLOWED_FAULTS - {"none"}):
            scenario = copy.deepcopy(self.scenario)
            scenario["fault"] = fault
            result = runner.run_scenario(scenario)
            digest = hashlib.sha256(runner._canonical(result["derived_observation"]).encode()).hexdigest()
            self.assertNotEqual(digest, baseline_digest, fault)

    def test_caller_cannot_inject_conclusion(self) -> None:
        for field in ("healthy", "root_cause", "job_success", "success", "outcome"):
            scenario = copy.deepcopy(self.scenario)
            scenario["metadata"][field] = True
            with self.assertRaises(ValueError):
                runner.run_scenario(scenario)

    def test_negative_control_and_independent_symptom(self) -> None:
        baseline = runner.run_scenario(self.scenario)
        negative = baseline["negative_control"]
        self.assertTrue(negative["metadata_only_change_preserved_status"])
        self.assertTrue(negative["metadata_only_change_preserved_path_digest"])
        self.assertTrue(negative["independent_path_change_degraded"])
        storage = copy.deepcopy(self.scenario)
        storage["fault"] = "storage_saturation"
        fabric = copy.deepcopy(self.scenario)
        fabric["fault"] = "rail_imbalance"
        self.assertEqual(runner.run_scenario(storage)["workload_result"]["status"], runner.run_scenario(fabric)["workload_result"]["status"])
        self.assertNotEqual(runner.run_scenario(storage)["derived_observation"]["fault_signal"], runner.run_scenario(fabric)["derived_observation"]["fault_signal"])

    def test_retained_manifest_hashes_and_cleanup(self) -> None:
        observed = Path(runner.__file__).resolve().parent / "observed"
        with tempfile.TemporaryDirectory(dir=observed, prefix="test-run-") as parent:
            result = runner.run_scenario(self.scenario, parent)
            bundles = list(Path(parent).glob("run-*"))
            self.assertEqual(len(bundles), 1)
            bundle = bundles[0]
            manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
            self.assertTrue(manifest["immutable"])
            self.assertEqual(manifest["correlation_id"], result["correlation_id"])
            for phase in runner.PHASE_FILES:
                self.assertEqual(hashlib.sha256((bundle / phase).read_bytes()).hexdigest(), manifest["content_sha256"][phase])
                payload = json.loads((bundle / phase).read_text(encoding="utf-8"))
                if phase != "cleanup.json":
                    self.assertEqual(payload["correlation_id"], result["correlation_id"])
            self.assertTrue(json.loads((bundle / "cleanup.json").read_text(encoding="utf-8"))["temporary_workspace_removed"])
        self.assertFalse(Path(parent).exists())

    def test_artifact_path_is_scoped(self) -> None:
        with self.assertRaises(ValueError):
            runner.run_scenario(self.scenario, "/tmp/not-the-fixture-root")
        with self.assertRaises(ValueError):
            runner.run_scenario(self.scenario, Path(runner.__file__).resolve().parent / "observed" / ".." / "escape")


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(FixtureContractTests)
    result = unittest.TextTestRunner(verbosity=1).run(suite)
    raise SystemExit(0 if result.wasSuccessful() else 1)
