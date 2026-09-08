#!/usr/bin/env python3
"""Report answer-quality issues without turning existing prose into a hard gate."""

from collections import defaultdict
from pathlib import Path
import re


QUESTION = re.compile(r"^\s*(?:\d+\.\s+\*\*.*?\*\*|###\s+\d+\..*)", re.MULTILINE)
WORDS = re.compile(r"\b[\w'-]+\b")


def answer_entries(path: Path):
    text = path.read_text(encoding="utf-8")
    heading = re.search(r"^## Questions and answers\s*$", text, re.MULTILINE)
    if not heading:
        return []
    section = re.split(
        r"^## (?!Questions and answers)", text[heading.end() :], maxsplit=1, flags=re.MULTILINE
    )[0]
    matches = list(QUESTION.finditer(section))
    entries = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(section)
        body = section[match.end() : end].strip()
        direct, separator, reasoning = body.partition("Interview reasoning:")
        answer_marker = re.search(r"(?:\*\*)?Answer:(?:\*\*)?", direct)
        has_answer_marker = answer_marker is not None
        if answer_marker:
            direct = direct[: answer_marker.start()] + direct[answer_marker.end() :]
        direct = direct.strip()
        entries.append((direct, bool(separator or has_answer_marker), reasoning.strip()))
    return entries


def normalized_paragraph(value: str) -> str:
    value = re.sub(r"[`*_>\[\]()]", " ", value.lower())
    return " ".join(value.split())


def main() -> None:
    paths = [
        *sorted(Path("book").glob("*.md")),
        *sorted(Path("book/topics").glob("*.md")),
        *sorted(Path("book/case-studies").glob("*.md")),
    ]
    paths = [p for p in paths if p.name not in {"README.md", "FACT-INFERENCE-LEDGER.md"}]
    short_answers = []
    missing_boundaries = []
    duplicates = defaultdict(list)
    answer_count = 0

    for path in paths:
        for number, (direct, has_boundary, reasoning) in enumerate(answer_entries(path), 1):
            answer_count += 1
            if not has_boundary:
                missing_boundaries.append(f"{path}:{number}")
            if len(WORDS.findall(direct)) < 12:
                short_answers.append(f"{path}:{number} ({len(WORDS.findall(direct))} words)")
            # A duplicate direct answer is useful to review, but short definitions
            # and intentional shared wording should not become a hard failure.
            key = normalized_paragraph(direct)
            if len(key.split()) >= 18:
                duplicates[key].append(f"{path}:{number}")

    repeated = [locations for locations in duplicates.values() if len(locations) > 1]
    print(f"Answer boundary checks inspected {answer_count} answers.")
    if missing_boundaries:
        print(f"WARNING: {len(missing_boundaries)} answers lack an explicit 'Answer:' or 'Interview reasoning:' boundary.")
        print("  " + ", ".join(missing_boundaries[:8]))
    if short_answers:
        print(f"WARNING: {len(short_answers)} direct answers contain fewer than 12 words.")
        print("  " + ", ".join(short_answers[:8]))
    if repeated:
        print(f"WARNING: {len(repeated)} normalized direct-answer groups are repeated.")
        for locations in repeated[:8]:
            print("  " + ", ".join(locations))
    if not (missing_boundaries or short_answers or repeated):
        print("No answer-boundary, direct-depth, or duplicate warnings found.")


if __name__ == "__main__":
    main()
