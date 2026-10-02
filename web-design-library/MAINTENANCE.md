# Maintaining the web design library

Orchestrator-side notes. Not deployed to the board.

## Where these came from

| Files | Upstream | Commit |
|-------|----------|--------|
| all but `web-design-guidelines.md` | `github.com/Leonxlnx/taste-skill` (MIT), `skills/*/SKILL.md` | `ce26fc2` (2026-09-26) |
| `web-design-guidelines.md` | `github.com/vercel-labs/agent-skills`, `skills/web-design-guidelines/SKILL.md` | `063bee9` (2026-08-28) |

The files are byte-for-byte upstream copies, renamed from `SKILL.md` to `<name>.md` so that
neither Claude Code nor Hermes lists them as skills. **Do not edit them** — put corrections
in this file. To pull newer upstream versions run `scripts/refresh.sh`, read the diff, and
re-check the two tables above before committing.

Do not reinstall these with `npx skills add` or `skillfish add`: that puts them back at the
top level of `~/.claude/skills`, where every session on the mini and Hermes would list all
of them again.

## Deploying to the board

`~/agents/multica/sync-skills.py` carries the entry (`references/` only). After a refresh
or an edit to `SKILL.md`, run the sync and check `multica skill files list <skill-id>`.
