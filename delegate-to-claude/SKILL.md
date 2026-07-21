---
name: delegate-to-claude
description: When and how to hand a task to Claude Code via the queue, including relaying its questions back to the user.
---
## When to use
Multi-file code changes, deep research, tasks failed twice locally.

## Procedure (queue-runner architecture, 2026-07-19)
1. Write full context to ~/agents/queue/<slug>.task (goal, constraints,
   file paths, relevant memory notes — Claude starts cold).
   Never start a slug with `done-` or `failed-` — the worker reserves those
   prefixes and will archive such files unrun.
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
3. Completions notify Discord automatically: claude-worker.sh posts each
   finished task to #reports via `hermes send` (no LLM, no agent loop, so it
   survives relay rate limits) with status, duration, cost, any PR: line, a
   result tail, and the session_id. Override the target with
   WORKER_NOTIFY_TARGET; the body is built in the worker's python heredoc.
   On-demand status: pending = ~/agents/queue/*.task · finished = queue/done/ ·
   failed = queue/failed/ · result JSON = newest
   ~/agents/logs/claude-<slug>-*.json (note its session_id field).
   A file still in the queue root has not run yet. (Before 2026-07-19 the
   worker renamed finished tasks to done-<slug>.task in the queue root,
   which the *.task glob re-enqueued every night and re-ran a $5 reflect
   job. If duplicate overnight runs ever reappear, check the queue root
   for marker-named files first.)
4. When a result is complete: summarize the outcome to daily-log/ and
   report back to the user, always including any line starting with "PR:".
5. If the result is a QUESTION or a blocker report, triage it first
   (autonomy policy, 2026-07-20):
   - OPERATIONAL asks (restart a service, apply a migration, reset/seed a
     dev DB, install deps, rerun checks) → do NOT bounce these to the
     user. Re-queue them as a new task — workers perform ops themselves
     per the repo CLAUDE.md §Autonomy & escalation and the queue preamble.
     Exception: destructive ops (data-wiping resets, deletes) stay with
     the user, explicitly labeled destructive.
   - GENUINE DESIGN/implementation-choice questions → relay to the user
     verbatim. Then continue the same Claude session: write a NEW task
     file whose FIRST LINE is exactly "RESUME:<session_id>" followed by
     the user's answer.
   The session_id is a long UUID — copy it exactly from the result JSON
   at the moment you write the RESUME file; never invent, shorten, or
   recall one from memory (sess_12345 incident, 2026-07-20).
6. If your own reply/narration dies mid-turn (e.g. a rate limit), the
   functional work usually completed first — reconstruct status from the
   queue dirs and result JSONs, never from the truncated chat reply.
