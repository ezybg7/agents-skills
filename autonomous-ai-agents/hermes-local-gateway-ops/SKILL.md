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
  **NEW 2026-08-20 — this blip RECURS on restart; it is NOT a one-off.** After the
  08-15 pid-731 event stayed quiet 4 nights, TWO more `gateway.start`s fired on
  08-20 afternoon — **pid 728 @ 13:48:41 local (17:48:41 UTC)** and **pid 725 @
  14:25:17 local (18:25:17 UTC)** (exit-diag `gateway.start` total 28→30) — and
  **each hit the same `discord.com:443` `ClientConnectorDNSError` at boot** (live
  errors.log ERROR lines 13:48:44, 14:25:19, 14:25:49; live `ClientConnectorDNSError`
  grep count rose 2→6). Both degraded gracefully exactly as the 08-15 model predicts:
  the pid-725 boot logged `Reconnect discord failed, next retry in 60s` → retried →
  `[Discord] Connected as orchestrator#5798` → `✓ discord reconnected successfully`
  at **14:27:15**, ~2 min after boot. So treat the boot-time adapter DNS failure as
  an **expected transient on every (re)start**, self-healing within a few minutes;
  it is not tied to a single 08-15 cold start. (agent.log confirms the recovery:
  normal `discord.gateway: … successfully RESUMED session` keepalives resume
  08-20 21:13 → 08-21 02:11.)
  **NEW 2026-08-22 — the blip ALSO recurs with NO gateway restart (a mid-run
  reconnect), not only on (re)start.** At **08-21 04:16–04:22** the adapter hit the
  same `discord.com:443` `ClientConnectorDNSError` while the SAME gateway (pid 725,
  up since 08-20 14:25) kept running — exit-diag shows **no new `gateway.start`**
  (total held at **30**, last still pid 725), so this was NOT a restart. It began as
  a **liveness-probe failure** — agent.log `[Discord] Discord liveness probe failed
  (1/3): Cannot connect to host discord.com:443` at 04:16:46 — which tripped
  `discord.client: Attempting a reconnect in …` back-offs, then gateway.log
  `Reconnecting discord (attempt 3/4)` with `Reconnect discord failed, next retry in
  120s`, self-healing to `[Discord] Connected as orchestrator#5798` + `✓ discord
  reconnected successfully` at **04:22:36** (~6 min). It landed right after the daily
  ~04:00 session reset (`session_reset … at_hour 4`). So generalize the rule: the
  `discord.com:443` adapter DNS failure is a **transient on ANY (re)connect —
  gateway restart OR a mid-run liveness-probe reconnect** — and self-heals within a
  few minutes via the reconnection watcher; a `gateway.start` is NOT a prerequisite.
  This single 04:20:33 ERROR + traceback is also the **only** write to the live
  `errors.log` since 08-20 14:25 (MCP-parking has added nothing — see §"Behavior
  that is normal").
  **NEW 2026-08-28 — a DISTINCT Discord failure signature: a gateway WEBSOCKET 503,
  not the adapter DNS blip.** The ~143 h errors.log silence (08-21 04:20 → 08-27,
  reported by the 08-27 nightly) **ended at 08-27 05:20:16** with exactly ONE new
  event (errors.log by-date count for 08-27 == 1): `ERROR discord.client: Attempting
  a reconnect in 0.87s`, whose traceback is
  `aiohttp.client_exceptions.WSServerHandshakeError: 503, message='Invalid response
  status', url='wss://gateway-us-east1-d.discord.gg/?v=10&encoding=json&compress=zlib-stream'`.
  This is a **different code path and failure mode** from every prior Discord error
  in this runbook: it is the **Discord gateway websocket handshake being 503'd by
  Discord's edge** (server-side "high demand"/transient rejection on the `discord.py`
  `discord.client` layer), NOT the `hermes_plugins.discord_platform.adapter`
  `discord.com:443` `ClientConnectorDNSError` DNS-resolution class (§ above) and NOT
  the periodic `gateway-*.discord.gg` liveness-probe DNS class. It **self-healed
  within pid 725 in ~8 s and required no restart** — `discord.py`'s own reconnect
  backoff fired (`reconnect in 0.87s`), the shard re-handshook, and gateway.log logged
  `[Discord] Connected as orchestrator#5798` at **05:20:24** (`gateway.start` still
  **30**, pid 725, so no `gateway.exit_nonzero`/restart), after which agent.log resumed
  its normal `successfully RESUMED session` keepalives. Treat a Discord gateway
  `WSServerHandshakeError: 503` like the transient Gemini 503 (§"Gemini free-tier
  limits") — `discord.py` retries it automatically and it recovers in seconds; only
  worry if the reconnect backoff never lands `Connected as orchestrator#5798`. Note it
  did NOT bring back MCP-parking (that loop is tied to the MCP transports / a
  `gateway.start`, not a Discord shard resume — last park still 08-20 13:32; see
  §"Behavior that is normal"), so it does not resolve the still-open post-restart
  parking-return watch.

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
- **Cadence is ~weekly, confirmed through 08-28 (`run_count=6`).** Observed runs:
  07-24 (`run_count=1`), 07-31 (2), 08-07 (3), 08-14 18:22 (4), 08-21 14:27 (5),
  **08-28 18:44:27 local / 22:44 UTC (6)** — each ~7 days apart, held a **sixth**
  consecutive point (08-21 → 08-28 = exactly 7 days), all in the early-afternoon-to-
  evening slot, i.e. *after* the 03:00 nightly (which is why the run for a given
  ~Thursday is only observable on the *next* nightly). **next run due ~09-04.** An
  unchanged `.curator_state` mtime between those dates is expected, not a stall. State
  lives at `~/agents/skills/.curator_state` (gitignored).
- **NEW 2026-08-22 — the 08-21 run is the FIRST-ever non-"no changes" run: `auto: 2
  marked stale`.** Runs 1–4 were all `auto: no changes`; the 08-21 run (`run_count=5`,
  0.42s, still `llm: skipped (consolidation off)`, 0 tokens) checked 72 and did its
  first real auto-transition — **2 skills active→stale, 0 archived, 0 reactivated**.
  `run.json` doesn't name them but `.usage.json` does (`state: "stale"`): **`claude-code`**
  (last invoked 2026-07-18) and **`hermes-agent`** (last invoked 2026-07-19) — both
  **product-reference** skills ~34 days idle, both `pinned: false`, neither
  nightly-maintained, so this is benign and needs no action (stale ≠ archived; the
  time-to-archive threshold is longer, and archive is reversible). But it is the
  **first live proof of the invocation-driven staleness mechanism** this section warns
  about: staleness is driven by skill *invocation*, not file edits, so a maintained-but-
  never-invoked skill really does age toward stale. **Watch item:** of the three
  nightly-maintained skills, only `hermes-local-gateway-ops` is in `.usage.json` (still
  `active`, last_used 08-19 — kept fresh only because the nightly reads it), and it is
  **`pinned: false`**; `nightly-maintenance` and `claude-worker-env` aren't in the usage
  sidecar at all. None are stale yet, but if a maintained skill ever appears in the
  stale set, `hermes curator pin <name>` (the CLI is likely worker-gated — flag it for
  Everett) before it can reach `archive_after_days`.
- **NEW 2026-08-29 — the projected ~08-28 6th run FIRED, and it jumped `auto: 2 marked
  stale` → `auto: 70 marked stale`.** After six nightlies flagging it as "the imminent
  axis," the run landed **08-28 18:44:27 local** (`run_count` 5→6, 0.64s, still `llm:
  skipped (consolidation off)`, 0 tokens; `run.json` `marked_stale:70, archived:0,
  reactivated:0, checked:72`). The 2→70 jump is **not a mechanism change** — the 70
  newly-stale skills are *exactly the never-invoked 07-24 seed cohort*: all 70 share
  `created_at` 2026-07-24 with `last_used_at: null` in `.usage.json`, so a whole
  same-age batch crossed the staleness line together in one weekly sweep (the 07-24
  seed + ~35 days ≈ 08-28). Still benign: **0 archived** (stale ≠ archived; archive
  threshold is longer and reversible), consolidation off so it's only a label.
  - **Watch-item from 08-22 did NOT trip — no nightly-maintained skill went stale.**
    `.usage.json` now holds only **2 `active`** skills: **`hermes-local-gateway-ops`**
    (this skill, `last_used` 08-19, kept fresh because the nightly *reads* it — still
    `pinned: false`) and **`delegate-to-claude`**. `nightly-maintenance` and
    `claude-worker-env` are **still absent from the sidecar entirely**, so they can't
    be marked stale (immune by absence). So the maintained set is safe this run.
  - **But correct the over-clean "invocation-age → stale" model: the boundary is NOT a
    simple fixed-days-from-`last_used` cutoff.** `delegate-to-claude` (`last_used`
    **2026-07-20**, ~39 days idle at the 08-28 run) is **active**, while `claude-code`
    (07-18) and `hermes-agent` (07-19) — only **1–2 days older** — were marked stale
    back on 08-21. A pure last_used-age rule can't split 07-18/07-19 (stale) from 07-20
    (active) while *also* staling the 07-24 cohort. So either the auto-pass doesn't
    re-evaluate already-`active` skills on the same clock as it seeds new stales, or
    there's an activity signal beyond the four sidecar timestamps (all of
    `delegate-to-claude`'s are 07-20). **Left as an open anomaly — do not fabricate the
    exact threshold.** The durable, verified facts: (a) the 07-24 null-`last_used`
    cohort staled as a batch; (b) maintained skills are safe *this* run; (c)
    `hermes-local-gateway-ops` is `pinned: false` and ages on *invocation*, not on the
    nightly's file-reads (its `last_used` is stuck at 08-19), so if it ever appears in
    the stale set, `hermes curator pin hermes-local-gateway-ops` (CLI likely
    worker-gated → flag for Everett) before it can reach `archive_after_days`.
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
  — steady-state dominant errors.log class for eleven nights running (08-10→08-20),
  not a one-off spike. **NEW 08-14: don't trust a single cumulative "N total by 03:00" number —
  `errors.log` ROTATES, and it has now rotated TWICE** (08-13 11:35 → the old file became
  `errors.log.1`; then again **08-18 11:15:32** → that file became `errors.log.1` and the
  08-13 one aged to `errors.log.2`). The live `errors.log` currently starts at **08-18 11:15:36**,
  so any cumulative counter resets at each rotation. The durable signal
  is the **per-day park rate**, NOT a monotonic total across files; count per-date
  (`grep 'parking until a reconnect' errors.log | grep -c 2026-08-DD`) and add the
  right rotated file for a full day that straddles a rotation — e.g. **full-day 08-18 = 562**
  = 263 (in `errors.log.1`, before the 11:15 roll) + 299 (in the live file, after it).
  **Two live-file metrics dropped to 0 tonight (08-19) purely as rotation artifacts, not signal:**
  the cumulative park total (reset by the 08-18 roll) and the `ClientConnectorDNSError` count
  (the 08-15 traceback body moved into `errors.log.1`) — check the rotated files before reading
  either "0" as a change. It is **graceful degradation, not a crash**
  — the server "parks" and reconnects on the next request. **Directly confirmed
  self-healing ten nights running (08-11 through 08-20)**: each
  nightly-maintenance session sees BOTH servers park and its own explicit tool
  calls reconnect them (`codegraph_explore` / `mcp__basic-memory__*` become
  callable later in the same run) — the park→reconnect contract observed
  end-to-end, not assumed, reproduced ten times.
  **NEW 08-19 — the park is a PERIODIC ~5-min self-probe cycle, not a startup burst,
  and this corrects the 08-18 note.** Counting a full day shows a park PAIR (codegraph
  then basic-memory, ~4s apart) every ~5 minutes all day long (tonight: 00:03, 00:08,
  00:13 … 02:52, 02:57 — 35 cycles × 2 = 70 by 02:57); the "N in tonight's 02:5x bootstrap"
  framing of earlier notes was just the tail of that cycle visible in the log's last lines,
  not a distinct startup event. Each cycle logs an `MCP server '<name>': attempting revival
  after initial connection failures (self-probe or explicit reconnect request); rebuilding
  transport` line — but that line is **INFO-level, so it lands in `agent.log`, NOT `errors.log`**
  (errors.log is WARNING+, i.e. parks only). That is why last night's errors.log-only check
  wrongly called 08-18 "a plain park→reconnect with no revival INFO line": **08-18 in fact had
  562 revival INFO lines in agent.log** — exactly one per park (park count == revival count each
  day: 562==562 on 08-18, 70==70 so far on 08-19). Because it is a fixed-period timer (≈288
  slots/day × 2 servers ≈ 576 max), the per-day total is **flat by construction** (~562/day, the
  ~2.5% shortfall is occasional missed slots), which is the real reason the rate never accelerates.
  The periodic self-probe keeps failing+re-parking (the gateway's own probe can't reach the
  servers), but an **explicit tool call** in a live session does reconnect — hence "reconnects on
  demand." The **per-day park rate is steady and flat an eleventh night** —
  562 (08-14) → 561 (08-15) → 562 (08-16) → 564 (08-17) → **562 (08-18, = 263 in `errors.log.1`
  + 299 in the live file)** then **562 (08-19)** confirmed full-day, with **70 so far
  in tonight's 08-20 cycle by 02:57** (last live errors.log lines are the `codegraph`
  02:57:02 + `basic-memory` 02:57:06 08-20 parks). **08-19's full day now confirms the
  timer model end-to-end**: 562 parks in errors.log == 562 `attempting revival` INFO lines
  in agent.log, exactly the per-park pairing the periodic-cycle reframe predicted. Not
  accelerating (see the timer explanation above). Don't
  read the line count as a crisis; it's the periodic self-probe retry
  path. Only chase it if `hermes mcp list` shows a server actually disabled or a
  live tool call fails after the reconnect. (This class postdates the 08-09 03:03
  nightly reflection, which is why runbooks through 08-09 list "only Discord DNS
  noise" in errors.log; conversely the periodic Discord `gateway-*.discord.gg`
  liveness-probe DNS class has stayed **quiet since 08-11** — last real line
  08-10 21:56, 0 on 08-11 through 08-20 — so errors.log is
  now essentially all MCP-parking noise. **Do not confuse that quiet probe class
  with the one-off 08-15 13:38 adapter-connect DNS failure** (`discord.com:443`
  unresolvable, 1 ERROR + traceback = 2 `ClientConnectorDNSError` grep hits) — a
  different code path (`hermes_plugins.discord_platform.adapter`, at gateway boot,
  not the periodic probe); see §"Restart & exit-diagnostics triage". **That 08-15
  adapter DNS failure has NOT recurred:** exit-diag shows no new `gateway.start`
  after the 08-15 17:38 UTC pid-731 one through 08-20 (still 28 starts total, last is
  pid 731), so it stays a one-off boot blip — confirmed quiet a **fourth** night now
  (08-17, 08-18, 08-19, 08-20). Caveat: the live errors.log `ClientConnectorDNSError` count is
  **0 as of 08-20 only because the 08-18 11:15 rotation moved that traceback into
  `errors.log.1`** — it is a rotation artifact, not fresh confirmation; grep the rotated
  file to see the original 08-15 event.)
  **NEW 2026-08-20/21 — the flat ~562/day MCP-parking era ENDED; the periodic self-probe
  cycle stopped and has not resumed.** The last park is **08-20 13:32:11** (`basic-memory`)
  and the last `attempting revival` INFO line is **08-20 13:32:04** — both cease together,
  once more confirming the park==revival pairing (08-20 got **318** of each before stopping,
  a partial day, not the full ~562, precisely because the cycle halted at 13:32). Since then:
  **0 parks and 0 revival lines** from 08-20 13:32 through 08-21 03:00+ (the old ~5-min cadence
  would have logged ~160 in that 13.5 h window), and the live `errors.log` has had **no writes
  at all since 08-20 14:25**. Yet the MCP servers are plainly healthy — the `mcp__codegraph__*`
  / `mcp__basic-memory__*` tools surfaced and were callable in tonight's 08-21 session. The halt
  coincides with the two 08-20 gateway restarts (pid 728 @ 13:48, pid 725 @ 14:25; see §"Restart
  & exit-diagnostics triage"): **the current gateway (pid 725) simply keeps the MCP transports
  connected, so the self-probe→park→revive loop no longer fires.** Operational takeaway: an
  **empty** park stream is now the healthy state, not a silent failure — verify via a live tool
  call (which works) or `hermes mcp list`, not by expecting the old ~562/day WARNING volume. This
  also means the "in-session self-heal reproduced N nights running" streak has a clean terminus:
  tonight there was nothing to self-heal because nothing parked. Watch whether parking stays gone
  across the next restart, or whether it returns to the timer-driven flat rate.)
  **ROLLING 2026-08-21 → 2026-08-30 — the empty-park-stream era is holding (consolidated from the
  per-night CONFIRMED ledger, 08-22…08-29, which had grown to one near-identical paragraph per night;
  collapsed on the 2026-08-30 nightly — no durable fact dropped, every distinct event is in the two
  sections cross-referenced below).** Parking has stayed gone **ten consecutive nights (08-21 through
  08-30, all 0 parks)**; the last park of any kind is still **08-20 13:32:11** (`basic-memory`), and the
  MCP self-probe→park→revive loop stays **dormant by design** — the current gateway (**pid 725**, up
  since 08-20 14:25 local / exit-diag `gateway.start` held at **30**, no new restart in ~9.5 days) keeps
  the codegraph/basic-memory transports connected, so the ~5-min timer never fires. **So "empty park
  stream = healthy" is the steady state** — verify via a live tool call (`mcp__codegraph__*` /
  `mcp__basic-memory__*` surface each session; the call itself is worker-sandbox permission-gated) or
  `hermes mcp list`, **never by the old ~562/day WARNING volume**. Across this whole 10-night window the
  live `errors.log` took only **two** writes, **neither a park**, both a *distinct* Discord signature and
  both self-healed inside pid 725 with no restart (full detail in §"Restart & exit-diagnostics triage"):
  the single **08-21 04:20:33** adapter `discord.com:443` `ClientConnectorDNSError` DNS blip, and the
  single **08-27 05:20:16** gateway `WSServerHandshakeError: 503`. The WS-503 did **not** recur — **0
  writes dated 08-28 / 08-29 / 08-30** — so errors.log has been quiet ~70 h again (08-27 05:20 → 08-30
  03:00) with that WS-503 still its last line, and agent.log `discord.gateway: … successfully RESUMED
  session` keepalives run right through **08-30 01:57:36**. (The per-night "silent for N h / mtime
  frozen" shortcut earlier nightlies used is **retired** — errors.log now carries those two self-heal
  writes, so read liveness from keepalives + a live tool call, not from file mtime.) **Still-open watch
  (unchanged all ten nights):** does parking *return* after the next restart? No `gateway.start` since
  pid 725 came up 08-20 14:25 (~9.5 d), and neither the 08-21 DNS blip nor the 08-27 WS-503 was a
  restart (both were in-place reconnects / shard resumes that did not re-test the MCP transports), so a
  genuinely-silent stream still can't be distinguished from a would-be-silent-anyway one until a real
  restart re-tests them. Curator is no longer the imminent axis — it fired 08-28 18:44 (`run_count`
  5→6, `auto: 70 marked stale`), next ~09-04 (see §"Curator").

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
