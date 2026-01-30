<!-- GRIND_BADGES -->

## current stats

<!-- GRIND_STATS_TABLE -->

### topics covered

<!-- GRIND_TOPICS -->

## _last updated: <!-- GRIND_TIMESTAMP -->_

---

documenting my journey from  
**“what’s a linked list?”**  
to **“okay… i won’t embarrass myself in interviews today.”**

this repo exists because:

- vibes don’t pass interviews
- “i’ll figure it out on the job” apparently isn’t a strategy
- muscle memory doesn’t build itself

so yeah. we grind.

---

<details>
<summary><strong>the mission</strong></summary>

solve problems.  
understand _why_ they work.  
get better over time.  
land a job.  
stop being terrible at this.

**preferably in that order.**

</details>

---

<details>
<summary><strong>where the pain happens</strong></summary>

**current platforms:**

- **[geeksforgeeks](https://www.geeksforgeeks.org/)** — my current home base (warming up here)
- **[leetcode](https://leetcode.com/)** — the final boss (loading…)
- **[hackerrank](https://www.hackerrank.com/)** — when i need variety
- **[codeforces](https://codeforces.com/)** — when i’m feeling brave (or reckless)

no platform loyalty. only progress.

</details>

---

<details>
<summary><strong>how i organize the chaos</strong></summary>

### file naming

```
PlatformName_Question_Title.py
```

examples:

- `GeeksForGeeks_Union_Of_Array_With_Duplicates.py`
- `LeetCode_Two_Sum.py` (soon™)

no setup tax. just think.

### `TEMPLATE.py`

the blueprint every problem file starts from.

**why it exists:**

- keeps documentation consistent
- forces me to think about complexity, edge cases, and takeaways
- removes decision fatigue

the generator:

- fills metadata like `problem_link` and `created`
- renames the `solve` function to match the problem title

no imports.  
no assumptions.  
just structure.

### `scripts/update_stats.py`

keeps the README honest.

**what it does:**

- scans the repo for solved problems using filename prefixes
- counts solutions per platform
- updates the **current stats** table
- refreshes the “last updated” date

**manual run:**

```bash
python scripts/update_stats.py
```

### GitHub Actions (automatic stats updates)

there’s a GitHub Actions workflow that runs on every push.

**what it does:**

- detects new commits
- runs `scripts/update_stats.py`
- updates the README automatically if stats changed

so stats stay accurate **without me thinking about it**.

system > motivation.

</details>

---

<details>
<summary><strong>configuration (grind.json)</strong></summary>

the `grind.json` file lets you customize how your README looks and stores optimization data.

### quick settings

**customize your name:**

```json
{
  "user": {
    "name": "Your Name",
    "github_username": "yourusername"
  }
}
```

**toggle what shows up:**

```json
{
  "readme": {
    "show_badges": true, // badges at the top
    "show_stats_table": true, // platform stats table
    "show_topics": true, // topics breakdown
    "show_streak": true // streak badge
  }
}
```

**change badge style:**

```json
{
  "readme": {
    "badge_style": "for-the-badge" // or "flat", "flat-square", etc.
  }
}
```

**filter topics:**

```json
{
  "readme": {
    "topic_filters": {
      "exclude": ["?", "misc"], // skip these topics
      "min_count": 1 // only show topics with X+ problems
    }
  }
}
```

**reorder platforms:**

```json
{
  "readme": {
    "platforms": ["LeetCode", "GeeksForGeeks", "HackerRank", "Codeforces"]
  }
}
```

### what gets stored

the script saves optimization data so it doesn't have to rescan everything:

- `optimization.cache` — cached stats (solved count, time, streak, topics)
- `stats.platforms` — breakdown by platform (count, easy/medium/hard)
- `optimization.last_update` — when stats were last updated

### placeholders in README

these get replaced when you run `python scripts/update_stats.py`:

- `<!-- GRIND_BADGES -->` → badges
- `<!-- GRIND_STATS_TABLE -->` → platform stats table
- `<!-- GRIND_TOPICS -->` → topics list
- `<!-- GRIND_TIMESTAMP -->` → last update date

so you can write whatever you want in the README, and only the stats get auto-updated.

no more manual counting. no more stale stats.

</details>

---

_if you’re reading this, you’re probably grinding too._  
_we’ll figure it out. eventually._

_ps: that “sigh…” in my code comments? yeah. that’s real._
