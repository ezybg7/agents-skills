---
name: github-workflow
description: How to create repos, branches, commits, and PRs on GitHub for real projects.
---
## Conventions
- All projects live in ~/code/<name>, one git repo each, private by default.
- New project: gh repo create <name> --private --clone (run inside ~/code).
- Multi-file changes never go straight to main: create a branch
  (git checkout -b feat/<slug>), commit, push, then gh pr create --fill.
  The user reviews and merges PRs.
- Trivial single-file fixes may commit to main directly.
- Commit messages: one line, imperative mood ("add login route").
- NEVER commit secrets, .env files, tokens, or anything from ~/.hermes,
  ~/.claude, or ~/.ssh. Check git status before every commit.
- After pushing: gh run list --limit 3 to check CI; investigate failures
  with gh run view <id> --log-failed.
- Large changes: follow delegate-to-claude, and include the repo path and
  branch name in the task file.

## Reporting
- Every delegated task that opens a PR must end Claude's output with a
  final line of exactly: PR: <url>
- Hermes: after the worker finishes, find that line in the result JSON
  and post it to the Discord channel the task came from. If no PR line
  exists, say so explicitly rather than guessing.
- If a task depends on code in an unmerged PR, do not branch from main —
  report the dependency and wait for the merge instead.
- Before pushing "to a PR", verify the PR is still open:
  gh pr view <num> --json state. If it merged while you worked, commits
  pushed to its branch silently never reach main. Recovery: open a new PR
  from the same branch (it contains just the delta commits). This happened
  with pantry PR #3 → PR #5 on 2026-07-18.

## API-gated? ship an idempotent script instead of calling `gh` live
When `gh` is gated in the worker shell (see claude-worker-env) but the task
needs API writes — bulk-create issues, apply labels, open a PR — don't burn the
session fighting the gate. Commit a script into the repo on a pushed branch and
hand off a single command; the branch push works even when every `gh` call is
denied. Make the script safe to run exactly once by a permissioned human/spawn:
- **Upsert, never blind-create** — create labels/milestones only if absent.
- **Fetch existing state and skip matches** so re-runs can't duplicate. E.g.
  read existing issue titles, skip any that already exist (satisfies
  "no duplicates" even though the worker couldn't query the API itself).
- **Support `DRY_RUN=1`** to print what it would do without mutating.
- Put the exact invocation in the handoff (`bash scripts/create-tracking-issues.sh`;
  `DRY_RUN=1 bash …` to preview). CI + the script are the gate.
(Proven 07-21: `chore/spec-audit-tracking-issues` filed 18 spec-tracking issues
this way after `gh issue create` was denied 13×.)

## Stacked PRs (branch based on another open PR's branch)
- Prefer NOT to stack — branch from main and wait for the dependency to
  merge (see Reporting). Stack only when the work genuinely can't wait; if
  you do, say "stacked on #N, merge that first" in the PR body.
- When the base PR is **squash-merged**, the downstream PR breaks: GitHub
  leaves it OPEN · base=<merged-branch> · CONFLICTING · DIRTY, and its diff
  now mixes in all of the base's already-merged commits — not reviewable.
  Un-stack it (this is prep, NOT a merge):
  1. git fetch, then `git rebase --onto origin/main <old-base>` to drop the
     now-merged commits and replay only this PR's own commits.
  2. `git push --force-with-lease`.
  3. `gh pr edit <num> --base main` to retarget off the merged branch.
     PR should flip to MERGEABLE/CLEAN.
  4. A force-push done while the PR was DIRTY may NOT dispatch CI — trigger
     a fresh run with a no-content close→reopen (`gh pr close`/`reopen`),
     then confirm green with `gh pr checks <num>`.
  This was pantry PR #10 after #9 squash-merged, 2026-07-20.
