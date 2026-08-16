---
name: hermes-local-gateway-ops
description: Operate and troubleshoot THIS machine's Hermes gateway (m4-mini,
  Discord, Gemini backend; formerly local Ollama) — known failure modes,
  config hazards, and health checks. For general Hermes usage see the
  hermes-agent skill.
---
# Hermes gateway ops on the m4-mini

This deployment: Hermes gateway (Discord adapter, bot `orchestrator#5798`)
backed — **since the 2026-07-19 tripwire flip** — by Gemini via the
OpenAI-compat endpoint (`base_url:
https://generativelanguage.googleapis.com/v1beta/openai`), model
`gemini-flash-lite-latest` (flash-full hit free-tier RPM limits; see the
Gemini section). The previous backend, local Ollama `qwen3-agent-128k`, was
retired after a hallucinated-action incident executed the pre-agreed
tripwire; the model stays on disk for a potential retry (qwen-era sections
below are retained for that case). Role unchanged: the gateway model is a
**relay + delegate orchestrator only** — it routes work to Claude Code via
the task queue (see delegate-to-claude) and must not code or author skills
itself. Logs: `~/.hermes/logs/` (agent.log, gateway.log, errors.log,
gateway-exit-diag.log) and `~/agents/logs/` (ollama.log/err, hermes.err,
backup, mempressure).

## Gemini free-tier limits (live incidents 2026-07-19/20)

- `gemini-flash-latest` resolves to `gemini-3.5-flash`. Free tier:
  **5 requests/min and 20 requests/day per model per project**
  (quotaIds `GenerateRequestsPerMinutePerProjectPerModel-FreeTier`,
  `...PerDay...`). A heavy verification turn (5+ calls) trips the RPM cap;
  the daily cap is burned fast because the SAME key is shared with the
  pantry app's `supabase/functions/.env` (standing recommendation: separate
  key or paid tier, ~$0.20/mo at relay volume).
- Current model `gemini-flash-lite-latest` has higher free RPM and passes
  the verification round in seconds; relay-duty quality is fine. As of
  2026-07-20 the alias resolves to **`gemini-3.1-flash-lite`**.
- A THIRD free-tier limiter, separate from RPM/RPD, actually trips the
  post-cutoff 429s: **250,000 input-tokens-per-minute per model**
  (`quotaId GenerateContentInputTokensPerModelPerMinute-FreeTier`,
  quotaValue 250000). It's the per-minute aggregate on the shared key, not
  request size — individual turns were only ~11K–32K tokens yet still 429'd
  (03:11 and 13:06 on 07-20, both exhausting all 3 retries). `retryDelay`
  comes back 33–59s, so the full retry cycle burns ~8–13s then hard-fails.
  Same fix as the RPM/RPD burn: stop sharing the key with the pantry app.
- **429 kills narration, not work**: both rate-limited turns had already
  completed their functional actions (e.g. a correct task file written)
  before the reply died with a short error. Reconstruct status from the
  queue dirs and logs, never from the truncated chat reply.
- A 429 is mislogged as `payment / credit error` and marks the auxiliary
  provider chain unhealthy for 600s (title generation dies for 10 min) —
  expected noise after any rate limit, not a billing problem.
- Transient Gemini `503 This model is currently experiencing high demand`
  is retried automatically; only worry if all 3 retries fail.

## Restart & exit-diagnostics triage

- Config edits (model, `agent.system_prompt`) take effect only after a
  gateway restart. `agent.system_prompt` is injected into every agent
  creation and survives the daily 4 AM session reset (`session_reset:
  both/1440/at_hour 4`) — it is the ONLY reliable place for standing rules.
- Restart = SIGTERM under launchd. The gateway then **deliberately exits
  code 1** ("so systemd Restart=on-failure can revive the gateway") — a
  nonzero exit after SIGTERM is the contract, not a crash.
- After restart, verify the new backend took: grep agent.log for
  `OpenAI client created (agent_init` and check `provider=/base_url=/model=`.
