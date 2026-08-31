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
)

for path in "${required[@]}"; do
  [[ -f "$path" ]] || { echo "Missing required file: $path" >&2; exit 1; }
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

for path in [*Path("docs").glob("*.md"), *Path("book").glob("*.md")]:
    text = path.read_text(encoding="utf-8")
    for block in re.findall(r"```mermaid\n(.*?)```", text, re.DOTALL):
        if not block.isascii():
            raise SystemExit(f"Non-ASCII Mermaid content in {path}")
print("Repository structure and Mermaid ASCII checks passed.")
PY

python3 scripts/check_internal_links.py
