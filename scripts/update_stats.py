#!/usr/bin/env python3
from __future__ import annotations

import re
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"

# Your platform keys (match your file prefix exactly)
PLATFORM_MAP = {
    "GeeksForGeeks": "geeksforgeeks",
    "LeetCode": "leetcode",
    "HackerRank": "hackerrank",
    "Codeforces": "codeforces",
}

# File pattern: PlatformName_Anything.py (or .js/.ts if you later add)
FILE_RE = re.compile(r"^(?P<platform>[A-Za-z]+)_.+\.(py|js|ts|cpp|java|go|rs)$")

STATS_SECTION_RE = re.compile(
    r"(?s)(## current stats .*?\n)(.*?)(\n---\n)",
)

def scan_counts() -> Counter[str]:
    counts: Counter[str] = Counter()
    for p in REPO_ROOT.rglob("*"):
        if not p.is_file():
            continue
        if any(part.startswith(".") for part in p.parts):
            continue
        if "node_modules" in p.parts or ".venv" in p.parts or "__pycache__" in p.parts:
            continue

        m = FILE_RE.match(p.name)
        if not m:
            continue

        plat_key = m.group("platform")
        if plat_key in PLATFORM_MAP:
            counts[PLATFORM_MAP[plat_key]] += 1

    # Ensure all platforms exist in output
    for v in PLATFORM_MAP.values():
        counts.setdefault(v, 0)
    return counts

def vibe_for(platform: str, solved: int) -> str:
    # Keep your humor; tweak however you like
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
        # pad platform names to match your style
        display = plat
        lines.append(f"| {display:<12} | {solved:<6} | {vibe:<10} |")

    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines.append("")
    lines.append(f"_last updated: {updated}_")
    return "\n".join(lines)

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
            "Make sure it contains a '## current stats' heading and ends before a '---' line."
        )

    new_text = text[: m.start(2)] + table + text[m.end(2) :]
    README.write_text(new_text, encoding="utf-8")
    print("✅ Updated README stats:", dict(counts))

if __name__ == "__main__":
    main()
