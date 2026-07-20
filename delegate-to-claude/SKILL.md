---
name: delegate-to-claude
description: When and how to hand a task to Claude Code via the queue, including relaying its questions back to the user.
---
## When to use
Multi-file code changes, deep research, tasks failed twice locally.

## Procedure (queue-runner architecture, 2026-07-19)
1. Write full context to ~/agents/queue/<slug>.task (goal, constraints,
   file paths, relevant memory notes — Claude starts cold).
   Optional header lines at the top of the task file (worker parses them):
   - EFFORT:max / EFFORT:high — reasoning effort
   - MODEL:<name> — model override (no MODEL line = user default, fable)
   Everett's standing MODEL ROUTING (2026-07-19): thinking-heavy tasks
   (specs, design, architecture, debugging, audits, reviews) → EFFORT:max
   alone (fable, the top model); regular implementation of already-specced
   work → MODEL:opus + EFFORT:high (stretches the Max plan; Opus 4.8
   executes well-scoped file plans excellently).
2. STOP THERE. A launchd watcher (com.user.claude-worker, WatchPaths on
   ~/agents/queue) runs claude-worker.sh automatically within seconds.
   NEVER run the worker or `claude` manually — long tasks outlive the
   terminal tool's 180 s timeout. The worker is single-instance locked
   (~/agents/.worker.lock) and drains the queue sequentially.
3. Status: pending = ~/agents/queue/*.task · finished = queue/done/ ·
   failed = queue/failed/ · result JSON = newest
   ~/agents/logs/claude-<slug>-*.json (note its session_id field).
4. When a result is complete: summarize the outcome to daily-log/ and
   report back to the user, always including any line starting with "PR:".
5. If the result is a QUESTION or a permission/blocker report: relay it
   to the user verbatim. Then write a NEW task file whose FIRST LINE is
   exactly "RESUME:<session_id>" followed by the user's answer — the
   runner picks it up like any task and continues the same Claude session.
