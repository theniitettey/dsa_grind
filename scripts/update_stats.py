#!/usr/bin/env python3
"""
author: Michael Perry Tettey
repo: dsa-grind

purpose:
- automatically update the stats table in README.md
- parse metadata from solution files (time_spent, difficulty, etc.)
- calculate streaks and total time spent
- generate a cool dashboard-like README
- use grind.json for configuration and optimization
"""

from __future__ import annotations

import re
import json
import math
from collections import Counter, defaultdict
from datetime import datetime, timedelta, date
from pathlib import Path
from typing import NamedTuple, Optional, List, Dict

# --------------------------------------------------
# Paths
# --------------------------------------------------

REPO_ROOT = Path(__file__).resolve().parents[1]
README = REPO_ROOT / "README.md"
CONFIG_FILE = REPO_ROOT / "config" / "grind.json"

# --------------------------------------------------
# Config Management
# --------------------------------------------------

def load_config() -> dict:
    """Load configuration from grind.json"""
    if not CONFIG_FILE.exists():
        # Create default config
        default_config = {
            "user": {
                "name": "",
                "github_username": ""
            },
            "readme": {
                "title": "dsa grind 💪",
                "show_badges": True,
                "show_stats_table": True,
                "show_topics": True,
                "show_streak": True,
                "platforms": ["GeeksForGeeks", "LeetCode", "HackerRank", "Codeforces"],
                "badge_style": "for-the-badge",
                "topic_filters": {
                    "exclude": ["?", "misc"],
                    "min_count": 1
                }
            },
            "optimization": {
                "last_update": None,
                "total_files_scanned": 0,
                "cache": {
                    "total_solved": 0,
                    "total_time_mins": 0,
                    "current_streak": 0,
                    "topics": {}
                }
            },
            "stats": {
                "total_solved": 0,
                "platforms": {},
                "last_scan_timestamp": None
            }
        }
        save_config(default_config)
        return default_config
    
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_config(config: dict) -> None:
    """Save configuration to grind.json"""
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

# --------------------------------------------------
# Constants & Config
# --------------------------------------------------

PLATFORM_MAP = {
    "GeeksForGeeks": "geeksforgeeks",
    "LeetCode": "leetcode",
    "HackerRank": "hackerrank",
    "Codeforces": "codeforces",
}

ALLOWED_EXTS = ("py", "js", "ts", "cpp", "java", "go", "rs")

# File pattern: PlatformName_Anything.ext
FILE_RE = re.compile(
    rf"^(?P<platform>{'|'.join(map(re.escape, PLATFORM_MAP.keys()))})_.+\.({'|'.join(ALLOWED_EXTS)})$"
)

# --------------------------------------------------
# Data Structures
# --------------------------------------------------

class Problem(NamedTuple):
    filename: str
    platform: str
    difficulty: str
    time_spent_str: str
    time_spent_mins: int
    created: Optional[date]
    tries: int
    topic: str
    url: str

# --------------------------------------------------
# Parsing Logic
# --------------------------------------------------

def parse_time(time_str: str) -> int:
    """
    Parses time strings like "10 mins", "1h 30m", "2 hours" into minutes.
    Returns 0 if parsing fails or input is ?
    """
    if not time_str or "?" in time_str:
        return 0
    
    time_str = time_str.lower().strip()
    total_mins = 0
    
    # Simple regex for finding parts like "1h" or "30m"
    hours = re.search(r'(\d+)\s*h', time_str)
    mins = re.search(r'(\d+)\s*m', time_str)
    
    if hours:
        total_mins += int(hours.group(1)) * 60
    if mins:
        total_mins += int(mins.group(1))
        
    # Fallback: if just a number is given, assume minutes? 
    # Or if string contains "min", grab the number.
    if total_mins == 0 and "min" in time_str:
        nums = re.findall(r'\d+', time_str)
        if nums:
            total_mins += int(nums[0])
            
    return total_mins

def parse_file(path: Path) -> Optional[Problem]:
    m = FILE_RE.match(path.name)
    if not m:
        return None
    
    platform_key = m.group("platform")
    platform = PLATFORM_MAP.get(platform_key, "unknown")
    
    content = path.read_text(encoding="utf-8")
    
    # Extract docstring content (naive approach)
    # usually between triple quotes at the top
    docstring_match = re.search(r'"""(.*?)"""', content, re.DOTALL)
    metadata_text = docstring_match.group(1) if docstring_match else ""
    
    # Extract fields
    def get_val(key: str, default="?") -> str:
        # distinct keys followed by colon
        m = re.search(rf"^\s*{key}:\s*(.+)$", metadata_text, re.MULTILINE | re.IGNORECASE)
        return m.group(1).strip() if m else default

    difficulty = get_val("difficulty", "Unknown")
    time_str = get_val("time_spent", "?")
    time_mins = parse_time(time_str)
    tries_str = get_val("tries", "1")
    tries = int(re.search(r'\d+', tries_str).group()) if re.search(r'\d+', tries_str) else 1
    topic = get_val("topic", "misc")
    url = get_val("problem_link", "#")
    created_str = get_val("created", "?")
    
    created_date = None
    if created_str and "?" not in created_str:
        try:
            created_date = datetime.strptime(created_str, "%Y-%m-%d").date()
        except ValueError:
            pass # ignore bad dates

    return Problem(
        filename=path.name,
        platform=platform,
        difficulty=difficulty,
        time_spent_str=time_str,
        time_spent_mins=time_mins,
        created=created_date,
        tries=tries,
        topic=topic,
        url=url
    )

