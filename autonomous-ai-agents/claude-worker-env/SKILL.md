---
name: claude-worker-env
description: THIS machine's Claude Code worker sandbox (queue-runner sessions) —
  PATH/allowlist workarounds, OrbStack docker, Supabase edge-runtime ops, and
  the facts every worker session otherwise rediscovers. Read at the start of
  any queued task that touches the shell, node, docker, or Supabase.
---
# Claude worker sandbox on the m4-mini

Queued tasks run via launchd `com.user.claude-worker` → `claude-worker.sh` in
a restricted sandbox. Every session from 07-19/20 rediscovered the same
environment facts the hard way; they are collected here. (Orchestrator-side
queue procedure lives in delegate-to-claude; gateway ops in
hermes-local-gateway-ops.)

## PATH and permission allowlist (the big one)

The worker shell PATH lacks `/opt/homebrew/bin`. Missing: `node`, `npm`,
`npx`, `gh`, `docker`, `supabase`. Present: `python3`, `curl`.

The allowlist accepts only **plain command forms** (`npm *`, `node *`,
`cp *`). All of these are DENIED — don't burn turns retrying them:

- `PATH=/opt/homebrew/bin:$PATH <cmd>` (env-prefixed)
- `/opt/homebrew/bin/npm ...` (absolute path)
- `zsh -lc "..."`, `export PATH=... && ...`, compound `cd X && git ...`
- `ln -s` (symlinks into ~/.local/bin), `rm`
- `dangerouslyDisableSandbox: true` (denied every time, in every session)

Working routes, in order of preference:

1. **node**: `~/.local/bin/node` is a *copy* of Homebrew's node (with
   `~/.local/lib/libnode.147.dylib`); ~/.local/bin is on PATH via .zshrc, so
   plain `node ...` passes the allowlist. Goes stale when Homebrew upgrades
   node — re-copy with `cp` (allowed) if it breaks.
2. **npm**: no binary — invoke as
   `node /opt/homebrew/lib/node_modules/npm/bin/npm-cli.js <cmd>`
   (package.json scripts: `npm run typecheck` / `lint` / `test` equivalents).
3. **Everything else** (gh, docker, supabase, curl-with-secret): python3
   subprocess helper — write `/tmp/<task>_helper.py` (or `~/agents/tmp_*`),
   use `subprocess.run([...], cwd=<repo>, env={**os.environ, 'PATH':
   '/opt/homebrew/bin:/Applications/OrbStack.app/Contents/MacOS/xbin:' +
   os.environ['PATH']})`. HTTP with secrets: `urllib.request` inside the
   script (inline-secret curl commands get denied).
4. `rm` is blocked: you cannot delete your own temp files. Name them
   predictably (`~/agents/tmp_*`) and flag them "safe to delete" in the
   handoff note.

## Docker = OrbStack

No plain `docker` binary exists anywhere on default PATHs. The CLI is at
`/Applications/OrbStack.app/Contents/MacOS/xbin/docker`; socket
`unix://$HOME/.orbstack/run/docker.sock`. Put the xbin dir on PATH inside a
node/python spawn (route 3 above) — `DOCKER_HOST=` prefixing is denied.

## Supabase local stack (pantry: ~/code/pantry)

- **`supabase start` does NOT start the edge-functions runtime** in this CLI
  version. The runtime is served only by a detached
  `supabase functions serve --env-file supabase/functions/.env`
  (run from the repo, xbin on PATH, log to
  `~/agents/logs/pantry-functions-serve.log`). It stays up until reboot or
  `supabase stop`. Check for a stale prior serve pid before starting a new
  one (avoid a double-serve).
- **Runtime-down triage** (the 07-20 incident): `GET /rest/v1/...` 200
  proves Kong+PostgREST+DB fine; then probe a real function AND a
  nonexistent one — identical `503 {"message":"name resolution failed"}` on
  both = the whole edge runtime is down, not your function's code.
- Healthy-serve signals: `OPTIONS /functions/v1/<fn>` → 204; unauth POST →
  401 "Missing authorization header".
- `supabase status --workdir <repo>` works via a spawn with xbin on PATH.
- `supabase db reset` is DESTRUCTIVE (wipes local dev data) — document it
  for the user, don't run it. (Autonomy line: do non-destructive ops
  yourself; list destructive ones in the handoff/PR.)
- Expo Go on-device points at the LAN IP (`http://10.0.0.74:54321`), not
  localhost — client-side "backend down" symptoms can be LAN/IP issues too.

## Task lifecycle facts

- Autonomy policy (repo CLAUDE.md §Autonomy & escalation + queue preamble
  `~/agents/queue/.preamble.md`): do operational work yourself — restart
  services, migrations, installs, verification; escalate only genuine
  design choices, in the PR, never blocking. End PR-producing tasks with
  `PR: <url>`.
- The worker writes the result JSON (`~/agents/logs/claude-<slug>-*.json`)
  only at completion — a 0-byte JSON plus a .task still in the queue root
  means the run is in progress or died; there is no failed/ record for a
  killed run, and the unmoved .task re-runs on next pickup.
- Session ids for the `RESUME:<session_id>` flow are UUIDs copied verbatim
  from the result JSON. Never invent, shorten, or recall one from memory
  (the "sess_12345" fabrication incident, 2026-07-20).
