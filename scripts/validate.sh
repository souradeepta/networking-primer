#!/usr/bin/env bash
# Validate repository structure and diagram portability without external tools.
set -euo pipefail

required=(
  README.md SPEC.md AGENTS.md MEMORY.md TODO.md LICENSE DISCLOSURES.md docs/README.md docs/markdown-style-guide.md docs/infra-engineer-toolkit.md docs/unix-debugging-sessions.md docs/networking-tools-and-commands.md docs/networking-issue-cheatsheets.md docs/infra-engineer-runbooks-and-exercises.md
  docs/01-foundations.md docs/02-request-path.md docs/03-f5-ltm.md
  docs/04-f5-gtm.md docs/05-troubleshooting.md docs/06-ddi.md
  docs/07-automation.md docs/08-transport-security.md docs/architecture.md
  docs/09-hands-on-labs.md docs/interview-questions.md docs/f5-interview-bank.md docs/networking-interview-bank.md docs/interview-dialogue-exercises.md docs/interview-rubric.md docs/interview-simulation-pack.md docs/interview-whiteboard-drills.md docs/network-system-design-exercises.md docs/interview-study-plan.md docs/staff-interview-rubric.md docs/staff-design-review-pack.md docs/staff-behavioral-exercises.md docs/glossary.md docs/references.md
  book/README.md book/FACT-INFERENCE-LEDGER.md
  examples/request_path.py examples/f5_pool_audit.py
  scripts/check_internal_links.py
  demos/README.md demos/dns_observe.sh demos/tls_inspect.sh
  demos/vip_ltm_model.py demos/certificate_audit.py demos/f5_change_planner.py
  demos/f5_rest_pagination_tasks.py
  demos/animations/request-journey.html demos/animations/dns-failover.html
  demos/docker/README.md demos/docker/compose.yml demos/docker/server.py demos/docker/client.py
  demos/wireshark.md exercises/README.md
)

for path in "${required[@]}"; do
  [[ -f "$path" ]] || { echo "Missing required file: $path" >&2; exit 1; }
done

