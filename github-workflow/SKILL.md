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