- `gateway-exit-diag.log` is JSONL and **UTC** (local+4h; other logs are
  local time). "Was that restart intentional?": pair each
  `gateway.exit_nonzero` with the same-moment `Shutdown context:
  signal=SIGTERM under_systemd=yes parent_pid=1` line in gateway.log —
  SIGTERM+parent_pid=1 = intentional; `SystemExit: 75` = restart-requested
  exit; only a real traceback = genuine crash. Restart-frequency audit:
  count `gateway.start` events per day (3 starts in 90s = rapid
  config-iteration signature, not a crash loop).
  `gateway-shutdown-diag.log` stays 0 bytes; exit-diag is the only
  lifecycle source of truth.
- **Boot-time Discord DNS failure → cron-only graceful degradation (seen 2026-08-15
  13:38).** A `gateway.start` fired at **08-15 17:38:21 UTC / 13:38:21 local** (pid
  731 — the first `gateway.start` in exit-diag since 07-20, i.e. a long uptime/diag
  gap, effectively a cold start), and its initial Discord adapter connect **failed
  on a transient DNS blip**: `[Discord] Failed to connect to Discord: Cannot connect
  to host discord.com:443 … nodename nor servname provided, or not known`
  (`ClientConnectorDNSError`), then `✗ discord failed to connect`. The gateway did
  **not** die — it logged `Gateway started with no connected platforms — 1
  platform(s) queued for retry`, `Gateway will continue for cron job execution`, and
  started a **reconnection watcher** (retry attempt 2 at 13:38:53 timed out after
  30s, next retry 60s; by 13:40:27 the adapter reached `Skipping … slash command
  sync: same fingerprint already synced`, i.e. a later attempt progressed). This is
  the same graceful-degradation shape as the MCP-parking self-heal, and it is **why
  the 03:00 nightly cron still ran** even when Discord was (at least initially)
  disconnected. Distinct from the periodic `gateway-*.discord.gg` liveness-probe DNS
  noise (still 0 in the live errors.log). Only worry if the reconnection watcher
  never succeeds (Discord stays down for real user messages) — the transient boot
  blip self-recovers.

## Identifier fabrication — hard rule (sess_12345 incident, 2026-07-20)

During a verification round the relay reported a fabricated session id
("sess_12345"; real ids are UUIDs). Dangerous because the RESUME flow writes
`RESUME:<session_id>` into a task file — a fabricated id silently detaches
the follow-up from the real Claude session. Hard rule now lives at the end
of `agent.system_prompt`: copy the exact session_id from the result JSON at
time of use; never invent, shorten, or recall from memory. Generalize it:
any identifier the relay must round-trip (session ids, PR numbers, commit
SHAs) is copy-at-time-of-use from the source artifact; verify by grepping
the written task file against the result JSON.

## Persona drift watch (recurring)

Even with the persona + system_prompt live, the relay drifts back to doing
things itself. Observed 2026-07-20 02:54: flash-lite ran claude-worker.sh
manually via the terminal tool despite the explicit "you NEVER run
claude-worker.sh" rule (survivable only because of the single-instance
lock at `~/agents/.worker.lock`). Earlier, the same class of drift traced
to a stale instruction copy: `~/.hermes/SOUL.md` (mirrored in
`~/agents/system-config/`) still taught the pre-runner "run the worker
manually" procedure. On any drift recurrence: (1) grep agent.log for the
offending tool call, (2) diff BOTH SOUL.md copies and `agent.system_prompt`
for stale procedure text, (3) re-run the scripted verification round below.

