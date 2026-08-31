#!/usr/bin/env bash
# Validate repository structure and diagram portability without external tools.
set -euo pipefail

required=(
  README.md SPEC.md AGENTS.md MEMORY.md TODO.md
  docs/01-foundations.md docs/02-request-path.md docs/03-f5-ltm.md
  docs/04-f5-gtm.md docs/05-troubleshooting.md docs/06-ddi.md
  docs/07-automation.md docs/08-transport-security.md docs/architecture.md
  docs/09-hands-on-labs.md docs/interview-questions.md docs/f5-interview-bank.md docs/glossary.md docs/references.md
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
if len(topics) < 33:
    raise SystemExit(f"Need 33 focused topic files; found {len(topics)}")
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
            required_words = 16 if path.name.startswith(("22-", "23-", "24-", "25-", "26-", "27-", "28-", "29-", "30-", "31-", "32-", "33-")) else minimum
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
exercises = re.findall(r"^\d+\.\s+\*\*", text.split("## Debugging exercises", 1)[-1], flags=re.MULTILINE)
if len(questions) < 30:
    raise SystemExit(f"F5 interview bank needs 30 questions; found {len(questions)}")
if len(exercises) < 8:
    raise SystemExit(f"F5 interview bank needs 8 debugging exercises; found {len(exercises)}")
print(f"F5 interview bank checks passed: {len(questions)} questions, {len(exercises)} debugging exercises.")
PY

python3 scripts/check_internal_links.py
