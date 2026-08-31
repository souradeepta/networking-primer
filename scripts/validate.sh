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

chapters = sorted(p for p in Path("book").glob("*.md") if p.name not in {"README.md", "FACT-INFERENCE-LEDGER.md"})
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