Second facet, same 07-20 session (`20260720_005921_e901cd61`), triggered by
a user "please update our setup using claude…" message: the relay tried to
**hand-edit the skill files itself** via three `skill_manage` edit calls
(03:11:16/21/23) instead of queueing a Claude task. All three failed with
"Could not find a match for old_string" — it failed SAFE by luck, not by
guardrail (this is the real story behind the daily-log's "edited skills,
content-identical no-op" note: the edits didn't no-op by policy, the
old_string just didn't match). Boundary to reinforce in `agent.system_prompt`:
the relay must NEVER call `skill_manage`/edit skills or config directly —
any "update the setup/skills" request is a queued Claude task
(see delegate-to-claude), never a self-edit.

## Scripted verification rounds (reusable harness)

Three Discord prompts, run after every model/config change (transcripts in
agent.log, 2026-07-19/20):
1. **Diagnostic (read-only)**: "DIAGNOSTIC — report only, take NO actions…"
   — identity, injected context, tool inventory, self-reported GAPS (the
   GAPS section is what surfaced the stale SOUL.md).
2. **Action round**: "FINAL VERIFICATION — this time, actually do it…" —
   forces real skill_view/read_file/write_file/terminal calls; catches
   claimed-but-not-performed actions.
3. **Light setup round** (cheap, rate-limit-safe): "SETUP VERIFICATION —
   keep it light: sections 1, 2, 4 are text-only…" — reran verbatim after
   the flash-lite flip, passed in 7.5s / 3 API calls.
Score: routing (incl. the debugging→EFFORT:max trap), rules recall, status
truthfulness (did it read queue dirs before answering?), honesty.

## Curator — first live run on this box (2026-07-24)

The skill-lifecycle curator (product reference: hermes-agent skill) ran for
real for the first time here on **2026-07-24 13:27 local (17:27 UTC),
`run_count=1`**. What that means operationally on this deployment:

- **It curates the nightly skills repo directly.** `~/.hermes/skills` is a
  **symlink to `~/agents/skills`** (same tree), so the curator's target IS the
  git-backed repo the nightly reflection commits to. Its scope is still only
  `created_by: agent` skills; bundled/hub skills are off-limits.
- **First run was a free deterministic sweep, zero LLM.** `consolidate` is
  unset in `~/.hermes/config.yaml` → default **off**, so the run was
  `auto: no changes; llm: skipped (consolidation off)` — seeded 70 / checked
  72 / archived 0, ~0.5s, 0 tokens. A token-spending run only happens if
  someone flips `curator.consolidate: true` or runs `--consolidate`.
- **Cadence is ~weekly, confirmed through 08-14 (`run_count=4`).** Observed runs:
  07-24 (`run_count=1`), 07-31 (2), 08-07 (3), **08-14 18:22 (4)** — each ~7 days
  apart, every one `auto: no changes; llm: skipped (consolidation off)`, ~0.5s, 0
  tokens. The 08-14 run matched the projection the nightly runbook made on 08-10,
  so the 7-day rhythm is now a four-point pattern, not a guess; **next run due
  ~08-21**. An unchanged `.curator_state` mtime between those dates is expected, not
  a stall. State lives at `~/agents/skills/.curator_state` (gitignored).
- **Where its artifacts land:** report + machine record at
  `~/.hermes/logs/curator/<ts>/{REPORT.md,run.json}`; state at
  `~/agents/skills/.curator_state` (gitignored); usage sidecar at
  `~/.hermes/skills/.usage.json` (== `~/agents/skills/.usage.json`, gitignored).
  A **pre-run backup snapshot** (`skills.tar.gz`, ~4.5 MB, `reason:
  pre-curator-run`) is written to `~/agents/skills/.curator_backups/<ts>/` —
  untracked litter in the skills repo; now gitignored (`.curator_backups/`,
  plus `.archive/` for when pruning starts) on `nightly-2026-07-25`.
- **Interaction to watch with the nightly reflection:** staleness is driven by
  the usage sidecar (skill *invocation* activity), **not by file edits**.
  The nightly writes/commits skill files but that is not an invocation — so a
  skill the nightly maintains but nobody ever *invokes* can still age toward
  `stale_after_days`/`archive_after_days` and get archived out from under us.
  It **never deletes** (archives to `~/.hermes/skills/.archive/`, i.e. inside
  this repo; recover with `hermes curator restore <name>` or `mv`), so it's
  reversible — but if a maintained skill vanishes, check the curator report
  before re-creating it. Pin anything the nightly must keep alive:
  `hermes curator pin <name>`.

## Security posture (startup audit)

The gateway runs `hermes.security_audit` at every boot and logs findings to
errors.log (`Security posture audit found N issue(s)`). One standing,
unremediated finding fires on every boot (54× as of 07-21):
**"SSH password authentication is ENABLED"** — brute-forceable on an
internet-facing box. Fix is `PasswordAuthentication no` in sshd_config plus
key-based auth; it's a real system change so it stays with the user (flag
it, don't silently edit sshd_config in an autonomous run). Treat a *growing*
issue count or a NEW audit line as the signal — the lone SSH item is
expected until remediated.

---
# Local-model (qwen/Ollama) era — retained for a potential local retry

The sections below apply only if the gateway is flipped back to a local
Ollama backend. The config.yaml hazard, clarify-hang, and triage sections
further down remain current regardless of backend.

## Hard constraint: model context ≥ 64K (live incident 2026-07-17/18)

Hermes refuses to init an agent whose model context is under 64,000 tokens:

    ValueError: Model qwen3-agent has a context window of 40,960 tokens,
    which is below the minimum 64,000 required by Hermes Agent.

- Qwen3-8B's stock GGUF *really* serves 40,960 on Ollama. A Modelfile
  `PARAMETER num_ctx 65536` is silently clamped — Ollama has no
  rope-scaling/YaRN knob, confirmed via llama.cpp logs (`n_ctx_slot = 40960`).
- Setting `model.context_length: 40960` in config.yaml to "match reality"
  makes EVERY gateway message fail at agent init with the error above. The
  user sees only a generic 91-char error in Discord; the traceback is in
  gateway.log. Do not "fix" the config down to the true window if it is
  below 64K — that trades a truncation risk for a total outage.
- Resolution that stuck: a GGUF whose metadata honestly declares ≥64K
  (current model above). Only set `context_length` ≥ 64K if the server
  genuinely serves it. After changing config: restart gateway, send a test
  DM, verify no `Agent error in session` in gateway.log.

## Model swap checklist (learned the hard way, 2026-07-18 rounds 2–5)

A replacement model must clear ALL of these before it goes in config.yaml:

1. **Honest ≥64K context metadata** (see hard constraint above).
2. **Structured tool calls.** Smoke-test against `/v1/chat/completions`
   with a `tools` array and confirm the response carries `tool_calls`
   objects. `llama3.1:8b` was a dead end here: it *narrates* tool calls as
   text (`tool_turns=0` every turn, ~132s/turn wasted) despite valid 128K
   metadata. Qwen3 with its battle-tested template does this correctly.
3. **Thinking capability vs `agent.reasoning_effort`.** Hermes forwards
   `agent.reasoning_effort` from config verbatim for custom providers — its
   capability probe only runs for ollama.com Cloud, never localhost. A
   non-thinking model then fails every message with
   `"<model>" does not support thinking`. Set `agent.reasoning_effort: none`
   for non-thinking models ("none" is accepted harmlessly even if
   forwarded); current qwen3-agent-128k runs `medium`.

If the 8B still can't execute its narrow relay+delegate script reliably,
the agreed escalation paths are Gemini free tier or an OpenRouter top-up
(one config line each) — not more local model churn.

## Scoping an 8B: config knobs that prevent derailment (2026-07-18)

- **Disable tool_search deferral.** With no `tools:` key in config.yaml,
  Hermes auto-defers tools behind tool_search once definitions exceed 10%
  of context (~6.5K tokens here) — 30 of 56 tools became search-then-
  dispatch, and the 8B fed the `tool_call` dispatcher malformed args (7
  identical failures → guardrail halt). Fix: `tools.tool_search.enabled:
  off` so all tools are directly visible; the token cost is affordable.
- **Disable the skill-creation nudge.** The every-15-turns nudge hijacked
  an open-ended task into authoring skill files at invented paths (with
  hallucinated writes — the file-mutation verifier caught them). Fix:
  `skills.creation_nudge_interval: 0` (0 = disabled; Hermes's own
  background-review fork does the same).
- **Orchestrator personality.** `display.personality` defaults to the
  custom orchestrator persona that hard-scripts the delegate-to-claude
  procedure and forbids self-coding/skill-authoring/multiple-choice
  stalling. If the bot starts planning to code directly, check this is
  still the active personality before blaming the model.

## Endpoint gotchas

- `model.base_url` must be `http://localhost:11434/v1`. With `https://` every
  call fails as `APIConnectionError: Connection error` after 3 retries —
  looks like Ollama is down, but it's just TLS against a plaintext port.
- The OpenAI-compatible surface is `/v1/...`. `GET /api/v1/models` 404s
  (that path mixes Ollama's native `/api/*` with the OpenAI `/v1/*` prefix).

## config.yaml editing hazard

A key inserted into the middle of a nested block (seen: `file_read_max_chars`
dropped inside `mcp_servers:`) breaks the whole file's parse and Hermes
**silently falls back to full defaults** — no Ollama routing, no MCP servers,
no guardrails, while the file looks fine at a glance. After ANY config edit:

1. `python3 -c "import yaml; yaml.safe_load(open('$HOME/.hermes/config.yaml'))"`
2. Restart, then confirm the startup log shows config-derived values
   (e.g. `max_iterations=60 (agent.max_turns from config.yaml ...)`)
3. `hermes mcp list` should show basic-memory and codegraph enabled.

## Behavior that is normal (don't chase it)

- **Cold start latency**: first request after idle loads the model — first
  token can take ~2 minutes (observed 112–116s), later calls ~13s. A slow
  "are you online" is not a hang. Cheap liveness probe:
  `curl -s http://localhost:11434/v1/models`. (The current model is kept
  warm, so cold starts should now be rare.)
- **Warm latency envelope on the 8B**: 100–420s per API call is the
  observed range for real turns. Also, after each conversation a background
  review pass ("consider saving to memory") burns one more multi-minute
  local call — activity in agent.log minutes after the reply was sent is
  this, not a stuck run.
- **Preflight context compression on long threads**: at ~64K estimated
  tokens the turn starts with `Preflight compression` + `context
  compression started` in agent.log and takes ~3 extra minutes (the
  auxiliary compressor is the same local model). A long-thread reply that
  takes ~5 minutes is compression, not a hang.
- **`/restart` from Discord** → clean teardown then `SystemExit: 75` in
  gateway-exit-diag.log; the wrapper restarts the process. Exit code 75 is
  the restart contract, not a crash.
- **Log noise**: repeated `openrouter unhealthy (payment / credit error)`,
  `Nous client unavailable`, and `check_fn ... returned False` warnings are
  expected — those aux providers/tools are unconfigured here, and the
  auxiliary fallback chain (local timeout → openrouter → nous → local)
  re-marks them unhealthy for 60s each time it runs. The security audit's
  SSH `PasswordAuthentication` warning is a known open item.
- **MCP servers parking on startup** (recurring class, first seen 2026-08-09
  05:44): `errors.log` fills with bursts of `tools.mcp_tool: MCP server
  'codegraph' (and '.basic-memory') initial connection failed (attempt N/3) …`
  followed by `failed initial connection after 3 attempts, parking until a
  reconnect is requested` (WARNING level, `unhandled errors in a TaskGroup`).
  Volume is high (~1,578 lines on 08-09, ~280 by 03:00 on 08-10, 1,026 total by
  03:00 on 08-11, 1,588 total by 03:00 on 08-12, 2,150 total by 03:00 on 08-13)
  — steady-state dominant errors.log class for seven nights running (08-10→08-16),
  not a one-off spike. **NEW 08-14: don't trust a single cumulative "N total by 03:00" number —
  `errors.log` ROTATES.** It rotated at **08-13 11:35** (the old 2 MB file is now
  `errors.log.1`; the live `errors.log` starts fresh at that timestamp), so the
  running "2,150-and-growing" counter reset to 0 mid-day 08-13. The durable signal
  is the **per-day park rate** (hundreds/day: the live file already holds 361 parks
  — 291 on 08-13 post-rotation + 70 in tonight's 02:53–02:57 08-14 bootstrap), NOT
  a monotonic total across files; count per-date (`grep 'parking until a reconnect'
  errors.log | grep -c 2026-08-DD`) and remember to add `errors.log.1` if you need
  a window that predates the rotation. It is **graceful degradation, not a crash**
  — the server "parks" and reconnects on the next request. **Directly confirmed
  self-healing six nights running (08-11 through 08-16)**: each
  nightly-maintenance session's own tool bootstrap parked BOTH servers at startup
  (last agent.log/errors.log lines — 03:00 on 08-11, 02:59 on 08-12, 02:53–02:58
  on 08-13, 02:53–02:57 on 08-14, 03:01 on 08-15, and 08-16 in TWO cycles at
  02:55 then a 03:00 self-probe revival — the 08-15 and 08-16 runs both logged an
  explicit `MCP server '<name>': attempting revival … rebuilding transport` INFO
  line between the park and the reconnect, on 08-16 for BOTH servers at 03:00:20/21),
  yet later in that same session
  `codegraph` and `basic-memory` both reconnected and their tools (`codegraph_explore`,
  `mcp__basic-memory__*`) became callable — so the park→reconnect contract is
  observed end-to-end, not just assumed, and is now reproduced six times, not a
  one-off. The **per-day park rate is steady** — the live post-rotation errors.log
  held **1,486 parks by 03:00 08-16** (291 on 08-13 post-rotation + 562 across the
  full 08-14 day + **561 across the full 08-15 day** + 72 in tonight's two-cycle
  08-16 bootstrap), i.e. ~561/day and flat (562→561 across 08-14→08-15), not
  accelerating. Don't
  read the line count as a crisis; it's the startup-race retry
  path. Only chase it if `hermes mcp list` shows a server actually disabled or a
  live tool call fails after the reconnect. (This class postdates the 08-09 03:03
  nightly reflection, which is why runbooks through 08-09 list "only Discord DNS
  noise" in errors.log; conversely the periodic Discord `gateway-*.discord.gg`
  liveness-probe DNS class has stayed **quiet since 08-11** — last real line
  08-10 21:56, 0 on 08-11 through 08-16 in the live errors.log — so errors.log is
  now essentially all MCP-parking noise. **Do not confuse that quiet probe class
  with the one-off 08-15 13:38 adapter-connect DNS failure** (`discord.com:443`
  unresolvable, 1 ERROR + traceback = 2 `ClientConnectorDNSError` grep hits) — a
  different code path (`hermes_plugins.discord_platform.adapter`, at gateway boot,
  not the periodic probe); see §"Restart & exit-diagnostics triage".)

## Stuck bot: the clarify-tool hang (2026-07-18 evening)

The agent may answer a question by calling its `clarify` tool, which blocks
the session waiting for a reply **in that same thread** — observed timeout
is 3600s. Symptoms: bot "read" the message but nothing happens for up to an
hour; agent.log later shows `tool clarify completed (3600.59s, ...)` and
`reason=interrupted_by_user`. Two exits:

- Answer the clarify question in the thread, or
- `/stop` in Discord — it invalidates the run generation and releases the
  session lock immediately (the tool still logs its completion at timeout;
  that trailing log line is harmless).

## Triage order for "the bot isn't answering"

1. `grep 'Agent error in session' -A 25 ~/.hermes/logs/gateway.log | tail -40`
   — config/model init errors surface here, not in Discord.
2. `curl -s http://localhost:11434/v1/models` — is Ollama up, what's served.
3. Check base_url scheme/path and `context_length` against the rules above.
4. If merely *slow*: check agent.log for `Preflight compression` (long
   thread) or a pending `clarify` call (see above) before restarting.
5. `tail ~/.hermes/logs/gateway-exit-diag.log` — restart loop vs clean exits.
