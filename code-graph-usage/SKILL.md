---
name: code-graph-usage
description: Answer code-structure questions via CodeGraph, not file crawling.
---
1. For "how does X work", "where is X used", flows, or impact questions:
   call codegraph_explore (or `codegraph explore "<query>"` from CLI) FIRST.
2. Treat returned source as already read — do not re-verify with grep.
3. Respect the ⚠️ staleness banner: if shown, Read that file directly.
4. Before large refactors, check blast radius: `codegraph impact <symbol>`.