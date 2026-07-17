---
name: memory-protocol
description: How to use the shared memory vault before and after every task.
---
## Before starting a task
1. Identify the project or topic; grep ~/agents/memory/ for matching notes
   (projects/, decisions/, entities/).
2. Load only the relevant files — keep context small.

## After finishing a task
1. Append a handoff note to ~/agents/memory/daily-log/<YYYY-MM-DD>.md:
   what was done, decisions made, open items, files touched.
2. If a durable fact was learned (a preference, a decision, a location of
   something), update the matching file in projects/ or entities/.
