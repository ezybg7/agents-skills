---
name: code-graph-usage
description: Answer code-structure questions with CodeGraph instead of crawling files — how does X work, where is X used, what breaks if I change it. Use before reading widely or editing shared code in an indexed repo.
---

# CodeGraph

A queryable graph of every symbol and edge in the repo. One query returns the verbatim source of the relevant symbols **plus** who calls them and what depends on them — including dynamic-dispatch hops (callbacks, React re-render, JSX children) that grep cannot follow. Reach for it **before** you read widely, and again before you edit anything shared.

## First, make sure there is an index

`.codegraph/` is gitignored, so a fresh clone has none. Building it is cheap — on this repo `codegraph init` indexes 537 files into ~6,700 nodes and 25,400 edges in **about 3 seconds**, and the index is ~32 MB. Run it once per checkout:

```
ls -d .codegraph 2>/dev/null || codegraph init
```

`codegraph status` reports the index's health.

**If `mcp__codegraph__codegraph_explore` is available, prefer it** — same answers, no shell. One catch, verified on 2026-09-11 (AMBR-31): the MCP server starts **before** your checkout exists, so it registers no default project and a bare query finds nothing. **Pass the checkout's absolute path as `projectPath`** on every call (`{query: "expiryLabel", projectPath: "<workdir>/pantry"}`). You still have to `codegraph init` inside the checkout first; the running server picks the index up without restarting. The CLI needs no `projectPath` because you run it from inside the repo — either path is fine, but do not report an MCP success you got from the CLI.

## Querying

| You want | Ask |
|---|---|
| How something works, or where it lives | `codegraph explore "expiry rules"` — name a file or symbol in the query to get its current line-numbered source |
| Everything that calls a symbol | `codegraph callers <symbol>` |
| What a change would break | `codegraph impact <symbol>` — run this **before** touching shared code |
| What a set of edits touches | `codegraph affected <files…>` |

## Rules

1. **Graph first, files second.** For "how does X work", "where is X used", a flow, or a blast radius, query before you open anything. A direct answer is one or two calls; the grep-and-read version is dozens.
2. **Treat returned source as already read.** Do not re-verify it with grep or a second Read — that is the cost the graph exists to avoid.
3. **Respect the staleness banner.** If a result is flagged stale, read that file directly; the index lags writes by about a second.
4. **Blast radius before refactors.** `codegraph impact` on the symbol you are about to change, and name in your PR what it said.
5. **No index, no argument.** If `codegraph init` fails, say so and fall back to reading — do not silently pretend the graph answered.

In pantry the highest-value queries are the shared pure modules — `expiry.ts`, `matching.ts`, `grouping.ts` — where a caller you did not know about is exactly the bug a review finds.
