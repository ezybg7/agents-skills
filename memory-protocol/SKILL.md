---
name: memory-protocol
description: How to use the shared memory vault before and after every task.
---

The vault at `~/agents/memory/` is an **OKF bundle** — one concept per file, YAML
frontmatter, cross-linked, with an `index.md` at every level. Rules:
`~/agents/SPEC.md` §2.1.

## Before starting a task

1. Open **`~/agents/memory/index.md`** and follow links down. Do not grep first —
   the index exists so you can pick one file instead of reading the directory.
   Grep is the fallback when you do not know what you are looking for.
2. Route by what you need:
   - current state of a project → `projects/` (hub note, then its linked concepts)
   - why something is the way it is → `decisions/`
   - what a machine/repo/service is → `entities/`
   - an external spec or paper we have read → `sources/`
3. Load **only** the matching concepts. One file per concept means you can.
4. Operating rules are Layer 3 in `~/agents/references/` — not in the vault.
   Read `safety-rules.md` before any production action.

## After finishing a task

1. Append a handoff note to `~/agents/memory/daily-log/<YYYY-MM-DD>.md`: what was
   done, decisions made, open items, files touched.
2. A durable fact goes in **its own concept file**, not appended to whatever note
   is nearest:

   | The fact is | Where it goes |
   |---|---|
   | a choice made, with a why | new file in `decisions/` |
   | a machine, repo, or service | `entities/` |
   | project state | that project's hub or a linked concept |
   | a trap or workaround | that project's gotchas concept |
   | an external source you read | `sources/` |

3. New file → give it frontmatter (`type` is required and must be informative;
   `note` is not a type) and link it from the enclosing `index.md`:

   ```bash
   python3 ~/agents/scripts/okf-normalize.py <file>   # fills frontmatter
   python3 ~/agents/scripts/okf-index.py memory references
   python3 ~/agents/scripts/okf-check.py              # must exit 0
   ```

4. Cross-link it. A concept nothing links to is an orphan, and `okf-check.py`
   fails the vault for it.

## Writing a concept

Keep one concept per file. When a note grows a section that a reader would want
**without** the rest of the note, that section is its own concept — split it and
link back. `projects/pantry.md` is the worked example: a hub plus six linked
concepts, split out on 2026-09-10.

## If memory MCP tools are available

`search_notes` / `write_note` (basic-memory) read and write the same files.
It is a second producer: it owns `permalink`, canonicalizes YAML, and can leave a
stacked frontmatter block on files edited outside it. `okf-normalize.py` merges
those — run it after bulk external edits.
