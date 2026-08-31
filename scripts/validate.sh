#!/usr/bin/env bash
# Validate repository structure and diagram portability without external tools.
set -euo pipefail

required=(
  README.md SPEC.md AGENTS.md MEMORY.md TODO.md
  docs/01-foundations.md docs/02-request-path.md docs/03-f5-ltm.md
  docs/04-f5-gtm.md docs/05-troubleshooting.md docs/06-ddi.md
  docs/07-automation.md docs/08-transport-security.md docs/architecture.md
  docs/09-hands-on-labs.md docs/interview-questions.md docs/glossary.md docs/references.md
  book/README.md book/FACT-INFERENCE-LEDGER.md
  examples/request_path.py examples/f5_pool_audit.py
  scripts/check_internal_links.py
  demos/README.md demos/dns_observe.sh demos/tls_inspect.sh
  demos/vip_ltm_model.py demos/certificate_audit.py
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
if len(chapters) < 14:
    raise SystemExit(f"Book edition needs 14 chapters; found {len(chapters)}")
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
    if len(words) < 1200:
        raise SystemExit(f"{path}: needs 1200 prose words; found {len(words)}")
    qa = re.findall(r"^\s*\d+\.\s+\*\*", text, flags=re.MULTILINE)
    if len(qa) < 8:
        raise SystemExit(f"{path}: needs 8 numbered Q&A; found {len(qa)}")
    if "```mermaid" not in text:
        raise SystemExit(f"{path}: missing Mermaid diagram")
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
if len(topics) < 10:
    raise SystemExit(f"Need 10 focused topic files; found {len(topics)}")
for path in topics:
    text = path.read_text(encoding="utf-8")
    required = ["Learning objectives", "Worked example", "When this breaks",
                "Operational checklist", "Questions and answers"]
    missing = [h for h in required if f"## {h}" not in text]
    if missing:
        raise SystemExit(f"{path}: missing topic headings: {', '.join(missing)}")
    if len(re.findall(r"\b[\w'-]+\b", re.sub(r"```.*?```", "", text, flags=re.DOTALL))) < 900:
        raise SystemExit(f"{path}: needs 900 words")
    if len(re.findall(r"^\s*\d+\.\s+\*\*", text, flags=re.MULTILINE)) < 5:
        raise SystemExit(f"{path}: needs 5 numbered Q&A")
    if "```mermaid" not in text or "| --- |" not in text:
        raise SystemExit(f"{path}: needs Mermaid diagram and Markdown table")
print(f"Focused topic checks passed: {len(topics)} topics.")
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

python3 scripts/check_internal_links.py
