---
name: delegate-to-claude
description: When and how to hand a task to Claude Code via the queue.
---
## When to use
Multi-file code changes, deep research, tasks failed twice locally.

## Procedure
1. Write full context to ~/agents/queue/<slug>.task (goal, constraints,
   file paths, relevant memory notes — Claude starts cold).
2. Run ~/agents/scripts/claude-worker.sh with the terminal tool and wait
   for it to finish.
3. Read the newest claude-*.json in ~/agents/logs/, summarize the outcome
   to daily-log/, and report back to the user.
