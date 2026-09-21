#!/usr/bin/env python3
"""
Szlak docs build check.

Validates the documentation without installing anything:

  1. every internal link resolves
  2. every `<!-- include: path -->` target exists
  3. the house writing conventions that can be checked mechanically

Exit code 0 means the docs are publishable.
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"

LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)\s]*)?\)")
INCLUDE = re.compile(r"<!--\s*include:\s*(\S+?)\s*-->")
IMAGE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
FENCE = re.compile(r"^```(\w*)", re.MULTILINE)

BANNED_WORDS = {
    "simply": "if it were simple they would not be reading the docs",
    "just ": "if it were simple they would not be reading the docs",
    "easily": "if it were simple they would not be reading the docs",
    "journey": "it is a trip, never a journey",
    "voyage": "it is a trip, never a voyage",
    "adventure": "it is a trip, never an adventure",
}

# Polish place names that must keep their diacritics.
DIACRITICS = {
    "Krakow": "Kraków",
    "Gdansk": "Gdańsk",
    "Lodz": "Łódź",
    "Wroclaw": "Wrocław",
    "Poznan": "Poznań",
    "Bialowieza": "Białowieża",
    "Swinoujscie": "Świnoujście",
    "Chocholowska": "Chochołowska",
    "Sniezka": "Śnieżka",
    "Wladyslawowo": "Władysławowo",
    "zloty": "złoty",
    "Zakopane ": "Zakopane ",  # no diacritics, kept for symmetry
}

PARAM_HEADER = "| Name | Type | Required | Default | Description |"

problems = []
warnings = []


def report(path, line, message, warn=False):
    location = f"{path.relative_to(ROOT)}:{line}" if line else str(path.relative_to(ROOT))
    entry = f"  {location}\n      {message}"
    (warnings if warn else problems).append(entry)


def check_page(path):
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    # 1. internal links
    for match in LINK.finditer(text):
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        resolved = (path.parent / target).resolve()
        if not resolved.exists():
            line = text[: match.start()].count("\n") + 1
            report(path, line, f"broken link: {target}")

    # 2. images
    for match in IMAGE.finditer(text):
        target = match.group(1)
        if target.startswith(("http://", "https://")):
            continue
        if not (path.parent / target).resolve().exists():
            line = text[: match.start()].count("\n") + 1
            report(path, line, f"missing image: {target}")

    # 3. includes
    for match in INCLUDE.finditer(text):
        target = ROOT / match.group(1)
        line = text[: match.start()].count("\n") + 1
        if not target.exists():
            report(path, line, f"include target missing: {match.group(1)}")

    # 4. style rule 5 - no pasted code samples
    for match in FENCE.finditer(text):
        language = match.group(1)
        if language in {"python", "py", "javascript", "js"}:
            line = text[: match.start()].count("\n") + 1
            report(path, line,
                   f"pasted {language} block. Code samples belong in samples/ "
                   f"and are included by reference with <!-- include: -->",
                   warn=True)

    # 5. banned words
    for index, line_text in enumerate(lines, start=1):
        lowered = line_text.lower()
        for word, rule in BANNED_WORDS.items():
            if word in lowered:
                report(path, index, f"avoid {word.strip()!r} - {rule}")

    # 6. diacritics
    for index, line_text in enumerate(lines, start=1):
        for bare, correct in DIACRITICS.items():
            if bare != correct and re.search(rf"\b{bare}\b", line_text):
                report(path, index,
                       f"Polish place names keep their diacritics: "
                       f"write {correct!r}, not {bare!r}")

    # 7. parameter table shape
    if "## Parameters" in text:
        section = text.split("## Parameters", 1)[1]
        if "|" in section.split("##")[0]:
            header = next((l.strip() for l in section.splitlines()
                           if l.strip().startswith("|")), "")
            if header and header != PARAM_HEADER:
                line = text[: text.index("## Parameters")].count("\n") + 1
                report(path, line,
                       f"parameter tables must use these columns in this order:\n"
                       f"      {PARAM_HEADER}")


def main():
    pages = sorted(DOCS.rglob("*.md"))
    if not pages:
        print("No pages found under docs/")
        return 1

    for page in pages:
        check_page(page)

    print(f"Checked {len(pages)} pages")

    if warnings:
        print(f"\n{len(warnings)} warning(s):\n")
        print("\n".join(warnings))

    if problems:
        print(f"\n{len(problems)} problem(s):\n")
        print("\n".join(problems))
        print("\nBuild FAILED")
        return 1

    print("Build OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
