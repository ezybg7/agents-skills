---
name: hermes-local-gateway-ops
description: Operate and troubleshoot THIS machine's Hermes gateway (m4-mini,
  Discord, Ollama backend) — known failure modes, config hazards, and health
  checks. For general Hermes usage see the hermes-agent skill.
---
# Hermes gateway ops on the m4-mini

This deployment: Hermes gateway (Discord adapter, bot `orchestrator#5798`)
backed by a local Ollama server at `http://localhost:11434/v1`, model
`qwen3-agent` (a Qwen3-8B Modelfile build). Logs: `~/.hermes/logs/`
(agent.log, gateway.log, errors.log, gateway-exit-diag.log) and
`~/agents/logs/` (ollama.log/err, hermes.err, backup, mempressure).

## Hard constraint: model context ≥ 64K (live incident 2026-07-17/18)

Hermes refuses to init an agent whose model context is under 64,000 tokens:

    ValueError: Model qwen3-agent has a context window of 40,960 tokens,
    which is below the minimum 64,000 required by Hermes Agent.

- Qwen3-8B's *real* serving context on Ollama is 40,960. A Modelfile
  `PARAMETER num_ctx 65536` is silently clamped — Ollama has no
  rope-scaling/YaRN knob, confirmed via llama.cpp logs (`n_ctx_slot = 40960`).
- Setting `model.context_length: 40960` in config.yaml to "match reality"
  makes EVERY gateway message fail at agent init with the error above. The
  user sees only a generic 91-char error in Discord; the traceback is in
  gateway.log. Do not "fix" the config down to the true window if it is
  below 64K — that trades a truncation risk for a total outage.
- Fix paths: (a) switch to a model that truly serves ≥64K — `llama3.1:8b`
  (128K) was pulled 2026-07-18 for this; (b) use a pre-baked YaRN
  long-context GGUF of Qwen3; (c) only set `context_length` ≥ 64K if the
  server genuinely serves it. After changing config: restart gateway and
  send a test DM; verify no `Agent error in session` in gateway.log.

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
  `curl -s http://localhost:11434/v1/models`.
- **`/restart` from Discord** → clean teardown then `SystemExit: 75` in
  gateway-exit-diag.log; the wrapper restarts the process. Exit code 75 is
  the restart contract, not a crash.
- **Log noise**: repeated `openrouter unhealthy (payment / credit error)`,
  `Nous client unavailable`, and `check_fn ... returned False` warnings are
  expected — those aux providers/tools are unconfigured here. The security
  audit's SSH `PasswordAuthentication` warning is a known open item.

## Triage order for "the bot isn't answering"

1. `grep 'Agent error in session' -A 25 ~/.hermes/logs/gateway.log | tail -40`
   — config/model init errors surface here, not in Discord.
2. `curl -s http://localhost:11434/v1/models` — is Ollama up, what's served.
3. Check base_url scheme/path and `context_length` against the rules above.
4. `tail ~/.hermes/logs/gateway-exit-diag.log` — restart loop vs clean exits.
