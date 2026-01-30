# dsa grind 💪

documenting my journey from  
**“what’s a linked list?”**  
to **“okay… i won’t embarrass myself in interviews today.”**

this repo exists because:

- vibes don’t pass interviews
- “i’ll figure it out on the job” apparently isn’t a strategy
- muscle memory doesn’t build itself

so yeah. we grind.

---

## the mission

solve problems.  
understand _why_ they work.  
get better over time.  
land a job.  
stop being terrible at this.

**preferably in that order.**

---

## where the pain happens

**current platforms:**

- **[geeksforgeeks](https://www.geeksforgeeks.org/)** — my current home base (warming up here)
- **[leetcode](https://leetcode.com/)** — the final boss (loading…)
- **[hackerrank](https://www.hackerrank.com/)** — when i need variety
- **[codeforces](https://codeforces.com/)** — when i’m feeling brave (or reckless)

no platform loyalty. only progress.

---

## how i organize the chaos

### file naming

```
PlatformName_Question_Title.py
```

examples:

- `GeeksForGeeks_Union_Of_Array_With_Duplicates.py`
- `LeetCode_Two_Sum.py` (soon™)
- `HackerRank_Array_Manipulation.py`

simple. searchable. future-me friendly.  
no cryptic abbreviations i’ll forget in two weeks.

---

### inside each file

every solution starts with honest documentation:

```
time_spent: 2 minutes (or 2 hours — both count)
difficulty: easy (allegedly)
topic: arrays, hashing, whatever torture device this is
problem_link: [the crime scene]
tries: 1 (Ls are tracked too, no shame)

notes:
my unfiltered thought process —
dead ends, breakthroughs, “wait… what?” moments

time_complexity: O(n) hopefully, not O(n³)
space_complexity: how much memory i’m burning

edge_cases_tested:
- empty inputs
- duplicates
- the obvious thing i somehow missed

learned:
what actually stuck after solving it

alternatives:
other approaches, when they exist
```

no corporate speak.  
no fake motivation.  
just what worked, what didn’t, and how long i stared at my screen.

---

## the setup

**what i’m running:**

- **[python](https://www.python.org/)** — because life is hard enough
- **[vs code](https://code.visualstudio.com/)** — the only editor i can configure without crying
- **[competitive companion](https://github.com/jmerle/competitive-companion)** — actual cheat code

### quick start

1. install python 3.7+
2. install vs code
3. install competitive companion (vs code extension)
4. install the browser extension
5. click the extension on any problem
6. it opens in vs code → hit run → dopamine

---

## scripts & automation (yes, i really over-engineered this)

this repo isn’t just a pile of `.py` files. there’s a small automation layer here whose only job is to **remove friction** and make progress visible.

### `scripts/new_problem.py`

creates a **ready-to-solve problem file** from a problem URL.

**what it does:**

- parses the problem URL (leetcode, gfg, hackerrank, codeforces)
- infers the platform automatically
- extracts the problem title
- generates a clean filename like:

```
LeetCode_Find_Players_With_Zero_Or_One_Losses.py
```

- creates a snake_case function name
- fills a standard `TEMPLATE.py`
- wires up a runnable local test block

**usage:**

```bash
python scripts/new_problem.py <problem_url>
```

no setup tax. just think.

---

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

---

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

---

### GitHub Actions (automatic stats updates)

there’s a GitHub Actions workflow that runs on every push.

**what it does:**

- detects new commits
- runs `scripts/update_stats.py`
- updates the README automatically if stats changed

so stats stay accurate **without me thinking about it**.

system > motivation.

---

## current stats (auto-updated, subject to emotional stability)

| platform      | solved | vibe check |
| ------------- | ------ | ---------- |
| geeksforgeeks | 3      | warming up |
| leetcode      | 2      | we move    |
| hackerrank    | 0      | tbd        |
| codeforces    | 0      | lol        |

## _last updated: 2026-01-29_

---

_if you’re reading this, you’re probably grinding too._  
_we’ll figure it out. eventually._

_ps: that “sigh…” in my code comments? yeah. that’s real._