def scan_problems() -> List[Problem]:
    problems = []
    for p in REPO_ROOT.glob("*"):
        if not p.is_file(): continue
        if p.name.startswith("."): continue
        if p.name == "TEMPLATE.py": continue
        if p.name == "README.md": continue
        
        prob = parse_file(p)
        if prob:
            problems.append(prob)
    return problems

# --------------------------------------------------
# Stats Calculation
# --------------------------------------------------

def calc_streak(problems: List[Problem]) -> int:
    dates = sorted({p.created for p in problems if p.created})
    if not dates:
        return 0
    
    today = datetime.now().date()
    # If we haven't solved anything today, check if we solved something yesterday to keep streak alive
    current_streak = 0
    
    # Check "current" streak working backwards from today or yesterday
    check_date = today
    if check_date not in dates:
        check_date = today - timedelta(days=1)
        
    while check_date in dates:
        current_streak += 1
        check_date -= timedelta(days=1)
        
    return current_streak

def format_duration(minutes: int) -> str:
    if minutes < 60:
        return f"{minutes}m"
    h, m = divmod(minutes, 60)
    return f"{h}h {m}m"

def generate_topics_breakdown(problems: List[Problem], config: dict) -> str:
    """Generate a markdown list of topics covered with counts."""
    topic_counter = Counter()
    topic_filters = config.get("readme", {}).get("topic_filters", {})
    exclude = topic_filters.get("exclude", ["?", "misc"])
    min_count = topic_filters.get("min_count", 1)
    
    for p in problems:
        # Split topics by comma and clean them up
        topics = [t.strip().lower() for t in p.topic.split(',')]
        for topic in topics:
            if topic and topic not in exclude:
                topic_counter[topic] += 1
    
    if not topic_counter:
        return "_No topics tracked yet._"
    
    # Filter by min_count
    topic_counter = {k: v for k, v in topic_counter.items() if v >= min_count}
    
    # Sort by count (descending), then alphabetically
    sorted_topics = sorted(topic_counter.items(), key=lambda x: (-x[1], x[0]))
    
    lines = []
    for topic, count in sorted_topics:
        # Format: "arrays (12)", "hashing (8)", etc.
        lines.append(f"- **{topic}** ({count})")
    
    return "\n".join(lines)

# --------------------------------------------------
# Markdown Generation
# --------------------------------------------------

def generate_badges(total_solved: int, streak: int, total_time_mins: int, config: dict) -> str:
    """Generate badges based on config settings."""
    readme_config = config.get("readme", {})
    badge_style = readme_config.get("badge_style", "for-the-badge")
    show_streak = readme_config.get("show_streak", True)
    
    badges = []
    badges.append(f"![Solved](https://img.shields.io/badge/Solved-{total_solved}-blue?style={badge_style})")
    
    if show_streak:
        badges.append(f"![Streak](https://img.shields.io/badge/Streak-{streak}%20Days-orange?style={badge_style})")
    
    time_str = format_duration(total_time_mins).replace(" ", "%20")
    badges.append(f"![Time Spent](https://img.shields.io/badge/Time%20Spent-{time_str}-success?style={badge_style})")
    
    return " ".join(badges)

