#!/usr/bin/env bash
# Validate repository structure and diagram portability without external tools.
set -euo pipefail

required=(
  README.md SPEC.md AGENTS.md MEMORY.md TODO.md
  docs/01-foundations.md docs/02-request-path.md docs/03-f5-ltm.md
  docs/04-f5-gtm.md docs/05-troubleshooting.md docs/06-ddi.md
  docs/07-automation.md docs/08-transport-security.md docs/architecture.md
  docs/interview-questions.md docs/glossary.md docs/references.md
  examples/request_path.py examples/f5_pool_audit.py
)

for path in "${required[@]}"; do
  [[ -f "$path" ]] || { echo "Missing required file: $path" >&2; exit 1; }
done

python3 - <<'PY'
from pathlib import Path
import re

for path in Path("docs").glob("*.md"):
    text = path.read_text(encoding="utf-8")
    for block in re.findall(r"```mermaid\n(.*?)```", text, re.DOTALL):
        if not block.isascii():
            raise SystemExit(f"Non-ASCII Mermaid content in {path}")
print("Repository structure and Mermaid ASCII checks passed.")
PY
