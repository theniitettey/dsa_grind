#!/usr/bin/env python3
"""
author: Michael Perry Tettey
repo: dsa-grind

purpose:
- automatically update the stats table in README.md
- count solved problems by platform based on filenames
- update the "last updated" timestamp

notes:
- filenames must follow: PlatformName_Question_Title.ext
- platforms tracked:
  GeeksForGeeks, LeetCode, HackerRank, Codeforces
- this script is intentionally simple and opinionated
"""

from __future__ import annotations

import re
from collections import Counter
from datetime import datetime
from pathlib import Path

# --------------------------------------------------
# Paths
# --------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"

# --------------------------------------------------
# Platform configuration
# --------------------------------------------------

# Platform keys must match filename prefixes exactly
PLATFORM_MAP = {
    "GeeksForGeeks": "geeksforgeeks",
    "LeetCode": "leetcode",
    "HackerRank": "hackerrank",
    "Codeforces": "codeforces",
}

# Allowed file extensions (future-proofing)
ALLOWED_EXTS = ("py", "js", "ts", "cpp", "java", "go", "rs")

# File pattern: PlatformName_Anything.ext
FILE_RE = re.compile(
    rf"^(?P<platform>{'|'.join(map(re.escape, PLATFORM_MAP.keys()))})_.+\.({'|'.join(ALLOWED_EXTS)})$"
)

# Replace everything inside:
#   ## current stats
#   ...
#   ---
STATS_SECTION_RE = re.compile(
    r"(?is)(^##\s+current\s+stats.*?\n)(.*?)(\n---\n)",
    re.MULTILINE,
)

# --------------------------------------------------
# Core logic
# --------------------------------------------------

def scan_counts() -> Counter[str]:
    counts: Counter[str] = Counter()

    for p in REPO_ROOT.rglob("*"):
        if not p.is_file():
            continue

        # ignore hidden dirs/files (.git, .venv, etc.)
        if any(part.startswith(".") for part in p.parts):
            continue

        # ignore common junk
        if "node_modules" in p.parts or ".venv" in p.parts or "__pycache__" in p.parts:
            continue

        m = FILE_RE.match(p.name)
        if not m:
            continue

        plat_key = m.group("platform")
        counts[PLATFORM_MAP[plat_key]] += 1

    # ensure all platforms exist in output
    for v in PLATFORM_MAP.values():
        counts.setdefault(v, 0)

    return counts


def vibe_for(platform: str, solved: int) -> str:
    """
    yes, this is subjective.
    no, i’m not changing it.
    """
    if platform == "leetcode":
        return "scared" if solved == 0 else "we move"
    if platform == "codeforces":
        return "lol" if solved == 0 else "pain"
    if platform == "hackerrank":
        return "tbd" if solved == 0 else "steady"
    if platform == "geeksforgeeks":
        return "warming up" if solved < 10 else "cooking"
    return "vibes"


def build_table(counts: Counter[str]) -> str:
    order = ["geeksforgeeks", "leetcode", "hackerrank", "codeforces"]

    lines = []
    lines.append("| platform      | solved | vibe check |")
    lines.append("| ------------- | ------ | ---------- |")

    for plat in order:
        solved = counts[plat]
        vibe = vibe_for(plat, solved)
        lines.append(f"| {plat:<12} | {solved:<6} | {vibe:<10} |")

    updated = datetime.now().strftime("%Y-%m-%d")
    lines.append("")
    lines.append(f"_last updated: {updated}_")

    return "\n".join(lines)

# --------------------------------------------------
# Entry point
# --------------------------------------------------

def main() -> None:
    if not README.exists():
        raise SystemExit("README.md not found at repo root.")

    counts = scan_counts()
    table = build_table(counts)

    text = README.read_text(encoding="utf-8")
    m = STATS_SECTION_RE.search(text)
    if not m:
        raise SystemExit(
            "Couldn't find the '## current stats' section in README.md.\n"
            "Make sure it starts with '## current stats' and ends before a '---' divider."
        )

    new_text = text[: m.start(2)] + table + text[m.end(2) :]
    README.write_text(new_text, encoding="utf-8")

    print("✅ Updated README stats:", dict(counts))


if __name__ == "__main__":
    main()
