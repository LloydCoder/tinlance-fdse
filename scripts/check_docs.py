"""Validate local Markdown links used by repository documentation."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"(?<!!)\[[^\]]+\]\(([^)#]+)(?:#[^)]+)?\)")


def main() -> int:
    failures: list[str] = []

    excluded_parts = {
        ".git",
        ".venv",
        "dist",
        "build",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        "node_modules",
    }

    for document in ROOT.rglob("*.md"):
        if any(part in excluded_parts for part in document.parts):
            continue
        text = document.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            if "://" in target or target.startswith("mailto:"):
                continue
            resolved = (document.parent / target).resolve()
            try:
                resolved.relative_to(ROOT.resolve())
            except ValueError:
                failures.append(f"{document}: link escapes repository: {target}")
                continue
            if not resolved.exists():
                failures.append(f"{document}: missing local link target: {target}")

    if failures:
        print("\n".join(failures))
        return 1

    print("documentation links: OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
