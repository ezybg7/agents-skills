---
name: delegate-to-claude
description: When and how to hand a task to Claude Code via the queue, including relaying its questions back to the user.
---
## When to use
Multi-file code changes, deep research, tasks failed twice locally.

## Procedure
1. Write full context to ~/agents/queue/<slug>.task (goal, constraints,
   file paths, relevant memory notes — Claude starts cold).
2. Run ~/agents/scripts/claude-worker.sh with the terminal tool and wait.
3. Read the newest claude-<slug>-*.json in ~/agents/logs/. Note its
   session_id field.
4. If the result is complete: summarize the outcome to daily-log/ and
   report back to the user.
5. If the result is a QUESTION or a permission/blocker report: relay it
   to the user on Discord verbatim and wait for their answer. Then write
   a new task file whose FIRST LINE is exactly "RESUME:<session_id>"
   followed by the user's answer on the next lines, and run the worker
   again. This continues the same Claude session with full context.
