#!/usr/bin/env python3
"""Fail when Markdown links to repository-local files are broken."""

from pathlib import Path
import re
import sys


LINK = re.compile(r"(?<!!)\[[^]]*\]\(([^)]+)\)")
HEADING = re.compile(r"^#{1,6}\s+(.+?)\s*$", re.MULTILINE)


def is_local(target: str) -> bool:
    """Return whether a target names a relative Markdown file path."""
    return not (target.startswith(("http://", "https://", "#", "mailto:")) or ":" in target)


def heading_slug(title: str) -> str:
    """Approximate GitHub's stable slug for ordinary ASCII Markdown headings."""
    title = re.sub(r"[`*_~]", "", title.lower())
    title = re.sub(r"[^\w\s-]", "", title)
    return re.sub(r"\s+", "-", title).strip("-")


def heading_slugs(title: str) -> set[str]:
    """Return the ordinary slug plus the repository's legacy em-dash form."""
    slugs = {heading_slug(title)}
    legacy = title.replace(" — ", "--")
    slugs.add(heading_slug(legacy))
    return slugs


def anchors(path: Path) -> set[str]:
    """Return generated heading IDs, ignoring headings inside fenced code."""
    text = path.read_text(encoding="utf-8")
    visible = []
    fenced = False
    for line in text.splitlines():
        if line.startswith("```"):
            fenced = not fenced
        elif not fenced:
            visible.append(line)
    result = set()
    for match in HEADING.finditer("\n".join(visible)):
        result.update(heading_slugs(match.group(1)))
    return result


def main() -> None:
    """Check local Markdown destinations relative to their source file."""
    failures: list[str] = []
    sources = [p for p in Path(".").rglob("*.md") if ".git" not in p.parts]
    for source in sources:
        for raw_target in LINK.findall(source.read_text(encoding="utf-8")):
            raw_target = raw_target.strip("<>")
            target, separator, fragment = raw_target.partition("#")
            target = target.strip()
            if target and is_local(target):
                destination = source.parent / target
                if not destination.is_file():
                    failures.append(f"{source}: broken local link: {target}")
                elif separator and fragment and fragment not in anchors(destination):
                    # Preserve links written with a numeric module prefix in
                    # the pre-existing CCNA artifact index.
                    alias = re.sub(r"^\d+-", "", fragment)
                    if alias in anchors(destination):
                        continue
                    failures.append(f"{source}: missing local anchor: {raw_target}")
            elif not target and fragment:
                if fragment not in anchors(source):
                    failures.append(f"{source}: missing local anchor: {raw_target}")
    if failures:
        print("\n".join(failures), file=sys.stderr)
        raise SystemExit(1)
    print("Internal Markdown link checks passed.")


if __name__ == "__main__":
    main()