def generate_progress_table(problems: List[Problem], config: dict) -> str:
    """Generate stats table based on config platform order."""
    readme_config = config.get("readme", {})
    platform_order = readme_config.get("platforms", ["GeeksForGeeks", "LeetCode", "HackerRank", "Codeforces"])
    
    # Reverse map for display: slug -> Proper Name
    slug_to_name = {v: k for k, v in PLATFORM_MAP.items()}
    
    # Group by Proper Name
    grouped = defaultdict(list)
    for p in problems:
        display_name = slug_to_name.get(p.platform, p.platform.title())
        grouped[display_name].append(p)
    
    # Add any others found
    remaining_keys = sorted([k for k in grouped.keys() if k not in platform_order])
    final_order = platform_order + remaining_keys
    
    lines = []
    # Columns: Platform | Solved | Easy | Medium | Hard | Avg Time | Avg Tries | Vibe
    lines.append("| Platform | Solved | Easy | Medium | Hard | Avg Time | Avg Tries | Vibe |")
    lines.append("| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :--- |")
    
    for plat in final_order:
        probs = grouped.get(plat, [])
        # Only skip if empty AND not in our main list (we want to show 0s for main platforms)
        if not probs and plat not in platform_order:
            continue
            
        count = len(probs)
        
        # Difficulty breakdown
        easy = sum(1 for p in probs if "easy" in p.difficulty.lower())
        medium = sum(1 for p in probs if "medium" in p.difficulty.lower())
        hard = sum(1 for p in probs if "hard" in p.difficulty.lower())
        
        # Avg Stats
        valid_times = [p.time_spent_mins for p in probs if p.time_spent_mins > 0]
        avg_time = int(sum(valid_times) / len(valid_times)) if valid_times else 0
        
        valid_tries = [p.tries for p in probs]
        avg_tries = sum(valid_tries) / len(valid_tries) if valid_tries else 0.0
        
        # Vibe Check
        vibe = "ghost town"
        if count > 0:
            vibe = "warming up"
            if count > 10: vibe = "cooking"
            if count > 50: vibe = "on fire"
            if "LeetCode" in plat and hard > 5: vibe = "god mode"
        
        # Row
        avg_tries_str = f"{avg_tries:.1f}" if count > 0 else "-"
        avg_time_str = format_duration(avg_time) if count > 0 else "-"
        
        lines.append(f"| **{plat}** | {count} | {easy} | {medium} | {hard} | {avg_time_str} | {avg_tries_str} | {vibe} |")
        
    return "\n".join(lines)

def update_readme(problems: List[Problem], config: dict):
    """Update README using placeholders and save optimization data to config."""
    if not README.exists():
        return

    text = README.read_text(encoding="utf-8")
    
    # Calculate stats
    streak = calc_streak(problems)
    total_time = sum(p.time_spent_mins for p in problems)
    total_solved = len(problems)
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    # Generate content based on config
    readme_config = config.get("readme", {})
    
    badges_md = ""
    if readme_config.get("show_badges", True):
        badges_md = generate_badges(total_solved, streak, total_time, config)
    
    stats_table = ""
    if readme_config.get("show_stats_table", True):
        stats_table = generate_progress_table(problems, config)
    
    topics_md = ""
    if readme_config.get("show_topics", True):
        topics_md = generate_topics_breakdown(problems, config)
    
    # Replace placeholders
    text = text.replace("<!-- GRIND_BADGES -->", badges_md)
    text = text.replace("<!-- GRIND_STATS_TABLE -->", stats_table)
    text = text.replace("<!-- GRIND_TOPICS -->", topics_md)
    text = text.replace("<!-- GRIND_TIMESTAMP -->", timestamp)
    
    # Write updated README
    README.write_text(text, encoding="utf-8")
    
    # Update optimization cache in config
    topic_counter = Counter()
    for p in problems:
        topics = [t.strip().lower() for t in p.topic.split(',')]
        for topic in topics:
            if topic and topic not in ["?", "misc"]:
                topic_counter[topic] += 1
    
    config["optimization"]["last_update"] = timestamp
    config["optimization"]["total_files_scanned"] = total_solved
    config["optimization"]["cache"]["total_solved"] = total_solved
    config["optimization"]["cache"]["total_time_mins"] = total_time
    config["optimization"]["cache"]["current_streak"] = streak
    config["optimization"]["cache"]["topics"] = dict(topic_counter)
    
    # Update stats section
    platform_stats = {}
    slug_to_name = {v: k for k, v in PLATFORM_MAP.items()}
    grouped = defaultdict(list)
    for p in problems:
        display_name = slug_to_name.get(p.platform, p.platform.title())
        grouped[display_name].append(p)
    
    for platform, probs in grouped.items():
        platform_stats[platform] = {
            "count": len(probs),
            "easy": sum(1 for p in probs if "easy" in p.difficulty.lower()),
            "medium": sum(1 for p in probs if "medium" in p.difficulty.lower()),
            "hard": sum(1 for p in probs if "hard" in p.difficulty.lower())
        }
    
    config["stats"]["total_solved"] = total_solved
    config["stats"]["platforms"] = platform_stats
    config["stats"]["last_scan_timestamp"] = timestamp
    
    # Save updated config
    save_config(config)
    
    # Display results
    user_info = config.get("user", {})
    user_name = user_info.get("name", "")
    
    if user_name:
        print(f"✅ README updated for {user_name}!")
    
    print(f"📊 {total_solved} problems solved, {streak} day streak!")
    print(f"💾 Stats saved to grind.json")

if __name__ == "__main__":
    config = load_config()
    probs = scan_problems()
    update_readme(probs, config)
