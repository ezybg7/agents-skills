---
name: nightly-maintenance
description: The three-part nightly maintenance routine on the m4-mini (SKILLS
  branch, MEMORY archival, reflection note) that runs as the queued
  `reflect-<date>` job at 03:00. The conventions here are otherwise re-derived
  every night by reading four old reflection logs. Read at the start of any
  nightly-maintenance run.
---
# Nightly maintenance on the m4-mini

The 03:00 `reflect-<date>` queued job (runs through `claude-worker` — see
`claude-worker-env` for the shell sandbox) performs three tasks defined in the
nightly prompt. Every night's session otherwise reconstructs these conventions
by `jq`-ing the previous four reflection JSONs; they are collected here so a
fresh session can act instead of re-derive. `<date>` and "today" come from the
task prompt, not the clock.

## Task 1 — SKILLS (branch, don't merge)

- **Branch `nightly-<date>` off the PREVIOUS night's branch, NOT `main`.** The
  nightly branches **chain**: each is an ancestor of the next, so the whole
  history accumulates on one line off `main` and grows ~1–2 commits/night, **all
  unmerged**. The absolute count drifts, so check it live with
  `git -C ~/agents/skills rev-list --count main..HEAD` rather than trusting a
  number written here (it was **25** as of 07-26 — not the "23" this line first
  claimed; corrected on 07-27, the runbook's first live use). Everett reviews and
  merges; you NEVER merge and NEVER open a PR for these.
  - `git -C ~/agents/skills switch -c nightly-<date>` (the current HEAD is the
    latest nightly, so a plain branch-off is correct). Verify chaining with
    `git -C ~/agents/skills merge-base --is-ancestor nightly-<yesterday> nightly-<date>`.
- **Mine only genuinely-fresh material.** Sources:
  - `jq -r '.result' ~/agents/logs/claude-reflect-<date>-*.json` — the recent
    daily reflections (these session-result JSONs hold the distilled text in
    `.result`; today's own is 0 bytes until this job finishes).
  - `~/agents/logs/worker-runner.log` — did any NEW delegated worker session run
    since the last nightly? (look past the last `done (...)` line).
  - `~/.hermes/logs/errors.log`, `gateway.log`, `~/agents/logs/{mempressure,ollama}.log`,
    and curator state (`~/agents/skills/.curator_state` mtime) for infra events.
- **Idle days are normal and frequent** (07-22/23/24/26/27/28/29/30/31, 08-01/02/03/04/05/06/07/08/09/10/11/12/13/14/15/16/17/18 and 08-19 were all idle for
  the SKILLS task: no new worker session since the last nightly — worker-runner.log
  has only lock-exit noise past `done (nightly-pull-routine)` on 07-23; on 08-17 the only new
  `claude-*.json` is tonight's own 0-byte `reflect-2026-08-17` — and infra
  logs routine EXCEPT one genuinely new class (see below): the Discord DNS offline-probe
  noise (`ClientConnectorDNSError: gateway-*.discord.gg` — the "frozen at 08-03" claim
  in prior runbooks was stale) has itself stayed quiet since 08-11, so errors.log now appends
  almost entirely the MCP-parking class; agent.log's tail is likewise no longer Discord
  `RESUMED session` noise but tonight's own 02:53–02:58 MCP-parking bootstrap lines, curator last run 08-07 18:04
  (`auto: no changes; llm: skipped`, run_count 3 = 07-24/07-31/08-07 — a weekly cadence, so the next
  run is due ~08-14; unchanged tonight is expected, not stalled).
  **NEW on 08-10, followed up 08-11** (SKILLS-idle-but-real-finding, like 07-29/07-31): errors.log picked up a high-volume
  MCP-server class — `codegraph`+`basic-memory` `initial connection failed … parking until a reconnect
  is requested` (WARNING, ~1,578 lines 08-09 + ~280 by 03:00 08-10), **first seen 08-09 05:44** (i.e.
  AFTER the 08-09 03:03 reflection, which is why last night's log truthfully said "only Discord DNS noise").
  It is graceful degradation — the server parks and reconnects on demand, both come up in live sessions —
  so it's log noise, not a crisis; recorded 08-10 in `hermes-local-gateway-ops` §"Behavior that is normal".
  **08-11 refined that entry** with two verifiable facts: (a) the class is now the *steady-state dominant*
  errors.log class (1,026 total parks by 03:00 08-11, 72 that day) not a one-off spike, and the Discord DNS
  class went quiet (last line 08-10 21:56, 0 on 08-11); (b) the park→reconnect contract was confirmed
  end-to-end *inside the 08-11 nightly session itself* — its own bootstrap parked both servers at 03:00 (last
  agent.log lines), yet both reconnected and their tools became callable later in the same run.
  **08-12 refined it once more** (same shape, now reproduced): parks reached **1,588 total by 03:00 08-12**
  (563 across the full 08-11 day, 71 in tonight's 02:59 bootstrap) — dominant a *third* night running; the
  Discord DNS class stayed quiet (0 on both 08-11 and 08-12); and the in-session self-heal was **reproduced a
  second consecutive night** — tonight's own bootstrap parked both servers at 02:59, yet `codegraph` and
  `basic-memory` both reconnected and became callable within the same run, so the contract is now observed
  twice, not a one-off.
  **08-13 refined it again** (same shape, fourth night): parks reached **2,150 total by 03:00 08-13**
  (563 across the full 08-12 day, 70 in tonight's 02:53–02:58 bootstrap) — dominant a *fourth* night running; the
  Discord DNS class stayed quiet (0 on 08-11, 08-12 and 08-13); and the in-session self-heal was **reproduced a
  third consecutive night** — tonight's own bootstrap parked both servers at 02:53–02:58 (last errors.log lines
  are `basic-memory` + `codegraph` parks), yet both reconnected and their tools (`codegraph_explore`,
  `basic-memory`) became callable within the same run, so the contract is now observed three times, not a
  one-off. Still noise, not a fault.
  **08-14 refined it once more with a rotation caveat** (fifth night dominant, self-heal fourth): the key new
  fact is that **`errors.log` ROTATES** — it rolled at **08-13 11:35** (old 2 MB file → `errors.log.1`; the live
  file restarts there), so the runbook's growing "2,150 total by 03:00" counter reset to 0 mid-day 08-13 and is
  **not** comparable across the rotation. Track the **per-day park rate** instead (the live file already holds 361
  parks — 291 on 08-13 post-rotation + 70 in tonight's 02:53–02:57 08-14 bootstrap); add `errors.log.1` only for a
  pre-rotation window. Discord DNS class stayed 0 (08-11 through 08-14). Self-heal was **reproduced a fourth
  consecutive night** — tonight's own bootstrap parked both servers at 02:53–02:57 (last errors.log/agent.log lines
  are `basic-memory` parks), yet `codegraph` and `basic-memory` both reconnected and their tools became callable
  this run (the `mcp__codegraph__*` / `mcp__basic-memory__*` deferred tools surfaced). Recorded in
  `hermes-local-gateway-ops` §"Behavior that is normal".
  **08-15 refined it once more** (sixth night dominant, self-heal fifth) **and landed a curator data-point**: the live
  post-rotation `errors.log` now holds **925 parks** — 291 (08-13 post-rotation) + **562 across the full 08-14 day** + 72
  in tonight's 03:01 08-15 bootstrap — so the per-day rate is steady (**~562/day on 08-14**), MCP-parking is the dominant
  errors.log class a *sixth* night, and the Discord DNS class stayed 0 (08-11 through 08-15). Self-heal was **reproduced a
  fifth consecutive night** — tonight's own 03:01 bootstrap parked both servers (last errors.log/agent.log lines are the
  08-15 03:01 `codegraph`+`basic-memory` parks, incl. an explicit `attempting revival … rebuilding transport` INFO line),
  yet both reconnected and their `mcp__codegraph__*` / `mcp__basic-memory__*` tools surfaced this run. **NEW genuine fact —
  the curator's projected run happened:** it ran **08-14 18:22 (`run_count` 3→4, `auto: no changes; llm: skipped`)**, exactly
  the ~08-14 the 08-10 note projected from the weekly cadence (07-24 / 07-31 / 08-07 / 08-14) — a fourth data-point
  confirming the 7-day rhythm; next run due ~08-21. Recorded in `hermes-local-gateway-ops` §"Behavior that is normal" + §"Curator".
  **08-16 refined it once more** (seventh night dominant, self-heal sixth) **and surfaced a genuinely new
  gateway finding that is NOT MCP-parking:** the live post-rotation `errors.log` holds **1,486 parks by 03:00
  08-16** and the per-day rate is now *flat* (562 on 08-14, **561 on 08-15**, 72 in tonight's two-cycle 02:55+03:00
  bootstrap) — dominant a *seventh* night, not accelerating; self-heal was **reproduced a sixth consecutive night**
  (tonight's bootstrap parked both servers at 02:55, a 03:00 self-probe logged explicit `attempting revival …
  rebuilding transport` INFO lines for BOTH servers then re-parked, yet `mcp__codegraph__*`/`mcp__basic-memory__*`
  surfaced this run). The new fact: a **08-15 13:38 gateway restart** (`gateway.start` pid 731 — first exit-diag
  start since 07-20, effectively a cold start) hit a **transient Discord-adapter DNS failure** (`discord.com:443`
  unresolvable, 1 ERROR+traceback = 2 `ClientConnectorDNSError` hits — a *different* path from the periodic
  `gateway-*.discord.gg` probe class, which stays 0 in the live errors.log) and **degraded gracefully to cron-only**
  (`Gateway will continue for cron job execution`, Discord queued for retry via a reconnection watcher) — which is
  *why tonight's 03:00 cron still ran* despite Discord being initially disconnected. Recorded in
  `hermes-local-gateway-ops` §"Restart & exit-diagnostics triage" + §"Behavior that is normal". Curator unchanged
  (run_count=4, 08-14 18:22; next due ~08-21).
  **08-17 confirmed the flat rate an eighth night and closed the loop on the 08-15 blip:** the live post-rotation
  `errors.log` holds **2,048 parks by 02:59 08-17** and the per-day rate is *still flat* — 562 (08-14), 561 (08-15),
  **562 (08-16)**, 72 in tonight's 02:59 bootstrap — MCP-parking dominant an *eighth* night, not accelerating;
  self-heal was **reproduced a seventh consecutive night** (tonight's 02:59 bootstrap parked both servers — last
  errors.log lines are the `codegraph` 02:59:35 + `basic-memory` 02:59:41 08-17 parks — yet `mcp__codegraph__*`
  /`mcp__basic-memory__*` surfaced this run). The genuinely new *negative* fact: the **08-15 13:38 adapter DNS
  failure has NOT recurred** — exit-diag shows no new `gateway.start` after the 08-15 17:38 UTC pid-731 one through
  08-17, so that boot blip stays a one-off (the 2 `ClientConnectorDNSError` grep hits in the live errors.log are
  still that single event's traceback body, not a fresh failure), and the periodic Discord probe class stayed 0
  (08-11 through 08-17). Curator unchanged (run_count=4, 08-14 18:22; next due ~08-21). Recorded in
  `hermes-local-gateway-ops` §"Behavior that is normal" + §"Restart & exit-diagnostics triage".
  **08-18 confirmed the flat rate a ninth night and the 08-15 blip quiet a second night:** the live post-rotation
  `errors.log` holds **2,610 parks by 02:58 08-18** and the per-day rate is *still flat* — 562 (08-14), 561 (08-15),
  562 (08-16), **564 (08-17)**, 70 in tonight's 02:48–02:58 three-cycle bootstrap — MCP-parking dominant a *ninth*
  night, not accelerating; self-heal was **reproduced an eighth consecutive night** (tonight's 02:48/02:53/02:58
  bootstrap parked both servers in three cycles — last errors.log lines are the `codegraph` 02:58:44 + `basic-memory`
  02:58:49 08-18 parks, this time a plain park→reconnect with NO `attempting revival` INFO line — yet
  `mcp__codegraph__*`/`mcp__basic-memory__*` surfaced this run). The 08-15 13:38 adapter DNS failure still has NOT
  recurred (no new `gateway.start` after the 08-15 pid-731 one through 08-18; the 2 live `ClientConnectorDNSError`
  hits are still that single event's traceback), and the periodic Discord probe class stayed 0 (08-11 through 08-18).
  Curator unchanged (run_count=4, 08-14 18:22; next due ~08-21). Recorded in `hermes-local-gateway-ops`
  §"Behavior that is normal".
  **08-19 confirmed the flat rate a tenth night AND reframed the whole park class + corrected the 08-18 note:**
  the biggest finding is that the MCP park is a **periodic ~5-min self-probe cycle**, not a startup burst — counting a
  full day shows a park PAIR (`codegraph` then `basic-memory`) every ~5 minutes from 00:03 onward (tonight 35 cycles ×
  2 = 70 by 02:57), and **each cycle emits an `attempting revival … rebuilding transport` INFO line that lands in
  `agent.log`, not `errors.log`** (errors.log is WARNING+). So park count **==** revival count each day (562==562 on
  08-18, 70==70 so far on 08-19), and last night's errors.log-only check was wrong to call 08-18 "a plain
  park→reconnect with NO revival INFO line" — **08-18 actually had 562 revival INFO lines in agent.log**. Because it's a
  fixed-period timer (~288 slots/day × 2 ≈ 576 max), the per-day total is flat *by construction* (~562/day), which is
  the real reason it never accelerates; self-heal is thus **reproduced a ninth consecutive night** (both servers park,
  explicit tool calls reconnect them, `mcp__codegraph__*`/`mcp__basic-memory__*` surfaced this run). Second genuine
  fact: **`errors.log` rotated a SECOND time (08-18 11:15:32)** — full-day 08-18 = **562** = 263 (`errors.log.1`,
  pre-11:15) + 299 (live file, post) — and two live-file metrics "dropped to 0" tonight purely as rotation artifacts
  (the cumulative park total; the `ClientConnectorDNSError` traceback, now in `errors.log.1`), NOT as change. The 08-15
  adapter DNS blip still has NOT recurred (still 28 `gateway.start` total, last pid 731; quiet a *third* night). Curator
  unchanged (run_count=4, 08-14 18:22; next ~08-21). Recorded in `hermes-local-gateway-ops` §"Behavior that is normal" +
  §"Restart & exit-diagnostics triage".
  (mem % and ollama `/v1/models` were **not re-probed on 08-04→10** — `vm_stat` and `curl localhost`
  are both sandbox-gated; the idle call rests on the worker-session + log-class evidence, which
  doesn't need them — earlier idle nights read ~74% free / ollama 200s.)) That's
  a **twenty-seven-night SKILLS-idle streak (07-24 through 08-19; last real worker session before it was
  07-23) that BROKE on 08-20** — the `jetson-orin-setup-plan` worker session ran 08-19 11:06 (a real
  delegated Claude session, `claude-jetson-orin-setup-plan-20260819-110610.json`, after the 08-19 03:00
  nightly), so tonight is genuinely non-idle (see the 08-20 clause below for the one verifiable new finding
  it produced). A long idle streak is itself the expected steady state here,
  not a sign something is broken; keep making one honest runbook refinement rather than inventing edits.
  Note "SKILLS-idle" is independent of the MEMORY task —
  **07-29 and 07-31 were both SKILLS-idle yet had a real fold** (see Task 2), while 07-30, 08-01, 08-02, 08-03,
  08-04, 08-05, 08-06, 08-07, 08-08 and 08-09 were idle on *both* (08-02's 07-25, 08-03's 07-26, 08-04's 07-27, 08-05's 07-28, 08-06's 07-29, 08-07's 07-30, 08-08's 07-31 and 08-09's 08-01 folds were all verified no-ops).
  **08-10 through 08-19 are all the inverse of the 07-29/31 case**: each had a verified-no-op MEMORY fold (08-10's 08-02 → archive; 08-11's 08-03 → archive; 08-12's 08-04 → archive; 08-13's 08-05 → archive; 08-14's 08-06 → archive; 08-15's 08-07 → archive; 08-16's 08-08 → archive; 08-17's 08-09 → archive; 08-18's 08-10 → archive; 08-19's 08-11 → archive) but a *non-empty* SKILLS side — 08-10 first captured the MCP-parking class, 08-11 refined it with the steady-state-dominant volume + the first in-session end-to-end reconnect confirmation, 08-12 refined it again with the third-night-dominant volume (1,588 total parks) + the *second consecutive* in-session self-heal, 08-13 refined it a fourth time (2,150 total parks, *third consecutive* self-heal), 08-14 added the rotation caveat (errors.log rolled 08-13 11:35 → track the per-day rate, not the cumulative total) + the *fourth consecutive* in-session self-heal, 08-15 confirmed the sixth-night-dominant per-day rate (562 parks on 08-14) + the *fifth consecutive* in-session self-heal + the curator's projected 08-14 run (run_count 3→4, weekly cadence held), 08-16 confirmed the *flat* per-day rate (561 on 08-15, 1,486 live total) + the *sixth consecutive* self-heal + surfaced a genuinely new non-parking finding (the 08-15 13:38 boot-time Discord-adapter DNS failure → cron-only graceful degradation, which is why the 03:00 cron still ran), 08-17 confirmed the rate flat an *eighth* night (562 on 08-16, 2,048 live parks by 02:59) + the *seventh consecutive* self-heal + closed the loop on that 08-15 finding as a one-off (no new `gateway.start` through 08-17, so the adapter DNS failure did not recur), 08-18 confirmed the rate flat a *ninth* night (564 on 08-17) + the *eighth consecutive* self-heal + the 08-15 blip quiet a second night, and 08-19 confirmed the rate flat a *tenth* night (562 on 08-18 = 263+299 across the second rotation) + the *ninth consecutive* self-heal + **reframed the class as a periodic ~5-min self-probe cycle** (park count == revival count; revival INFO lines live in agent.log, correcting the 08-18 "no revival line" note) + logged the second errors.log rotation (08-18 11:15) + the 08-15 blip quiet a third night. **08-20 BREAKS the streak (first non-idle SKILLS night since 07-23):** the `jetson-orin-setup-plan` worker session ran 08-19 11:06 — a real delegated session, not lock-exit noise — and although it used already-codified procedures it yielded one verifiable new fact: the python3 `gh`-spawn PR-create bridge opened pantry **PR #101** end-to-end (its FIRST proven success; both 07-21 sessions only described it and fell back to the idempotent-script pattern), which also pins the working `~/agents/tmp_<slug>_pr.py` helper location — recorded in `claude-worker-env` §"gh / GitHub from the worker". MCP-parking meanwhile held flat an *eleventh* night (562 on 08-19, 70 in tonight's 08-20 cycle by 02:57) with the *tenth consecutive* self-heal, and 08-19's full day now confirms the periodic-timer model end-to-end (562 parks == 562 `attempting revival` agent.log INFO lines) + the 08-15 DNS blip quiet a fourth night (still 28 `gateway.start`, last pid 731). So an idle worker-session count doesn't mean nothing to record; read the logs before declaring a pure no-op.
  **08-21 is back to SKILLS-idle on the worker-session axis** (the 08-19 jetson session was the last real `done`, already captured on 08-20; nothing new since) **but is again idle-but-real-finding — the biggest infra change in weeks.** The eleven-night flat ~562/day MCP-parking cycle **ENDED on 08-20 13:32** (last park + last `attempting revival` both at 13:32, 318==318 that partial day) and has **not resumed** — 0 parks/revivals and no errors.log writes at all from 08-20 14:25 through 08-21 03:00+, yet `mcp__codegraph__*`/`mcp__basic-memory__*` were callable this session. It coincides with **two 08-20 gateway restarts** (pid 728 @ 13:48, pid 725 @ 14:25; `gateway.start` 28→30), and the current pid-725 gateway keeps the MCP transports connected so the self-probe→park loop no longer fires — an **empty park stream is now the healthy state**. Second finding: those two restarts each hit the **`discord.com:443` adapter DNS blip at boot** (`ClientConnectorDNSError` grep 2→6), so that 08-15 blip **RECURS on restart, not a one-off**, and each self-healed to `✓ discord reconnected successfully` by 14:27:15. Both recorded in `hermes-local-gateway-ops` (§"Behavior that is normal" + §"Restart & exit-diagnostics triage"). Curator still unchanged (run_count=4, 08-14 18:22; the ~08-21 projected run hadn't fired by 03:00 — its usual slot is the afternoon, so check tomorrow). So an idle worker-session count doesn't mean nothing to record; read the logs before declaring a pure no-op.
  **08-22 is SKILLS-idle on the worker axis again but idle-but-real-finding for a third straight night — three verifiable findings, all in `hermes-local-gateway-ops` (1 commit + this runbook commit = 2 total).** Worker axis: the last real `done` is still the 08-19 jetson session (captured 08-20); worker-runner.log has only lock-exit / "no .task files" noise since, and the only new `claude-*.json` is tonight's own 0-byte `reflect-2026-08-22`. The three findings: (1) **the `discord.com:443` adapter DNS blip recurs with NO gateway restart** — it fired 08-21 04:16–04:22 as a *mid-run liveness-probe reconnect* (exit-diag `gateway.start` held at 30, pid 725; self-healed to `✓ discord reconnected` at 04:22:36), so last night's "recurs on restart" tightens to "transient on ANY (re)connect"; (2) **MCP-parking stayed gone a second night** (08-21=0 and 08-22=0 parks, still no new `gateway.start`, `mcp__*` tools callable — "empty park stream = healthy" holding, the post-restart-return watch still open because no restart has happened); (3) **the curator's projected ~08-21 run DID fire** (08-21 14:27, `run_count` 4→5, fifth weekly-cadence point) and is the **first-ever non-"no changes" run — `auto: 2 marked stale`** (`claude-code` + `hermes-agent`, both unpinned product-reference skills idle ~34 days, 0 archived) — first live proof of the invocation-driven staleness mechanism; the nightly-maintained skills are NOT stale but are unpinned (watch item). All recorded in `hermes-local-gateway-ops`. So a third consecutive idle-but-real-finding night: read the logs before declaring a pure no-op.
  **08-23 is SKILLS-idle on the worker axis a fourth straight quiet-infra night, but still not a pure no-op (1 skill commit + this runbook commit = 2 total).** Worker axis: the last real `done` is STILL the 08-19 jetson session (captured 08-20); worker-runner.log has only lock-exit / "no .task files" noise since, and the only new `claude-*.json` is tonight's own 0-byte `reflect-2026-08-23`. The one verifiable finding: **MCP-parking is gone a THIRD night (08-21/08-22/08-23 all 0 parks, last park still 08-20 13:32:11) and the live `errors.log` is now fully silent ~47 h** — the single 08-21 04:20:33 Discord-adapter DNS ERROR+traceback is still its only write since, so neither a park nor a DNS blip has landed across all of 08-22 and 08-23. Gateway pid 725 is still up (no new `gateway.start`; agent.log shows normal `discord.gateway … RESUMED session` keepalives through 08-23 01:26) and `mcp__codegraph__*`/`mcp__basic-memory__*` were callable this session, so "empty park stream + silent errors.log = healthy" is verified live a third night. The DNS blip did NOT recur on 08-22/08-23, but honestly that window had **no (re)connect event to test it** (pid stable, only DNS-cache-warm RESUMEs), so it's "nothing triggered it," not new evidence about the transient. Curator unchanged (run_count=5, 08-21 14:27; next ~08-28) — the post-restart-return parking watch stays open because no restart has happened. Recorded in `hermes-local-gateway-ops` §"Behavior that is normal". So a fourth consecutive quiet-but-not-empty night: read the logs before declaring a pure no-op.
  **08-24 is SKILLS-idle on the worker axis a fifth straight quiet-infra night, and again not a pure no-op (1 skill commit + this runbook commit = 2 total).** Worker axis: the last real `done` is STILL the 08-19 jetson session (captured 08-20); worker-runner.log shows only tonight's own `reflect-2026-08-24` processing past it, and that reflect JSON is 0 bytes until this job finishes. The one verifiable finding: **MCP-parking is gone a FOURTH night (08-21/08-22/08-23/08-24 all 0 parks, last park still 08-20 13:32:11) and the live `errors.log` STILL ends at the single 08-21 04:20:33 Discord-adapter DNS ERROR+traceback** — nothing has been appended for ~71 h (08-21 04:20 → 08-24 03:00), neither a park nor a DNS blip. Gateway pid 725 is still up (exit-diag `gateway.start` held at 30, no new restart) and `mcp__codegraph__*`/`mcp__basic-memory__*` surfaced this session (transport connected — the live call is worker-sandbox-gated, so "tools surfaced" is the liveness signal), so "empty park stream + silent errors.log = healthy" is verified live a fourth night. Curator unchanged (run_count=5, 08-21 14:27; next ~08-28). The post-restart parking-return watch stays open — no restart since pid 725 came up 08-20 14:25 — and the 08-21 DNS blip had no (re)connect event to re-test it this window, so its non-recurrence is "untested," not new evidence. Recorded in `hermes-local-gateway-ops` §"Behavior that is normal". A fifth consecutive quiet-but-not-empty night: read the logs before declaring a pure no-op.
  **08-25 is SKILLS-idle on the worker axis a SIXTH straight quiet-infra night, and still not a pure no-op (1 skill commit + this runbook commit = 2 total).** Worker axis: the last real `done` is STILL the 08-19 jetson session (captured 08-20); worker-runner.log shows only tonight's own `reflect-2026-08-25` processing past it (that reflect JSON is 0 bytes until this job finishes), everything else is lock-exit / "no .task files" noise. The one verifiable finding: **MCP-parking is gone a FIFTH night (08-21/08-22/08-23/08-24/08-25 all 0 parks, last park still 08-20 13:32:11) and the live `errors.log` STILL ends at the single 08-21 04:20:33 Discord-adapter DNS ERROR+traceback** — nothing appended for ~95 h (08-21 04:20 → 08-25 03:00), neither a park nor a DNS blip. Gateway pid 725 is still up (exit-diag `gateway.start` held at **30**, no new restart — pid 725 has now held ~4.5 days since 08-20 14:25) and `mcp__codegraph__*`/`mcp__basic-memory__*` surfaced this session + agent.log shows normal `RESUMED session` keepalives through 08-25 02:45, so "empty park stream + silent errors.log = healthy" is verified live a **fifth** night. Curator unchanged (run_count=5, 08-21 14:27) — **next due ~08-28, now ~3 days out, the nearest thing on any axis that could actually change**, so re-check `.curator_state` mtime the next few nights. The post-restart parking-return watch stays open (no restart since pid 725 came up 08-20 14:25) and the 08-21 DNS blip had no (re)connect event to re-test it this window, so its non-recurrence is "untested," not new evidence. Recorded in `hermes-local-gateway-ops` §"Behavior that is normal". A sixth consecutive quiet-but-not-empty night: read the logs before declaring a pure no-op.
  **08-26 is SKILLS-idle on the worker axis a SEVENTH straight quiet-infra night, and still not a pure no-op (1 skill commit + this runbook commit = 2 total).** Worker axis: the last real `done` is STILL the 08-19 jetson session (captured 08-20); worker-runner.log shows only lock-exit / "no .task files" noise past it and tonight's own 0-byte `reflect-2026-08-26` JSON. The one verifiable finding: **MCP-parking is gone a SIXTH night (08-21/08-22/08-23/08-24/08-25/08-26 all 0 parks, last park still 08-20 13:32:11) and the live `errors.log` STILL ends at the single 08-21 04:20:33 Discord-adapter DNS ERROR+traceback** — nothing appended for ~119 h (08-21 04:20 → 08-26 03:00), neither a park nor a DNS blip (the live-file mtime is itself frozen at 08-21 04:20, a cheap zero-writes check). Gateway pid 725 is still up (exit-diag `gateway.start` held at **30**, no new restart — pid 725 has now held ~5.5 days since 08-20 14:25), `mcp__codegraph__*`/`mcp__basic-memory__*` surfaced this session (transport connected — the live call is worker-sandbox-gated, so "tools surfaced" is the liveness signal), and agent.log `RESUMED session` keepalives run through 08-26 02:32, so "empty park stream + silent errors.log = healthy" is verified live a *sixth* night. Curator unchanged (run_count=5, 08-21 14:27; **next due ~08-28, now ~2 days out** — still the nearest thing on any axis that could actually change, so re-check `.curator_state` mtime the next two nights). The post-restart parking-return watch stays open (no restart since pid 725 came up 08-20 14:25) and the 08-21 DNS blip had no (re)connect event to re-test it this window, so its non-recurrence stays "untested," not new evidence. Recorded in `hermes-local-gateway-ops` §"Behavior that is normal". A seventh consecutive quiet-but-not-empty night: read the logs before declaring a pure no-op.
  **08-27 is SKILLS-idle on the worker axis an EIGHTH straight quiet-infra night (1 gateway-skill commit + this runbook commit = 2), but is emphatically NOT a pure no-op — because tonight the MEMORY task landed a REAL fold (see Task 2, the 08-19 jetson PR #101 — first non-no-op fold since 07-23).** Worker axis: the last real `done` is STILL the 08-19 jetson session (captured 08-20); worker-runner.log shows only lock-exit / "no .task files" noise past it and tonight's own 0-byte `reflect-2026-08-27`. The gateway finding: **MCP-parking is gone a SEVENTH night (08-21→08-27 all 0 parks, last park still 08-20 13:32:11) and the live `errors.log` STILL ends at the single 08-21 04:20:33 Discord-adapter DNS blip** — nothing appended for ~143 h (the live-file mtime is itself frozen at 08-21 04:20, a cheap zero-writes check). Gateway pid 725 is still up (`gateway.start` held at **30**, no restart — pid 725 has now held ~6.5 days since 08-20 14:25), `mcp__codegraph__*`/`mcp__basic-memory__*` surfaced this session, and agent.log `RESUMED session` keepalives run through 08-27 02:38 — so "empty park stream + silent errors.log = healthy" is verified live a *seventh* night. **Curator is now the imminent axis:** unchanged (run_count=5, 08-21 14:27) but **next due ~08-28, now ~1 day out** — a 6th run (likely another `auto: … stale`) is the one thing on any axis expected to change, so re-check `.curator_state` mtime/`run_count` on the 08-28 nightly. The post-restart parking-return watch stays open (no restart since pid 725 came up 08-20 14:25). Recorded in `hermes-local-gateway-ops` §"Behavior that is normal". So this is the night that proves the point: an eight-night quiet-infra streak on the SKILLS axis says nothing about the MEMORY axis — walk each `##` section of the archived log before declaring a pure no-op, and a still-open PR in its project section is exactly what you'll find.
  **08-28 is SKILLS-idle on the worker axis a NINTH straight quiet-infra night (1 gateway-skill commit + this runbook commit = 2), but is again idle-but-real-finding — the first genuinely NEW infra event since the 08-20 restarts.** Worker axis: the last real `done` is STILL the 08-19 jetson session (captured 08-20); worker-runner.log shows only lock-exit / "no .task files" noise past it and tonight's own 0-byte `reflect-2026-08-28`. The finding: **the ~143 h "errors.log frozen at 08-21 04:20" state the last six nightlies reported ENDED at 08-27 05:20:16** — the live file grew to 944 KB (mtime 08-27 05:20) and its one new write since 08-21 is a single `discord.client` reconnect ERROR whose traceback is a **Discord gateway `WSServerHandshakeError: 503`** on `wss://gateway-us-east1-d.discord.gg` — a genuinely NEW signature (the `discord.py` websocket layer being 503'd by Discord's edge), **distinct** from the `discord.com:443` `ClientConnectorDNSError` adapter-DNS class, and it **self-healed within pid 725 in ~8 s with no restart** (`gateway.start` still **30**, `[Discord] Connected as orchestrator#5798` at 05:20:24). MCP-parking meanwhile is gone an **EIGHTH** night (08-21→08-28 all 0 parks, last still 08-20 13:32:11 — the WS-503 was a Discord *shard resume*, not a `gateway.start`, so it did NOT bring parking back or re-test the MCP transports), gateway pid 725 has held ~7.7 days, and `mcp__codegraph__*`/`mcp__basic-memory__*` + agent.log `RESUMED session` keepalives through **08-28 02:57** verify it live. **Curator did NOT fire by 03:00** — still `run_count=5`, `.curator_state` mtime still 08-21 14:27; the projected ~08-28 6th run hasn't landed (its ~weekly runs are early-afternoon, 13:27–14:27, *after* the 03:00 nightly — exactly how 08-21 itself behaved), so re-check `run_count` on the **08-29** nightly. Two lessons this reinforces: (a) the cheap "frozen mtime == zero writes" shortcut the prior nightlies leaned on is now retired — a single non-park write broke it, so grep by-date, don't trust mtime alone; (b) a long "silent errors.log" run does NOT mean the next Discord error will be the same class — this one was a WS-503, not the DNS blip. Recorded in `hermes-local-gateway-ops` §"Restart & exit-diagnostics triage" (new signature) + §"Behavior that is normal" (CONFIRMED 08-28). Read the logs before declaring a pure no-op.
  **08-29 is SKILLS-idle on the worker axis a TENTH straight quiet-infra night (1 gateway-skill commit + this runbook commit = 2), but is emphatically NOT a pure no-op — because tonight the axis the last SIX nightlies all flagged as "imminent" finally moved: the curator FIRED.** Worker axis: the last real `done` is STILL the 08-19 jetson session (captured 08-20); worker-runner.log shows only lock-exit / "no .task files" noise past it and tonight's own 0-byte `reflect-2026-08-29`. The finding: **the projected ~08-28 curator run landed 08-28 18:44:27** (`run_count` 5→6, 0.64s, 0 tokens, still `llm: skipped (consolidation off)`), and it **jumped `auto: 2 marked stale` → `auto: 70 marked stale`** (`run.json`: `marked_stale:70, archived:0, reactivated:0, checked:72`). The 2→70 is **not a mechanism change** — the 70 newly-stale are *exactly the never-invoked 07-24 seed cohort* (all 70 share `created_at` 2026-07-24 + `last_used_at: null` in `.usage.json`, a same-age batch crossing the ~35-day staleness line together). **The 08-22 watch-item did NOT trip:** `.usage.json` now holds only **2 `active`** skills — `hermes-local-gateway-ops` (last_used 08-19, kept fresh because the nightly reads it, still `pinned:false`) and `delegate-to-claude` — while `nightly-maintenance` + `claude-worker-env` are **still absent from the sidecar entirely** (immune by absence), so the maintained set is safe this run. **But I corrected the over-clean "invocation-age → stale" model:** `delegate-to-claude` (last_used **07-20**, ~39 days idle) is active while `claude-code`/`hermes-agent` (07-18/07-19, only 1–2 days *older*) are stale — a fixed last_used-age cutoff can't produce that split, so the boundary has another signal or the auto-pass doesn't re-clock already-active skills; **left as an open anomaly, did NOT fabricate the threshold.** All recorded in `hermes-local-gateway-ops` §"Curator" + the cadence bumped to `run_count=6` (next ~09-04). Infra otherwise held: **MCP-parking gone a NINTH night** (08-21→08-29 all 0, last park still 08-20 13:32:11), errors.log **quiet again** (last write still the 08-27 05:20 WS-503 — 0 writes 08-28/08-29, so it did not recur), gateway pid 725 held **~8.5 days** no restart (`gateway.start` still 30), `mcp__*` tools + agent.log `RESUMED session` keepalives through 08-29 02:58 verify it live (CONFIRMED 08-29 in `hermes-local-gateway-ops` §"Behavior that is normal"). So the lesson holds a tenth night: a long idle worker-session streak says nothing about the infra axes — the one thing the runbook kept saying "will change soon" finally did, and reading the curator state is what caught it.
  **08-30 is SKILLS-idle on the worker axis an ELEVENTH straight quiet-infra night, and its finding is a *refactor*, not a new datapoint.** The `hermes-local-gateway-ops` §"Behavior that is normal" MCP-parking log had accreted one near-identical "CONFIRMED parking gone Nth night" paragraph per night (08-22→08-29, ~111 lines / ~12.4 KB), so tonight I **COLLAPSED that run into a single rolling paragraph carried through 08-30** (net −9.8 KB) — no durable fact dropped (the 08-21 `discord.com:443` DNS blip, the 08-27 WS-503, and the 08-28 curator fire all already live in that skill's §"Restart & exit-diagnostics triage" / §"Curator" sections it cross-refs). Tonight's own datapoint — parking gone a **10th** night (08-21→08-30 all 0 parks, last still 08-20 13:32:11), errors.log quiet (0 writes 08-28/29/30, the WS-503 did not recur, ~70 h silent), gateway pid 725 up ~9.5 d no restart (`gateway.start` held at 30), `mcp__*` tools + `RESUMED session` keepalives through 08-30 01:57 live, curator unchanged (`run_count=6`, next ~09-04) — was folded **into** that rolling paragraph, not appended after it. **New convention (apply going forward): when a tracked-metric subsection accumulates more than ~5 near-identical dated confirmations, consolidate it into ONE rolling summary — preserve every *distinct* event (cross-reference the section that owns it) and collapse the pure confirmations — instead of appending indefinitely. This runbook's OWN per-night Task-1 idle narration and Task-2 fold ledger are the next consolidation candidates.** So an idle night can earn its keep by *reducing* a skill, not only by adding to it.
  **08-31 is NOT a pure no-op — the first genuine infra finding since the 08-28 WS-503, and the first real
  worker-axis activity since the 08-19 jetson session (3 commits: `hermes-local-gateway-ops` +
  `delegate-to-claude` + this runbook).** Two linked findings from the 08-30 10:08 errors.log write: (1)
  the **08-27 Discord gateway `WSServerHandshakeError: 503` RECURRED 08-30 10:08:14** — a second identical
  event, so it is a *recurring transient*, not the one-off the runbook described; it again self-healed in
  pid 725 with no restart (`gateway.start` still 30, RESUMED keepalives through 08-31 01:53:44) — recorded
  in `hermes-local-gateway-ops` §"Restart & exit-diagnostics triage" + the rolling parking paragraph
  (now 11 nights, 08-21→08-31, corrected from "two writes / did not recur" to "three writes / recurred");
  (2) coincident at 10:08:17, the worker task **`resume-merge-authorization` FAILED** with `No conversation
  found with session ID` — an **aged-out-session RESUME** (Everett trying to authorize the nightly-branch
  merge; the session had expired), the 2nd live occurrence of the 07-21 `resume-vision-model-selection`
  mode — recorded as a confirmation in `delegate-to-claude`. The clustered 10:08 WS-503 + `tools.registry
  … unavailable this turn` cascade + FAILED task are **three unrelated-but-simultaneous benign events**,
  not one outage. MCP-parking held gone an **11th** night (08-21→08-31 all 0, last park still 08-20
  13:32:11), curator unchanged (`run_count=6`, fired 08-28, next ~09-04). **The two flagged
  ledger-consolidation candidates — this runbook's OWN Task-1 idle narration and Task-2 fold ledger —
  remain OPEN**: deferred again tonight to prioritize the genuine finding and avoid a risky ~250-line
  verbatim rewrite of the most-relied-on runbook; still the standing reductive-work candidate for a truly
  idle night.
  **09-01 is SKILLS-idle on the worker axis a quiet-infra night, and it finally SPENT the standing
  reductive-work candidate: tonight's main SKILLS act is the deferred Task-2 fold-ledger consolidation
  (see Task 2 below), not a new finding.** Worker axis: the last real `done` is STILL the 08-19 jetson
  session (captured 08-20); worker-runner.log shows only lock-exit / "no .task files" noise past it and
  tonight's own 0-byte `reflect-2026-09-01`. Infra held quiet — recorded in `hermes-local-gateway-ops`
  (rolling paragraph carried to 09-01): **MCP-parking gone a TWELFTH night** (08-21→09-01 all 0 parks,
  last park still 08-20 13:32:11, live errors.log holds 1179), `errors.log` **silent ~47 h** (its last
  write is still the 08-30 10:08:14 WS-503 + `tools.registry` cascade, so the WS-503 did NOT fire a
  third time — `WSServerHandshakeError` count still 2), gateway **pid 725 up ~11.9 d** no restart
  (`gateway.start` held at 30), `mcp__codegraph__*`/`mcp__basic-memory__*` tools surfaced + agent.log
  `RESUMED session` keepalives through 09-01 02:00:35 verify it live, curator unchanged (`run_count=6`,
  fired 08-28, next ~09-04). **The reductive work:** the Task-2 MEMORY fold ledger below had grown to one
  near-identical "verified no-op, nothing lost" paragraph per night; collapsed each contiguous no-op run
  (07-24→08-18 and 08-20→08-23) into ONE rolling bullet — no distinct event dropped, the three genuine
  folds (07-21, 07-23, 08-19) stay narrated in full, and every fact is cross-referenced to the skill or
  `pantry.md` line that owns it. **The Task-1 idle narration (this very block, 07-24→now) is now the
  LAST-remaining consolidation candidate** — deferred tonight to keep the diff to one runbook section; it
  is the next truly-idle-night reductive target.
  On an idle day
  **do NOT fabricate skill edits.** Either capture one genuine finding from the
  nightly session itself — it runs *through* `claude-worker`, so its own tool
  denials are valid worker-sandbox evidence for `claude-worker-env` — or make a
  minimal honest change. **1–2 commits is the healthy norm**; a big diff on an
  idle night is a smell.
- **Where findings land** (refine the existing skill, don't spawn near-dupes):
  `claude-worker-env` (shell sandbox / PATH / allowlist), `hermes-local-gateway-ops`
  (gateway, Gemini limits, curator, infra), `github-workflow` (git/PR recipes),
  `delegate-to-claude` (queue lifecycle). Every commit message states the
  evidence (which session/log, which date).
- Finish: `git -C ~/agents/skills push -u origin nightly-<date>`. **Do not merge.**

## Task 2 — MEMORY (archive one daily-log, fold durable facts)

- **"older than 7 days" = STRICTLY more than 7 days before today.** A file dated
  exactly `today − 7` **stays**. So each night **exactly one** daily-log crosses
  the line: the one dated `today − 8`. On 07-26, `2026-07-18` (8 days) archives
  and `2026-07-19` (7 days) stays. First-ever eligible date was 07-25 (which
  archived 07-17); 07-22/23/24 were correctly no-ops.
- For that one file: **fold its durable, NOT-yet-captured facts** into the
  matching `~/agents/memory/projects/<name>.md` (pantry → `projects/pantry.md`),
  then move the original to `~/agents/memory/daily-log/archive/` (`mv`, or
  `git -C ~/agents/memory mv` — either is fine; the backup routine commits it).
  - **Most old content is already captured** by the intervening daily logs, prior
    foldings, and the skills — the Hermes model-swap saga lives in
    `hermes-local-gateway-ops`, the queue/duplicate-run facts in
    `delegate-to-claude`, and recent project status supersedes old capture
    decisions. Fold only what is durable AND not already somewhere; add a one-line
    provenance note to the project file ("<date> daily-log folded in during the
    <today> nightly archival"); and **state in the reflection that nothing was
    lost** (name where the rest already lives). Don't duplicate a skill's facts.
  - **But "usually nothing to fold" is not "never" — diff section-by-section, don't
    assume.** 07-17→07-20 were all no-add folds, but **07-21 (folded 07-29) broke the
    streak**: its receipt-parsing half was already in `pantry.md` Status, yet its
    *second* deliverable — the **spec-audit → `chore/spec-audit-tracking-issues`
    branch** (idempotent `scripts/create-tracking-issues.sh` filing 18 `[spec 2..19]`
    issues, still un-run because `gh` is gated) — was captured **nowhere** and had to
    be folded in. Lesson: walk each `##` section of the archived log against the
    project file before declaring a no-op; a still-open unmerged branch/deliverable
    is exactly the durable thing that slips through. **07-22 (folded 07-30) went back
    to a clean no-op** — but only *after* diffing all four of its sections: its
    worker-env "budget ONE probe" lesson was already in `claude-worker-env`, its
    RESUME-from-the-slug's-JSON-not-the-newest lesson in `delegate-to-claude`, its
    idempotent-`gh`-script pattern in `github-workflow`, and its spec-audit deliverable
    already folded into `pantry.md` Status on 07-29. No-op is the norm, but earn it.
  - **07-23 (folded 07-31) broke the no-op streak again — the SAME failure mode as 07-21.**
    Its `## Nightly reflection` half was all already-captured worker-env/git facts (the
    `simple_expansion` for-loop + `git -C` rules in `claude-worker-env`, the
    `merge-tree --write-tree` drift recipe in `github-workflow`), BUT its **second section**
    — the pantry **`feat/nightly-pull-routine`** deliverable (`scripts/sync-main.sh` = `npm run
    sync`, `.github/workflows/nightly-sync.yml` report-only cron, spec `specs/nightly-sync.md`;
    branch pushed, **PR never opened because `gh` is gated**) — was captured **nowhere** and was
    folded into `pantry.md` Status. Two of three real folds so far (07-21, 07-23) have been exactly
    this: a pushed-but-un-PR'd feature branch in the log's project section. **That is the pattern to
    hunt** — walk each `##` section, and treat any still-open unmerged branch as fold-worthy until
    you've found it in the project file.
  - **07-24 through 08-18 folds (done on the 08-01 → 08-26 nightlies) were ALL verified no-ops — consolidated here from the former one-paragraph-per-night ledger (collapsed on the 2026-09-01 nightly per the ledger-consolidation convention; no distinct event dropped).** Every one of these archived logs was a `## Nightly reflection` whose durable content was already captured elsewhere: its infra facts (the entire MCP-parking arc — first-captured 08-10, the steady flat ~562/day period, the 08-14 `errors.log`-rotation caveat → per-day rate, the 08-19 periodic ~5-min self-probe reframe, and the 08-20 13:32 cycle-end) live in `hermes-local-gateway-ops` §"Behavior that is normal"; its worker-env/git facts (`simple_expansion` loops, `git -C`, the bare-glob approval gate, `update-index --chmod`, `merge-tree --write-tree`) in `claude-worker-env` / `github-workflow`; and each night's own MEMORY fold plus standing carry-overs (the three still-open un-PR'd branches `feat/nightly-pull-routine` / `feat/receipt-parsing` / `chore/spec-audit-tracking-issues`, PR #9 merged / #10 open, the ANTHROPIC_API_KEY prereq) were **all already in the `pantry.md` Status board** — its provenance lines (one per date) + each night's commit message hold the per-date detail. The fold-worthy-pattern hunt (walk each `##` section; treat any still-open un-PR'd branch as fold-worthy until found in the project file) ran every night and correctly came up empty: none of these logs opened a feature branch of its own. Nothing was lost on any of them. (The three genuine folds sit OUTSIDE this run and stay narrated in full: 07-21 and 07-23 above, 08-19 below.)
  - **08-19 (folded 08-27) BROKE the no-op streak — the THIRD "un-PR'd branch/PR slips through" real fold,
    same failure mode as 07-21 and 07-23.** 08-19's log has two `##` sections; its `## Nightly reflection`
    half was all already-captured (the 08-11 no-op fold at `pantry.md` line 34; the eleventh-night flat
    MCP-parking + periodic-self-probe reframe in `hermes-local-gateway-ops`), **but its second section — the
    queued `jetson-orin-setup-plan` worker deliverable: `specs/jetson-orin-nano-setup.md` on branch
    `feat/jetson-orin-setup-plan`, PR #101, + a `—`-row in `specs/README.md` — was captured NOWHERE** in
    `pantry.md` (its Status board's newest entry was still 07-23) and was folded into Status tonight. The
    lesson holds and now has a third data-point: walk each `##` section and treat any still-open PR / pushed
    branch in the log's *project* section as fold-worthy until you've found it in the project file — a long
    run of no-op folds (08-10→08-18 here) does NOT mean the next one is. The 08-19 log's `gh`-spawn PR-create
    bridge fact (how PR #101 was opened) was already folded into `claude-worker-env` on the 08-20 nightly, so
    only the pantry deliverable itself was new. Provenance line added at `pantry.md`; nothing else lost.
  - **08-20 through 08-23 folds (done on the 08-28 → 08-31 nightlies) were ALL verified no-ops — same consolidation (collapsed 2026-09-01).** Each was a `## Nightly reflection` log with no still-open PR/branch of its own (08-20 only *reported on* the 08-19 jetson session, whose PR #101 deliverable was already folded on 08-27). Their durable infra facts (parking gone the 2nd→5th night → "empty park stream = healthy"; the 08-21 `discord.com:443` DNS blip generalized to "transient on ANY (re)connect"; the 08-22 curator first-ever `auto: 2 marked stale`) are all in `hermes-local-gateway-ops` §"Behavior that is normal" / §"Restart & exit-diagnostics triage" / §"Curator" and were superseded nightly since; their MEMORY halves + carry-overs (PR #101, the three un-PR'd branches, PR #10, ANTHROPIC_API_KEY) were all already in `pantry.md` Status. Provenance lines + commit messages hold the per-date detail — nothing lost.
  - Memory files use **basic-memory frontmatter** (`title` / `type` / `permalink`)
    — preserve it when editing or moving.
- **Do NOT commit or push memory yourself.** The 03:00 `backup` routine commits
  the staged rename + note edits + the new daily-log to
  `m4-mini-orchestrator.git` (`main`) automatically — verified every night in
  `~/agents/logs/backup.log`. Your job is just to leave the files in the right
  state.

## Task 3 — Nightly reflection note

- Append a **5-line** summary under a `## Nightly reflection` heading in
  `~/agents/memory/daily-log/<date>.md`. **The file usually does not exist yet**
  at 03:00 — create it (with basic-memory frontmatter matching the sibling logs).
  This human-facing note is separate from the job's own result JSON, and it's
  what the CLAUDE.md handoff protocol points at.
- Cover: what each of the three tasks did, the branch name + commit count, any
  standing carry-overs (e.g. the unmerged skill branches; a pushed pantry branch
  whose PR isn't open because `gh` is gated). Keep it honest — an idle night says
  so.

## Environment quick-refs

Runs in the `claude-worker` sandbox: use `git -C <repo>` (never `cd && git`),
avoid shell `for`/`while` loops and captured `$(...)` (rejected as
`simple_expansion`), and read the reflect JSONs with `jq`. Chained `||`/`&&`
fallbacks can trip the "multiple operations … requires approval" gate — run
fallbacks as separate calls. Full sandbox detail is in `claude-worker-env`.
