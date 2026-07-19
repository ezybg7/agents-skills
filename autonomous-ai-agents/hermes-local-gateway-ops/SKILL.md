---
name: hermes-local-gateway-ops
description: Operate and troubleshoot THIS machine's Hermes gateway (m4-mini,
  Discord, Ollama backend) — known failure modes, config hazards, and health
  checks. For general Hermes usage see the hermes-agent skill.
---
# Hermes gateway ops on the m4-mini

This deployment: Hermes gateway (Discord adapter, bot `orchestrator#5798`)
backed by a local Ollama server at `http://localhost:11434/v1`, model
`qwen3-agent-128k` — an unsloth Qwen3-8B-128K GGUF (honest 131K context
metadata) built with the original qwen3-agent chat template and
`num_ctx 65536`, kept warm permanently (~10 GB resident, keep-alive forever).
Role (Everett's decision 2026-07-18): the local 8B is a **relay + delegate
orchestrator only** — it routes work to Claude Code via the task queue (see
delegate-to-claude) and must not code or author skills itself. Logs:
`~/.hermes/logs/` (agent.log, gateway.log, errors.log, gateway-exit-diag.log)
and `~/agents/logs/` (ollama.log/err, hermes.err, backup, mempressure).

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
