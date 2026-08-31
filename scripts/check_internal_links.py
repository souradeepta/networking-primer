#!/usr/bin/env python3
"""Fail when Markdown links to repository-local files are broken."""

from pathlib import Path
import re
import sys


LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")


def is_local(target: str) -> bool:
    """Return whether a target names a relative Markdown file path."""
    return not (target.startswith(("http://", "https://", "#", "mailto:")) or ":" in target)


def main() -> None:
    """Check local Markdown destinations relative to their source file."""
    failures: list[str] = []
    for source in [Path("README.md"), *Path("docs").glob("*.md"), *Path("book").glob("*.md")]:
        for target in LINK.findall(source.read_text(encoding="utf-8")):
            target = target.split("#", maxsplit=1)[0].strip("<>")
            if target and is_local(target) and not (source.parent / target).is_file():
                failures.append(f"{source}: broken local link: {target}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print("Internal Markdown link checks passed.")


if __name__ == "__main__":
    main()