for animation in demos/animations/*.html; do
  rg -q 'Play|Pause' "$animation" || { echo "Animation lacks controls: $animation" >&2; exit 1; }
  rg -q 'prefers-reduced-motion' "$animation" || { echo "Animation lacks reduced-motion fallback: $animation" >&2; exit 1; }
done

python3 - <<'PY'
from pathlib import Path
import re

chapters = sorted(p for p in Path("book").glob("*.md") if p.name not in {"README.md", "FACT-INFERENCE-LEDGER.md", "ccna-networking-expansion-spec.md", "ccna-networking-expansion-todo.md", "ccna-networking-expansion-review.md", "ccna-terra-remediation-plan.md", "ccna-terra-remediation-handoff.md"})
if len(chapters) < 17:
    raise SystemExit(f"Book edition needs 17 chapters; found {len(chapters)}")
required = [
    "Learning objectives", "Prerequisites", "Mental model", "Worked example",
    "When this breaks", "Operational checklist", "Diagram", "Questions and answers",
]
for path in chapters:
    text = path.read_text(encoding="utf-8")
    missing = [heading for heading in required if f"## {heading}" not in text]
    if missing:
        raise SystemExit(f"{path}: missing headings: {', '.join(missing)}")
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    prose = "\n".join(line for line in prose.splitlines() if not line.startswith(("#", "|", "- ")))
    words = re.findall(r"\b[\w'-]+\b", prose)
    minimum = 1500 if path.name.startswith(("15-", "16-", "17-")) else 1200
    if len(words) < minimum:
        raise SystemExit(f"{path}: needs {minimum} prose words; found {len(words)}")
    qa = re.findall(r"^\s*\d+\.\s+\*\*", text, flags=re.MULTILINE)
    if len(qa) < 8:
        raise SystemExit(f"{path}: needs 8 numbered Q&A; found {len(qa)}")
    if "```mermaid" not in text:
        raise SystemExit(f"{path}: missing Mermaid diagram")
    if path.name.startswith(("15-", "16-", "17-")) and "| --- |" not in text:
        raise SystemExit(f"{path}: edition-5 chapter needs a Markdown table")
print(f"Book chapter checks passed: {len(chapters)} chapters.")
PY

python3 - <<'PY'
from pathlib import Path
import re

root = Path("book/ccna-networking")
expected = ["00-README.md"] + [
    f"{n:02d}-" + name for n, name in enumerate([
        "network-models-and-physical.md", "ethernet-switching-and-vlans.md",
        "stp-lacp-and-layer2-resilience.md", "ipv4-subnetting-nat-and-ipv6.md",
        "routing-static-ospf-and-vrf.md", "bgp-policy-and-hybrid-wan.md",
        "network-services-and-operations.md", "acls-aaa-and-network-security.md",
        "wireless-and-qos.md", "multicast-and-service-delivery.md",
        "data-center-fabrics.md", "cloud-networking-aws-gcp.md",
        "private-public-hybrid-and-onprem.md", "automation-sdn-and-iac.md",
        "observability-troubleshooting-and-design.md",
    ], start=1)
]
actual = sorted(p.name for p in root.glob("*.md")) if root.exists() else []
if actual != sorted(expected):
    raise SystemExit(f"CCNA expansion exact file set mismatch: {actual}; expected: {sorted(expected)}")
readme = (root / "00-README.md").read_text(encoding="utf-8")
if "Atomic concept-to-evidence crosswalk" not in readme:
    raise SystemExit("CCNA README missing atomic concept-to-evidence crosswalk")
if readme.count("| ") < 16:
    raise SystemExit("CCNA README crosswalk is too small")
for name in expected[1:]:
    if f"]({name})" not in readme:
        raise SystemExit(f"CCNA README missing ordered link: {name}")
for path in [root / name for name in expected[1:]]:
    text = path.read_text(encoding="utf-8")
    lowered = text.lower()
    required = ["learning objectives", "prerequisites", "mental model", "verification", "failure", "exercise", "references"]
    missing = [h for h in required if h not in lowered]
    if "questions and answers" not in lowered and "interview q&a" not in lowered:
        missing.append("questions and answers")
    if missing:
        raise SystemExit(f"{path}: missing CCNA contract markers: {', '.join(missing)}")
    if text.count("```mermaid") < 2 or "| --- |" not in text:
        raise SystemExit(f"{path}: needs two Mermaid diagrams and a table")
    if len(re.findall(r"^\s*\d+\.\s+", text, flags=re.MULTILINE)) < 6:
        raise SystemExit(f"{path}: needs numbered Q&A/exercise entries")
    for heading in ("## J.", "## K.", "## L."):
        if heading not in text:
            raise SystemExit(f"{path}: missing completion heading {heading}")
    for marker in ("Safety", "Baseline", "Injected fault", "Expected output", "Repair", "Rollback", "Cleanup"):
        if marker.lower() not in lowered:
            raise SystemExit(f"{path}: failure lab missing {marker.lower()} field")
    if "criterion" not in lowered and "score" not in lowered:
        raise SystemExit(f"{path}: missing criterion-level completion evidence")
    for label in ("Fact", "Vendor terminology", "Observed lab result", "Engineering inference"):
        if label not in text:
            raise SystemExit(f"{path}: missing evidence label {label}")
print(f"CCNA expansion checks passed: {len(expected)-1} modules and exact index.")
PY

python3 - <<'PY'
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile


def pointer(payload, expression):
    value = payload
    for part in expression.lstrip("/").split("/"):
        if part:
            value = value[int(part)] if isinstance(value, list) else value[part]
    return value


def contains_key(value, names):
    if isinstance(value, dict):
        return any(key in names or contains_key(child, names) for key, child in value.items())
    if isinstance(value, list):
        return any(contains_key(child, names) for child in value)
    return False


runner = Path("book/ccna-networking/fixtures/runner.py")
evaluator = Path("book/ccna-networking/fixtures/evaluator.py")
if not runner.exists() or not evaluator.exists():
    raise SystemExit("CCNA fixture runner/evaluator is missing")
source = runner.read_text(encoding="utf-8") + evaluator.read_text(encoding="utf-8")
if any(token in source for token in ("mechanism_fault", "fault_plane", "probe_healthy")):
    raise SystemExit("legacy coupled fault or caller-supplied probe pattern remains in fixture code")
with tempfile.TemporaryDirectory(prefix="ccna-validator-") as temporary:
    capture = Path(temporary) / "capture"
    result = subprocess.run([sys.executable, str(runner), "--all", "--artifacts-dir", str(capture)], check=True, capture_output=True, text=True)
    if "FIXTURE_PASS modules=15" not in result.stdout or "temporary_workspace_removed=True" not in result.stdout or "no_leak=True" not in result.stdout:
        raise SystemExit("CCNA fixture runner did not prove all modules and cleanup")
    run = json.loads((capture / "run.json").read_text(encoding="utf-8"))
    if run.get("schema") != "ccna-fixture-bundle/v3" or run.get("bundle_count") != 15:
        raise SystemExit("CCNA run record has the wrong schema or module count")
    contract = run.get("semantic_contract", {})
    if contract != {"control_faults_only": True, "data_plane_derived": True, "ownership_probes_derived": True, "reconciliation_model": True}:
        raise SystemExit("CCNA run does not declare the four semantic contracts")
    run_id = run.get("run_id")
    modules = run.get("modules", [])
    if len(modules) != 15 or len({item.get("module_id") for item in modules}) != 15:
        raise SystemExit("CCNA capture must contain 15 unique module bundles")
    required_phases = {"setup.json", "baseline-readback.json", "fault.json", "assertion.json", "repair-readback.json", "rollback.json", "cleanup.json", "manifest.json"}
    for item in modules:
        bundle = capture / item["bundle"]
        if not bundle.is_dir() or not item["correlation_id"].endswith(f"module-{item['module_id']}"):
            raise SystemExit(f"invalid bundle or module correlation ID: {item}")
        manifest = json.loads((bundle / "manifest.json").read_text(encoding="utf-8"))
        if manifest.get("schema") != "ccna-fixture-bundle/v3" or manifest.get("immutable") is not True or manifest.get("bundle_complete") is not True:
            raise SystemExit(f"{bundle}: incomplete immutable v3 manifest")
        if set(manifest.get("phase_files", [])) != required_phases - {"manifest.json"}:
            raise SystemExit(f"{bundle}: phase manifest is incomplete")
        for phase in required_phases:
            path = bundle / phase
            if not path.is_file():
                raise SystemExit(f"{bundle}: missing retained phase {phase}")
            if phase != "manifest.json" and hashlib.sha256(path.read_bytes()).hexdigest() != manifest["content_sha256"].get(phase):
                raise SystemExit(f"{path}: content hash mismatch")
        cleanup = json.loads((bundle / "cleanup.json").read_text(encoding="utf-8"))
        if cleanup.get("temporary_workspace_removed") is not True or cleanup.get("no_leak") is not True or cleanup.get("exists_after_cleanup") is not False:
            raise SystemExit(f"{bundle}: cleanup proof failed")
        phases = {}
        for phase in required_phases - {"manifest.json", "cleanup.json"}:
            phase_payload = json.loads((bundle / phase).read_text(encoding="utf-8"))
            phases[phase] = phase_payload
            if phase_payload.get("runner_version") != manifest.get("runner_version") or phase_payload.get("correlation_id") != item["correlation_id"]:
                raise SystemExit(f"{bundle}/{phase}: version or correlation mismatch")
        for name in ("baseline-readback.json", "fault.json", "repair-readback.json", "rollback.json"):
            payload = phases[name]
            for field in ("desired_request", "controller_result", "authoritative_readback", "device_service_observation"):
                if field not in payload:
                    raise SystemExit(f"{bundle}/{name}: missing reconciliation field {field}")
            rb = payload["authoritative_readback"]
            reconciliation = rb.get("reconciliation", {})
            if not reconciliation.get("task_id") or reconciliation.get("status") not in {"APPLIED", "NO_CHANGE"} or "changed_fields" not in reconciliation:
                raise SystemExit(f"{bundle}/{name}: read-back is not a reconciliation result")
            if not rb.get("requested_fields") or not rb.get("effective_fields") or not reconciliation.get("effective_fields"):
                raise SystemExit(f"{bundle}/{name}: missing requested/effective reconciliation fields")
            if rb.get("effective_fields") == rb.get("requested_fields") or rb.get("effective_state") == payload["desired_request"].get("desired_state"):
                raise SystemExit(f"{bundle}/{name}: read-back is an echo rather than an effective state")
        assertion = phases["assertion.json"]
        negative = assertion.get("negative_control", {})
        if assertion.get("semantic_assertions") != {"control_change_can_leave_dataplane_healthy": True, "independent_path_change_can_fail_dataplane": True, "no_direct_outcome_injection": True, "same_control_readback_can_have_different_path_result": True}:
            raise SystemExit(f"{bundle}: semantic negative test did not pass")
        control_only = negative.get("control_only_change", {})
        independent = negative.get("independent_path_change", {})
        if (control_only.get("evaluator_output", {}).get("healthy") is not True
                or independent.get("evaluator_output", {}).get("healthy") is not False
                or contains_key(independent.get("path_trace", {}), {"healthy", "probe_healthy", "mechanism_fault", "fault_plane"})
                or independent.get("request_status") != "ACCEPTED"
                or independent.get("readback_status") != "ACTIVE"):
            raise SystemExit(f"{bundle}: negative control is not independently derived")
    submissions = json.loads((capture / "completed-submissions.json").read_text(encoding="utf-8"))
    if submissions.get("schema") != "ccna-fixture-bundle/v3" or submissions.get("run_id") != run_id or len(submissions.get("records", [])) != 15:
        raise SystemExit("CCNA capture must contain 15 v3 completed-submission records")
    for record in submissions["records"]:
        if record.get("status") != "completed-local-emulator-submission" or len(record.get("criteria", [])) != 4:
            raise SystemExit(f"{record.get('module_id')}: incomplete submission record")
        total = 0
        for criterion in record["criteria"]:
            pointer_text = criterion.get("json_pointer", "")
            if "/observations/" not in pointer_text or pointer_text.endswith("/healthy") or "health" in criterion.get("threshold", "").lower():
                raise SystemExit(f"{criterion.get('criterion_id')}: generic health-only rubric remains")
            artifact = capture / criterion["artifact_path"]
            if not artifact.is_file():
                raise SystemExit(f"{criterion.get('criterion_id')}: missing artifact")
            observed_value = pointer(json.loads(artifact.read_text(encoding="utf-8")), pointer_text)
            expected = criterion.get("expected_value")
            operator = criterion.get("operator")
            if operator == "eq": computed = observed_value == expected
            elif operator == "ne": computed = observed_value != expected
            elif operator == "ge": computed = observed_value >= expected
            elif operator == "gt": computed = observed_value > expected
            elif operator == "lt": computed = observed_value < expected
            elif operator == "present": computed = observed_value is not None
            elif operator == "missing": computed = observed_value is None
            else: raise SystemExit(f"{criterion.get('criterion_id')}: unknown scoring operator")
            awarded = criterion.get("points_possible") if computed else 0
            if (observed_value != criterion["observed_value"] or computed != criterion.get("pass")
                    or computed != criterion.get("scoring_inputs", {}).get("predicate_result")
                    or awarded != criterion.get("points_awarded")
                    or criterion.get("threshold_decision") != ("PASS" if computed else "FAIL")):
                raise SystemExit(f"{criterion.get('criterion_id')}: observed criterion does not match record")
            if criterion.get("scoring_inputs", {}).get("observed_value") != observed_value or criterion.get("scoring_inputs", {}).get("expected_value") != expected or criterion.get("scoring_inputs", {}).get("operator") != operator:
                raise SystemExit(f"{criterion.get('criterion_id')}: scoring inputs are not reproducible")
            total += awarded
        arithmetic = " + ".join(str(item["points_awarded"]) for item in record["criteria"]) + f" = {total}/100"
        if total != record.get("total_points") or record.get("score_arithmetic") != arithmetic or record.get("score_computed_at_execution") is not True:
            raise SystemExit(f"{record.get('module_id')}: score arithmetic is not reproducible")
    ownership = json.loads((capture / "ownership-records.json").read_text(encoding="utf-8"))
    if ownership.get("schema") != "ccna-fixture-bundle/v3" or ownership.get("run_id") != run_id or len(ownership.get("records", [])) != 24:
        raise SystemExit("CCNA capture must contain 24 v3 ownership records")
    for record in ownership["records"]:
        required = ("owner_id", "object_field_path", "ownership_key", "single_writer_rule", "approver_id", "evidence_owner_id", "rollback_owner_id", "owner_assignment_id", "approver_record_id", "evidence_record_id", "rollback_record_id", "collision_exception_rule", "linked_change_record", "fixture_request", "authoritative_readback", "controller_result", "effective_fields", "traffic_request", "path_trace", "evaluator_output", "collision_result", "negative_control")
        if any(not record.get(field) for field in required):
            raise SystemExit(f"{record.get('record_id')}: incomplete ownership record")
        request, readback = record["fixture_request"], record["authoritative_readback"]
        if request.get("correlation_id") != readback.get("correlation_id") or request.get("correlation_id") != record.get("correlation_id"):
            raise SystemExit(f"{record.get('record_id')}: request/read-back correlation mismatch")
        reconciliation = readback.get("reconciliation", {})
        if (not request.get("status") == "ACCEPTED" or readback.get("status") != "ACTIVE"
                or reconciliation.get("status") not in {"APPLIED", "NO_CHANGE"}
                or not reconciliation.get("task_id") or not reconciliation.get("changed_fields")
                or readback.get("effective_fields") == readback.get("requested_fields")
                or record.get("effective_fields") != readback.get("effective_fields")):
            raise SystemExit(f"{record.get('record_id')}: request/read-back lacks reconciliation evidence")
        if record["evaluator_output"].get("healthy") is not True or "derived_probe" not in record["evaluator_output"]:
            raise SystemExit(f"{record.get('record_id')}: positive evaluator is not derived")
        collision = record["collision_result"]
        if collision.get("status") != "REJECTED_COLLISION" or collision.get("ownership_key") != record.get("ownership_key") or collision.get("writer") == record.get("owner_id"):
            raise SystemExit(f"{record.get('record_id')}: ownership collision was not enforced")
        negative = record["negative_control"]
        if (negative.get("request_status") != "ACCEPTED" or negative.get("readback_status") != "ACTIVE"
                or negative.get("evaluator_output", {}).get("healthy") is not False
                or contains_key(negative.get("path_trace", {}), {"healthy", "probe_healthy", "mechanism_fault", "fault_plane"})):
            raise SystemExit(f"{record.get('record_id')}: request-success/data-plane-failure negative control is incomplete")
    observed = Path("book/ccna-networking/fixtures/observed/run.json")
    if observed.exists() and json.loads(observed.read_text(encoding="utf-8")).get("schema") != "ccna-fixture-bundle/v3":
        raise SystemExit("CCNA observed artifact is stale; regenerate the retained v3 run")
    if observed.exists():
        legacy_tokens = ("ccna-fixture-bundle/v2", "mechanism_fault", "fault_plane", "probe_healthy")
        for artifact in observed.parent.rglob("*.json"):
            content = artifact.read_text(encoding="utf-8")
            if any(token in content for token in legacy_tokens):
                raise SystemExit(f"{artifact}: stale coupled-fault, echo-readback, or caller-probe pattern")
for path in sorted(Path("book/ccna-networking").glob("[0-9][0-9]-*.md")):
    if path.name == "00-README.md":
        continue
    text = path.read_text(encoding="utf-8")
    if "fixtures/observed/" not in text or "fixtures/worked-submissions.md" not in text:
        raise SystemExit(f"{path}: missing artifact-backed submission links")
print("CCNA semantic fixture, reconciliation, module-specific rubric, ownership, negative-control, and cleanup checks passed.")
PY

python3 - <<'PY'
from pathlib import Path
import re

cases = sorted(Path("book/case-studies").glob("*.md"))
cases = [p for p in cases if p.name != "README.md"]
if len(cases) < 19:
    raise SystemExit(f"Need 19 infrastructure case studies; found {len(cases)}")
required = ["Context and goals", "Architecture", "Timeline", "Evidence",
            "Competing hypotheses", "Decision points", "Remediation",
            "Verification", "Rollback or recovery", "Postmortem lessons",
            "Questions and answers"]
for path in cases:
    text = path.read_text(encoding="utf-8")
    missing = [h for h in required if f"## {h}" not in text]
    if missing:
        raise SystemExit(f"{path}: missing case-study headings: {', '.join(missing)}")
    prose = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    prose = re.sub(r"%%\{init:.*?\}%%", "", prose)
    if len(re.findall(r"\b[\w'-]+\b", prose)) < 1500:
        raise SystemExit(f"{path}: needs 1500 prose words")
    if len(re.findall(r"^\s*\d+\.\s+\*\*", text, flags=re.MULTILINE)) < 10:
        raise SystemExit(f"{path}: needs 10 numbered Q&A")
    if "```mermaid" not in text:
        raise SystemExit(f"{path}: missing Mermaid diagram")
    if "| --- |" not in text:
        raise SystemExit(f"{path}: needs at least one Markdown table")
print(f"Infrastructure case-study checks passed: {len(cases)} cases.")
PY

python3 - <<'PY'
from pathlib import Path
import re

topics = sorted(p for p in Path("book/topics").glob("*.md") if p.name != "README.md")
if len(topics) < 37:
    raise SystemExit(f"Need 37 focused topic files; found {len(topics)}")
index = Path("book/topics/README.md").read_text(encoding="utf-8")
indexed = set(re.findall(r"\((\d{2}-[^)]+\.md)\)", index))
actual = {p.name for p in topics}
if indexed != actual:
    missing = sorted(actual - indexed)
    stale = sorted(indexed - actual)
    raise SystemExit(f"Focused topic index mismatch; missing={missing}, stale={stale}")
for path in topics:
    text = path.read_text(encoding="utf-8")
    required = ["Learning objectives", "Worked example", "When this breaks",
                "Operational checklist", "Questions and answers"]
    missing = [h for h in required if f"## {h}" not in text]
    if missing:
        raise SystemExit(f"{path}: missing topic headings: {', '.join(missing)}")
    minimum = 1200 if path.name.startswith(("28-", "29-")) else (600 if path.name.startswith(("22-", "23-", "24-", "25-", "26-", "27-", "30-", "31-", "32-", "33-")) else (1200 if path.name.startswith(("11-", "12-", "13-", "14-", "15-", "16-", "17-", "18-", "19-", "20-", "21-")) else 900))
    if len(re.findall(r"\b[\w'-]+\b", re.sub(r"```.*?```", "", text, flags=re.DOTALL))) < minimum:
        raise SystemExit(f"{path}: needs {minimum} words")
    qa_minimum = 8 if path.name.startswith(("28-", "29-", "30-", "31-", "32-", "33-")) else (6 if path.name.startswith(("11-", "12-", "13-", "14-", "15-", "16-", "17-", "18-", "19-", "20-", "21-", "22-", "23-", "24-", "25-", "26-", "27-")) else 5)
    qa_patterns = (r"^\s*\d+\.\s+\*\*", r"^###\s+\d+\.")
    qa_count = sum(len(re.findall(pattern, text, flags=re.MULTILINE)) for pattern in qa_patterns)
    if qa_count < qa_minimum:
        raise SystemExit(f"{path}: needs {qa_minimum} numbered Q&A")
    if "```mermaid" not in text or "| --- |" not in text:
        raise SystemExit(f"{path}: needs Mermaid diagram and Markdown table")
print(f"Focused topic checks passed: {len(topics)} topics.")
PY

python3 - <<'PY'
from pathlib import Path
import re

def check_answers(paths, minimum, label):
    checked = 0
    for path in paths:
        text = path.read_text(encoding="utf-8")
        match = re.search(r"^## Questions and answers\s*$", text, flags=re.MULTILINE)
        if not match:
            continue
        section = text[match.end():]
        section = re.split(r"^## (?!Questions and answers)", section, maxsplit=1, flags=re.MULTILINE)[0]
        entries = re.split(r"^\s*(?:\d+\.\s+\*\*.*?\*\*|###\s+\d+\..*)", section, flags=re.MULTILINE)
        for answer in entries[1:]:
            words = re.findall(r"\b[\w'-]+\b", answer)
            required_words = 24 if path.name.startswith(("34-", "35-", "36-", "37-")) else (16 if path.name.startswith(("22-", "23-", "24-", "25-", "26-", "27-", "28-", "29-", "30-", "31-", "32-", "33-")) else minimum)
            if len(words) < required_words:
                raise SystemExit(f"{path}: interview answer has {len(words)} words; needs {required_words}")
            checked += 1
    if checked == 0:
        raise SystemExit(f"{label}: no interview answers found")
    print(f"Interview answer-depth checks passed: {checked} answers ({label}).")

check_answers(sorted(Path("book").glob("*.md")), 35, "book chapters")
check_answers(sorted(Path("book/topics").glob("*.md")), 35, "focused topics")
check_answers(sorted(Path("book/case-studies").glob("*.md")), 30, "case studies")
check_answers([Path("docs/interview-questions.md"), Path("docs/10-platform-networking.md")], 25, "quick-start docs")
PY

python3 - <<'PY'
from pathlib import Path
import re

for path in [*Path("docs").glob("*.md"), *Path("book").glob("*.md")]:
    text = path.read_text(encoding="utf-8")
    for block in re.findall(r"```mermaid\n(.*?)```", text, re.DOTALL):
        if not block.isascii():
            raise SystemExit(f"Non-ASCII Mermaid content in {path}")
print("Repository structure and Mermaid ASCII checks passed.")
PY

python3 - <<'PY'
from pathlib import Path
import re

path = Path("docs/f5-interview-bank.md")
text = path.read_text(encoding="utf-8")
questions = re.findall(r"^\d+\.\s+\*\*", text, flags=re.MULTILINE)
exercise_sections = re.findall(r"^## Debugging exercises[^\n]*\n(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
exercises = [item for section in exercise_sections for item in re.findall(r"^\d+\.\s+(?:\*\*)?", section, flags=re.MULTILINE)]
if len(questions) < 60:
    raise SystemExit(f"F5 interview bank needs at least 60 questions; found {len(questions)}")
if len(exercises) < 16:
    raise SystemExit(f"F5 interview bank needs 16 debugging exercises; found {len(exercises)}")
print(f"F5 interview bank checks passed: {len(questions)} questions, {len(exercises)} debugging exercises.")
PY

python3 - <<'PY'
from pathlib import Path
import re

path = Path("docs/networking-interview-bank.md")
text = path.read_text(encoding="utf-8")
questions = re.findall(r"^\d+\.\s+\*\*", text, flags=re.MULTILINE)
exercise_sections = re.findall(r"^## Debugging exercises[^\n]*\n(.*?)(?=^## |\Z)", text, flags=re.MULTILINE | re.DOTALL)
exercises = [item for section in exercise_sections for item in re.findall(r"^\d+\.\s+(?:\*\*)?", section, flags=re.MULTILINE)]
if len(questions) < 60:
    raise SystemExit(f"Networking interview bank needs at least 60 questions; found {len(questions)}")
if len(exercises) < 16:
    raise SystemExit(f"Networking interview bank needs 16 debugging exercises; found {len(exercises)}")
print(f"Networking interview bank checks passed: {len(questions)} questions, {len(exercises)} debugging exercises.")
PY

python3 - <<'PY'
from pathlib import Path
import re

checks = {
    "docs/interview-rubric.md": (r"^\d+\.\s+\*\*", 12, "scored exemplars"),
    "docs/interview-simulation-pack.md": (r"^\d+\.\s+", 20, "simulation scenarios"),
    "docs/interview-whiteboard-drills.md": (r"^\d+\.\s+", 15, "whiteboard drills"),
    "docs/network-system-design-exercises.md": (r"^\d+\.\s+\*\*", 10, "system-design exercises"),
}
for filename, (pattern, minimum, label) in checks.items():
    text = Path(filename).read_text(encoding="utf-8")
    count = len(re.findall(pattern, text, flags=re.MULTILINE))
    if count < minimum:
        raise SystemExit(f"{filename}: needs {minimum} {label}; found {count}")
sim = Path("docs/interview-simulation-pack.md").read_text(encoding="utf-8")
for marker in ("Detailed conversation transcripts", "Interviewer", "Candidate", "Follow-up", "Wrong path", "Boundary", "Scorecard"):
    if marker not in sim:
        raise SystemExit(f"simulation pack missing detailed marker: {marker}")
if len(re.findall(r"^### Scenario", sim, flags=re.MULTILINE)) < 5:
    raise SystemExit("simulation pack needs at least five detailed transcript scenarios")
drills = Path("docs/interview-whiteboard-drills.md").read_text(encoding="utf-8")
for marker in ("Worked answer", "Assume", "falsifier", "Calculation", "```mermaid"):
    if marker not in drills:
        raise SystemExit(f"whiteboard drills missing detailed marker: {marker}")
design = Path("docs/network-system-design-exercises.md").read_text(encoding="utf-8")
for marker in ("Worked design", "Requirements and assumptions", "Capacity", "Observability", "Follow-ups", "```mermaid"):
    if marker not in design:
        raise SystemExit(f"system-design exercises missing detailed marker: {marker}")
print("Interview practice structure checks passed: rubric, simulations, drills, and design exercises.")
PY

python3 - <<'PY'
from pathlib import Path
import re

required = {
    "docs/staff-interview-rubric.md": ("## Scorecard", "## Staff answer shape", "## Readiness gate"),
    "docs/staff-design-review-pack.md": ("## Design prompts", "## Required review artifact"),
    "docs/staff-behavioral-exercises.md": ("## Review checklist",),
}
for filename, markers in required.items():
    text = Path(filename).read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            raise SystemExit(f"{filename}: missing {marker}")
pack = Path("docs/staff-design-review-pack.md").read_text(encoding="utf-8")
behavioral = Path("docs/staff-behavioral-exercises.md").read_text(encoding="utf-8")
if len(re.findall(r"^\d+\.\s+\*\*", pack, flags=re.MULTILINE)) < 12:
    raise SystemExit("Staff design pack needs 12 prompts")
if len(re.findall(r"^\d+\.\s+", behavioral, flags=re.MULTILINE)) < 12:
    raise SystemExit("Staff behavioral pack needs 12 prompts")
print("Staff curriculum checks passed: rubric, design, and behavioral packs.")
PY

python3 - <<'PY'
from pathlib import Path
import re

path = Path("docs/interview-dialogue-exercises.md")
text = path.read_text(encoding="utf-8")
scenarios = re.findall(r"^## \d+\.", text, flags=re.MULTILINE)
if len(scenarios) < 12:
    raise SystemExit(f"Dialogue exercise bank needs 12 scenarios; found {len(scenarios)}")
if "Interviewer" not in text or "Candidate" not in text or "## Evidence table template" not in text:
    raise SystemExit("Dialogue exercise bank is missing conversation/evidence structure")
print(f"Dialogue exercise checks passed: {len(scenarios)} scenarios.")
PY

python3 scripts/check_internal_links.py

python3 - <<'PY'
from pathlib import Path
import re

docs = {path.name for path in Path('docs').glob('*.md') if path.name != 'README.md'}
index = Path('docs/README.md').read_text(encoding='utf-8')
indexed = {
    Path(target).name
    for target in re.findall(r'\[[^]]+\]\(([^)]+\.md)\)', index)
    if '/' not in target and not target.startswith('#')
}
missing = sorted(docs - indexed)
if missing:
    raise SystemExit(f'docs/README.md has orphaned Markdown files: {missing}')
print(f'Documentation index checks passed: {len(docs)} docs files indexed.')
PY

python3 - <<'PY'
from pathlib import Path
import re

failures = []
for path in sorted(Path('.').rglob('*.md')):
    if '.git' in path.parts:
        continue
    in_fence = False
    headings = []
    for line_number, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if line.startswith('```'):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        match = re.match(r'^(#{1,6})\s+(.+?)\s*$', line)
        if match:
            headings.append((line_number, len(match.group(1)), match.group(2)))
    if not headings:
        failures.append(f'{path}: no headings')
        continue
    if sum(level == 1 for _, level, _ in headings) != 1:
        failures.append(f'{path}: expected exactly one H1')
    previous = headings[0][1]
    if previous != 1:
        failures.append(f'{path}:{headings[0][0]}: first heading must be H1')
    for line_number, level, title in headings[1:]:
        if not title.strip():
            failures.append(f'{path}:{line_number}: empty heading')
        if level > previous + 1:
            failures.append(f'{path}:{line_number}: heading skips H{previous} to H{level}')
        previous = level
if failures:
    raise SystemExit('\n'.join(failures))
print('Markdown heading hierarchy checks passed for all Markdown files.')
PY

python3 - <<'PY'
from pathlib import Path
import re

root = Path('cloud-networking-interview')
expected = {
    '00-README.md', '17-references.md',
    '01-cloud-network-foundations.md', '02-virtual-network-boundaries-and-design.md',
    '03-subnet-and-ip-address-planning.md', '04-routes-gateways-and-hybrid-connectivity.md',
    '05-internet-ingress-nat-and-egress.md', '06-firewalls-security-groups-and-network-acls.md',
    '07-private-connectivity-and-service-publishing.md', '08-dns-and-service-discovery.md',
    '09-load-balancing-and-traffic-entry.md', '10-iam-and-workload-identity.md',
    '11-containers-kubernetes-and-network-policy.md', '12-observability-troubleshooting-and-slos.md',
    '13-quotas-capacity-and-network-cost.md', '14-multi-region-disaster-recovery-and-failover.md',
    '15-cloud-network-migration-and-modernization.md', '16-cloud-interview-synthesis-and-mock-loops.md',
}
actual = {p.name for p in root.glob('*.md')}
if actual != expected:
    raise SystemExit(f'Cloud track file set mismatch; missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
index = (root / '00-README.md').read_text(encoding='utf-8')
ordered = re.findall(r'\]\(([^)]+\.md)\)', index)
topic_order = [name for name in ordered if not name.startswith('../')]
expected_topics = [
    '01-cloud-network-foundations.md', '02-virtual-network-boundaries-and-design.md',
    '03-subnet-and-ip-address-planning.md', '04-routes-gateways-and-hybrid-connectivity.md',
    '05-internet-ingress-nat-and-egress.md', '06-firewalls-security-groups-and-network-acls.md',
    '07-private-connectivity-and-service-publishing.md', '08-dns-and-service-discovery.md',
    '09-load-balancing-and-traffic-entry.md', '10-iam-and-workload-identity.md',
    '11-containers-kubernetes-and-network-policy.md', '12-observability-troubleshooting-and-slos.md',
    '13-quotas-capacity-and-network-cost.md', '14-multi-region-disaster-recovery-and-failover.md',
    '15-cloud-network-migration-and-modernization.md', '16-cloud-interview-synthesis-and-mock-loops.md',
]
if topic_order[:len(expected_topics)] != expected_topics:
    raise SystemExit('Cloud track README must list every topic in its ordered learning path')
for path in sorted(root.glob('*.md')):
    if path.name in {'00-README.md', '17-references.md'}:
        continue
    text = path.read_text(encoding='utf-8')
    for marker in ('Learning objectives', 'Prerequisites', 'AWS and GCP', 'References'):
        if marker.lower() not in text.lower():
            raise SystemExit(f'{path}: missing required curriculum marker {marker!r}')
    for marker in ('AWS setup and use', 'GCP setup and use'):
        if marker.lower() not in text.lower():
            raise SystemExit(f'{path}: missing provider walkthrough section {marker!r}')
    if path.name == '16-cloud-interview-synthesis-and-mock-loops.md':
        for marker in ('Mock loop', 'Self-scoring'):
            if marker.lower() not in text.lower():
                raise SystemExit(f'{path}: missing synthesis marker {marker!r}')
    else:
        for marker in ('Worked', 'exercise'):
            if marker.lower() not in text.lower():
                raise SystemExit(f'{path}: missing required curriculum marker {marker!r}')
    prose = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    words = re.findall(r"\b[\w'-]+\b", prose)
    if len(words) < 850:
        raise SystemExit(f'{path}: needs at least 850 words; found {len(words)}')
    if len(re.findall(r'^\s*(?:\d+\.\s+\*\*|###\s+(?:[A-Z]\.)?\d+(?:\.|\s))', text, flags=re.MULTILINE)) < 6:
        raise SystemExit(f'{path}: needs at least 6 numbered interview Q&A entries')
    if text.count('```mermaid') < 2:
        raise SystemExit(f'{path}: needs two Mermaid diagrams')
    if not re.search(r'^\|\s*:?-{3,}:?\s*\|', text, flags=re.MULTILINE):
        raise SystemExit(f'{path}: needs a Markdown evidence/comparison table')
    for block in re.findall(r'```mermaid\n(.*?)```', text, flags=re.DOTALL):
        if not block.isascii():
            raise SystemExit(f'{path}: Mermaid diagram contains non-ASCII characters')
print(f'Cloud networking interview track checks passed: {len(expected)-2} topics, exact index, depth, exercises, Q&A, tables, and diagrams.')
PY

python3 - <<'PY'
from pathlib import Path
import re

root = Path('terraform-interview')
expected = {
    '00-README.md', '13-references.md',
    '01-terraform-core-and-execution-model.md', '02-providers-versions-and-authentication.md',
    '03-state-backends-locking-and-workspaces.md', '04-resources-data-modules-and-composition.md',
    '05-plan-apply-lifecycle-and-safe-change.md', '06-import-moved-blocks-and-drift-recovery.md',
    '07-aws-networking-with-terraform.md', '08-gcp-networking-with-terraform.md',
    '09-f5-big-ip-provider-and-as3-boundaries.md', '10-multi-provider-platform-patterns.md',
    '11-testing-policy-cicd-and-security.md', '12-debugging-rollback-cost-and-interview-loops.md',
    '14-real-world-terraform-exercises.md', '15-real-world-exercise-answer-key.md',
    '16-a10-load-balancers-and-terraform.md', '17-cisco-networking-and-terraform.md',
    '18-spine-leaf-switching-and-fabric-as-code.md', '19-cisco-nso-service-models-and-terraform.md',
}
actual = {p.name for p in root.glob('*.md')}
if actual != expected:
    raise SystemExit(f'Terraform track file set mismatch; missing={sorted(expected-actual)}, extra={sorted(actual-expected)}')
index = (root / '00-README.md').read_text(encoding='utf-8')
ordered = re.findall(r'\]\(([^)]+\.md)\)', index)
expected_modules = [f'{i:02d}-' for i in range(1, 13)]
listed = [Path(name).name for name in ordered if not name.startswith('../')]
if len(listed) < 14 or any(not listed[i].startswith(expected_modules[i]) for i in range(12)):
    raise SystemExit('Terraform README must list all 12 modules in order')
if not listed[12].startswith('14-real-world-') or not listed[13].startswith('15-real-world-'):
    raise SystemExit('Terraform README must list the real-world exercise pack after the modules')
if not listed[14].startswith('16-a10-') or not listed[15].startswith('17-cisco-'):
    raise SystemExit('Terraform README must list A10 and Cisco modules after the exercises')
if not listed[16].startswith('18-spine-') or not listed[17].startswith('19-cisco-nso-'):
    raise SystemExit('Terraform README must list spine-leaf and NSO modules after Cisco')
for path in sorted(root.glob('*.md')):
    if path.name in {'00-README.md', '13-references.md'}:
        continue
    text = path.read_text(encoding='utf-8')
    if path.name in {'14-real-world-terraform-exercises.md', '15-real-world-exercise-answer-key.md'}:
        for marker in ('AWS', 'GCP', 'F5', 'Terraform', 'exercise', 'answer', 'rollback'):
            if marker.lower() not in text.lower():
                raise SystemExit(f'{path}: missing real-world practice marker {marker!r}')
        prose = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        if len(re.findall(r"\b[\w'-]+\b", prose)) < 2200:
            raise SystemExit(f'{path}: needs at least 2200 prose words')
        if text.count('```mermaid') < 4:
            raise SystemExit(f'{path}: needs at least four architecture diagrams')
        if not re.search(r'^\|\s*:?-{3,}:?\s*\|', text, flags=re.MULTILINE):
            raise SystemExit(f'{path}: needs a Markdown exercise/evidence table')
        continue
    if path.name in {'16-a10-load-balancers-and-terraform.md', '17-cisco-networking-and-terraform.md', '18-spine-leaf-switching-and-fabric-as-code.md', '19-cisco-nso-service-models-and-terraform.md'}:
        for marker in ('AWS', 'GCP', 'Terraform', 'exercise', 'answer', 'rollback'):
            if marker.lower() not in text.lower():
                raise SystemExit(f'{path}: missing platform-module marker {marker!r}')
        if path.name.startswith('16-') and 'A10' not in text:
            raise SystemExit(f'{path}: missing A10 coverage')
        if path.name.startswith(('17-', '18-', '19-')) and 'Cisco' not in text:
            raise SystemExit(f'{path}: missing Cisco coverage')
        prose = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
        if len(re.findall(r"\b[\w'-]+\b", prose)) < 1500:
            raise SystemExit(f'{path}: needs at least 1500 prose words')
        if text.count('```mermaid') < 2:
            raise SystemExit(f'{path}: needs at least two architecture diagrams')
        if not re.search(r'^\|\s*:?-{3,}:?\s*\|', text, flags=re.MULTILINE):
            raise SystemExit(f'{path}: needs a Markdown evidence table')
        continue
    for marker in ('Learning objectives', 'Prerequisites', 'AWS', 'GCP', 'F5', 'Terraform', 'Exercises', 'References'):
        if marker.lower() not in text.lower():
            raise SystemExit(f'{path}: missing required marker {marker!r}')
    prose = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    if len(re.findall(r"\b[\w'-]+\b", prose)) < 1100:
        raise SystemExit(f'{path}: needs at least 1100 prose words')
    if text.count('```mermaid') < 2 or '```hcl' not in text:
        raise SystemExit(f'{path}: needs two Mermaid diagrams and Terraform HCL')
    if not re.search(r'^\|\s*:?-{3,}:?\s*\|', text, flags=re.MULTILINE):
        raise SystemExit(f'{path}: needs an evidence/comparison table')
    if len(re.findall(r'^\s*(?:\d+\.\s+\*\*|###\s+(?:[A-Z]\.)?\d+(?:\.|\s))', text, flags=re.MULTILINE)) < 6:
        raise SystemExit(f'{path}: needs at least six interview Q&A entries')
    for block in re.findall(r'```mermaid\n(.*?)```', text, flags=re.DOTALL):
        if not block.isascii():
            raise SystemExit(f'{path}: Mermaid diagram contains non-ASCII characters')
print('Terraform interview track checks passed: exact 20-file set, ordered index, provider examples, HCL, diagrams, exercises, and Q&A.')
PY
