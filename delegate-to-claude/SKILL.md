---
name: delegate-to-claude
description: When and how to hand a task to Claude Code via the queue, including relaying its questions back to the user.
---
## When to use
Multi-file code changes, deep research, tasks failed twice locally.

## Procedure
1. Write full context to ~/agents/queue/<slug>.task (goal, constraints,
   file paths, relevant memory notes — Claude starts cold).
   Never start a slug with `done-` or `failed-` — the worker reserves those
   prefixes and will archive such files unrun.
   Optional header lines at the top of the task file (worker parses them):
   - EFFORT:max — thinking-heavy tasks (specs, architecture, debugging)
   - EFFORT:high — regular implementation tasks
   - MODEL:<name> — override model (default: the user's saved default, fable)
   Everett's standing rule: fable on max for thinking tasks, high for regular.
2. Run ~/agents/scripts/claude-worker.sh with the terminal tool and wait.
3. Read the newest claude-<slug>-*.json in ~/agents/logs/. Note its
   session_id field.
   Task lifecycle: the worker moves a finished task file to
   ~/agents/queue/done/<slug>.task (or failed/ on error). A file still in
   the queue root has not run yet. (Before 2026-07-19 the worker renamed
   finished tasks to done-<slug>.task in the queue root, which the *.task
   glob re-enqueued every night — test → done-test → done-done-test — and
   re-ran a $5 reflect job. If duplicate overnight runs ever reappear,
   check the queue root for marker-named files first.)
4. If the result is complete: summarize the outcome to daily-log/ and
   report back to the user.
5. If the result is a QUESTION or a permission/blocker report: relay it
   to the user on Discord verbatim and wait for their answer. Then write
   a new task file whose FIRST LINE is exactly "RESUME:<session_id>"
   followed by the user's answer on the next lines, and run the worker
   again. This continues the same Claude session with full context.
