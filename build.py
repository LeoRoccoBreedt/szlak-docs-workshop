#!/usr/bin/env python3
"""
Szlak docs build.

Builds the documentation without installing anything, and fails on the things
that would ship a broken page:

  1. every internal link resolves
  2. every image exists
  3. every `<!-- include: path -->` target exists

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

problems = []


def report(path, line, message):
    problems.append(f"  {path.relative_to(ROOT)}:{line}\n      {message}")


def check_page(path):
    text = path.read_text(encoding="utf-8")

    for match in LINK.finditer(text):
        target = match.group(1)
        if target.startswith(("http://", "https://", "mailto:")):
            continue
        if not (path.parent / target).resolve().exists():
            report(path, text[: match.start()].count("\n") + 1,
                   f"broken link: {target}")

    for match in IMAGE.finditer(text):
        target = match.group(1)
        if target.startswith(("http://", "https://")):
            continue
        if not (path.parent / target).resolve().exists():
            report(path, text[: match.start()].count("\n") + 1,
                   f"missing image: {target}")

    for match in INCLUDE.finditer(text):
        if not (ROOT / match.group(1)).exists():
            report(path, text[: match.start()].count("\n") + 1,
                   f"include target missing: {match.group(1)}")


def main():
    pages = sorted(DOCS.rglob("*.md"))
    if not pages:
        print("No pages found under docs/")
        return 1

    for page in pages:
        check_page(page)

    print(f"Built {len(pages)} pages")
    if problems:
        print(f"\n{len(problems)} problem(s):\n")
        print("\n".join(problems))
        print("\nBuild FAILED")
        return 1

    print("Build OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
