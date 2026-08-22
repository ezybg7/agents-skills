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
  **08-22 is SKILLS-idle on the worker axis again but idle-but-real-finding for a third straight night — three verifiable findings, all in `hermes-local-gateway-ops` (1 commit + this runbook commit = 2 total).** Worker axis: the last real `done` is still the 08-19 jetson session (captured 08-20); worker-runner.log has only lock-exit / "no .task files" noise since, and the only new `claude-*.json` is tonight's own 0-byte `reflect-2026-08-22`. The three findings: (1) **the `discord.com:443` adapter DNS blip recurs with NO gateway restart** — it fired 08-21 04:16–04:22 as a *mid-run liveness-probe reconnect* (exit-diag `gateway.start` held at 30, pid 725; self-healed to `✓ discord reconnected` at 04:22:36), so last night's "recurs on restart" tightens to "transient on ANY (re)connect"; (2) **MCP-parking stayed gone a second night** (08-21=0 and 08-22=0 parks, still no new `gateway.start`, `mcp__*` tools callable — "empty park stream = healthy" holding, the post-restart-return watch still open because no restart has happened); (3) **the curator's projected ~08-21 run DID fire** (08-21 14:27, `run_count` 4→5, fifth weekly-cadence point) and is the **first-ever non-"no changes" run — `auto: 2 marked stale`** (`claude-code` + `hermes-agent`, both unpinned product-reference skills idle ~34 days, 0 archived) — first live proof of the invocation-driven staleness mechanism; the nightly-maintained skills are NOT stale but are unpinned (watch item). All recorded in `hermes-local-gateway-ops`. So a third consecutive idle-but-real-finding night: read the logs before declaring a pure no-op. On an idle day
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
  - **07-24 (folded 08-01) went back to an earned no-op — the hunt ran and came up empty.** Applied
    the pattern above: 07-24 is a `## Nightly reflection` log, so I diffed each of its lines. Its two
    skill findings were already codified — the `git update-index --chmod=+x` (mode `100755`, since
    `chmod`/`bash -n`/exec are gated on a committed script) fact in `claude-worker-env`, and the
    `merge-tree --write-tree` branch-drift recipe in `github-workflow`. Its OPEN/standing carry-overs
    named three still-open un-PR'd branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`,
    `chore/spec-audit-tracking-issues`) — exactly the fold-worthy pattern — but **all three were
    already in `pantry.md` Status** (nightly-pull-routine folded 07-31, the other two 07-29). So the
    hunt confirmed nothing was uncaptured: verified no-op, provenance line added, nothing lost.
  - **07-25 (folded 08-02) was another earned no-op — the pattern-hunt came up empty.** 07-25 was
    the *first-ever* archival night (it folded 07-17), so its own log is a `## Nightly reflection`
    whose durable content is all infra/curator: the **first live curator run** (07-24 13:27) and the
    box-specific fact that **`~/.hermes/skills` is a symlink to `~/agents/skills`** are both fully
    captured in `hermes-local-gateway-ops` (§"Curator — first live run"); the `.gitignore` add of
    `.curator_backups/`+`.archive/` is committed in the skills repo. Its only standing carry-over was
    the pantry `feat/nightly-pull-routine` un-PR'd branch — already in `pantry.md` Status (folded
    07-31). No un-captured deliverable of its own → verified no-op, provenance line added, nothing lost.
  - **07-26 (folded 08-03) was another earned no-op — the pattern-hunt came up empty.** 07-26 was a
    `## Nightly reflection` log (it archived 07-18). Diffed section-by-section: the two durable facts
    it folded that night — the Gemini `-latest`-alias pin gotcha and the "receipt image never
    persisted" privacy invariant — came from 07-18 and are already in `pantry.md` §"AI vision provider
    gotchas"; its skill work (the `nightly-maintenance` runbook itself, and the `claude-worker-env`
    chained-`||`/`&&`-fallback fact) is committed in the skills repo; and its lone standing carry-over,
    the pantry `feat/nightly-pull-routine` un-PR'd branch, is already in the Status board (folded
    07-31). No un-captured deliverable of its own → verified no-op, provenance line added, nothing lost.
  - **07-27 (folded 08-04) was another earned no-op — the pattern-hunt came up empty.** 07-27 was a
    `## Nightly reflection` log (it archived 07-19). Diffed section-by-section: its lone SKILLS finding
    was self-referential and *already codified in this very runbook* — the runbook's **first live use**
    caught its own stale "23 commits ahead" and switched to a live `rev-list --count` (see Task 1 above,
    "corrected on 07-27"). Its MEMORY section was the 07-19 no-op fold, already recorded in `pantry.md`
    line 11. Its standing carry-overs named the exact fold-worthy pattern — three still-open un-PR'd
    branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`, `chore/spec-audit-tracking-issues`)
    plus PR #9/#10 review and the Anthropic-API-key prereq — but **all are already in the Status board**
    (nightly-pull-routine folded 07-31, the other two 07-29; #9 merged / #10 open and the ANTHROPIC_API_KEY
    prereq both in the 07-20 entries). No un-captured deliverable of its own → verified no-op, nothing lost.
  - **07-28 (folded 08-05) was another earned no-op — the pattern-hunt came up empty.** 07-28 was a
    `## Nightly reflection` log (it archived 07-20). Diffed section-by-section: its lone SKILLS finding —
    that a **bare file-glob** (a single unchained `jq -r '.result' …-*.json`) trips the "multiple
    operations … requires approval" gate, so the trigger is the unresolved glob itself, **not** `||`/`&&`
    chaining — is already codified in `claude-worker-env` (the gate bullet, tagged "(07-28…)"). Its MEMORY
    half was the 07-20 no-op fold already recorded in `pantry.md` (line 13). Its standing carry-overs named
    the fold-worthy pattern — the still-open un-PR'd branches (`feat/nightly-pull-routine`,
    `feat/receipt-parsing`, `chore/spec-audit-tracking-issues`) plus PR #9/#10 review and the
    Anthropic-API-key prereq — but **all are already in the Status board** (nightly-pull-routine folded
    07-31, the other two 07-29; #9 merged / #10 open and the ANTHROPIC_API_KEY prereq in the 07-20 entries).
    No un-captured deliverable of its own → verified no-op, nothing lost.
  - **07-29 (folded 08-06) was another earned no-op — the pattern-hunt came up empty.** 07-29 was a
    `## Nightly reflection` log (it archived 07-21). Note the twist: 07-29's *own* MEMORY half **was** the
    first-ever non-no-op fold (it folded 07-21's spec-audit → `chore/spec-audit-tracking-issues` deliverable
    into Status), but archiving 07-29 tonight is still a no-op because that fold already landed on 07-29
    (provenance at `pantry.md` line 12). Diffed section-by-section: its SKILLS half was idle-day runbook
    upkeep (2 commits, committed in the skills repo). Its standing carry-overs named the fold-worthy pattern —
    the three still-open un-PR'd branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`,
    `chore/spec-audit-tracking-issues`, incl. `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus
    PR #9/#10 review and the ANTHROPIC_API_KEY prereq — but **all are already in the Status board**
    (nightly-pull-routine folded 07-31, the other two 07-29; #9 merged / #10 open and the ANTHROPIC_API_KEY
    prereq in the 07-20 entries). No un-captured deliverable of its own → verified no-op, nothing lost.
  - **07-30 (folded 08-07) was another earned no-op — the pattern-hunt came up empty.** 07-30 was a
    `## Nightly reflection` log (it archived 07-22, itself a verified no-op). Diffed section-by-section: its
    SKILLS half was idle-day runbook upkeep (1 commit adding 07-30 to the idle-days list + recording 07-22's
    clean no-op), committed in the skills repo; the `cd && git` hook-gate it nearly hit is already in this
    runbook's Environment quick-refs. Its MEMORY half was the 07-22 no-op fold already recorded in `pantry.md`
    (line 14). Its standing carry-overs named the fold-worthy pattern — the three still-open un-PR'd branches
    (`feat/nightly-pull-routine`, `feat/receipt-parsing`, `chore/spec-audit-tracking-issues` incl.
    `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus PR #9/#10 review and the ANTHROPIC_API_KEY
    prereq — but **all** are already in the Status board (nightly-pull-routine folded 07-31, the other two 07-29;
    #9 merged / #10 open and the ANTHROPIC_API_KEY prereq in the 07-20 entries). No un-captured deliverable of
    its own → verified no-op, nothing lost.
  - **07-31 (folded 08-08) was another earned no-op — same twist as 07-29.** 07-31 was a `## Nightly
    reflection` log (it archived 07-23), and like 07-29 its *own* MEMORY half **was** a real fold — it folded
    07-23's pantry **`feat/nightly-pull-routine`** deliverable into Status (provenance at `pantry.md` line 15).
    But archiving 07-31 tonight is still a no-op because that fold already landed on 07-31. Diffed
    section-by-section: its SKILLS half was idle-day runbook upkeep (1 commit: added 07-31 to the idle-days
    list, marked it SKILLS-idle-but-real-fold, and recorded the 07-23 fold as the *second* "un-PR'd branch
    slips through" case) — committed in the skills repo. Its standing carry-overs named the fold-worthy
    pattern — the three still-open un-PR'd branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`,
    `chore/spec-audit-tracking-issues` incl. `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus
    PR #9/#10 review and the ANTHROPIC_API_KEY prereq — but **all** are already in the Status board
    (nightly-pull-routine folded 07-31, the other two 07-29; #9 merged / #10 open and the ANTHROPIC_API_KEY
    prereq in the 07-20 entries). No un-captured deliverable of its own → verified no-op, nothing lost.
  - **08-01 (folded 08-09) was another earned no-op — the pattern-hunt came up empty.** 08-01 was a
    `## Nightly reflection` log (it archived 07-24). Diffed section-by-section: its SKILLS half was idle-day
    runbook upkeep (1 commit: added 08-01 to the idle-days list, noted the nine-night streak, recorded 07-24's
    fold as an earned no-op) — committed in the skills repo. Its MEMORY half was the 07-24 verified no-op fold
    already recorded above (`pantry.md` line 16). Its health note — that a chained `||`/`;` command trips the
    "multiple operations … requires approval" gate, so `git mv` was re-run as a single call — is already in
    `claude-worker-env` (the gate bullet). Its standing carry-overs named the fold-worthy pattern — the three
    still-open un-PR'd branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`,
    `chore/spec-audit-tracking-issues` incl. `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus
    PR #9/#10 review and the ANTHROPIC_API_KEY prereq — but **all** are already in the Status board
    (nightly-pull-routine folded 07-31, the other two 07-29; #9 merged / #10 open and the ANTHROPIC_API_KEY
    prereq in the 07-20 entries). 08-01 opened no feature branch of its own → verified no-op, nothing lost.
  - **08-02 (folded 08-10) was another earned no-op — the pattern-hunt came up empty.** 08-02 was a
    `## Nightly reflection` log (it archived 07-25). Diffed section-by-section: its SKILLS half was idle-day
    runbook upkeep (1 commit: added 08-02 to the idle-days list, bumped the streak to ten, recorded 07-25's
    fold as a verified no-op) — committed in the skills repo; its `simple_expansion` for-loop denial note is
    already in `claude-worker-env` (line 62). Its MEMORY half was the 07-25 verified no-op fold already
    recorded at `pantry.md` line 17. Its standing carry-overs named the fold-worthy pattern — the three
    still-open un-PR'd branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`,
    `chore/spec-audit-tracking-issues` incl. `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus
    PR #9/#10 review and the ANTHROPIC_API_KEY prereq — but **all** are already in the Status board
    (nightly-pull-routine folded 07-31, the other two 07-29; #9 merged / #10 open and the ANTHROPIC_API_KEY
    prereq in the 07-20 entries). 08-02 opened no feature branch of its own → verified no-op, nothing lost.
  - **08-03 (folded 08-11) was another earned no-op — the pattern-hunt came up empty.** 08-03 was a
    `## Nightly reflection` log (it archived 07-26). Diffed section-by-section: its SKILLS half was idle-day
    runbook upkeep (1 commit: bumped the idle streak to eleven, logged 07-26's verified no-op fold) — committed
    in the skills repo. Its MEMORY half was the 07-26 verified no-op fold already recorded at `pantry.md`
    line 18 — and the two facts 07-26 itself folded (the Gemini `-latest`-alias pin gotcha + the "receipt image
    never persisted" privacy invariant) are already under `pantry.md` §"AI vision provider gotchas". Its standing
    carry-overs named the fold-worthy pattern — the three still-open un-PR'd branches (`feat/nightly-pull-routine`,
    `feat/receipt-parsing`, `chore/spec-audit-tracking-issues` incl. `create-tracking-issues.sh`/the 18
    `[spec 2..19]` issues) plus PR #9/#10 review and the ANTHROPIC_API_KEY prereq — but **all** are already in the
    Status board (nightly-pull-routine folded 07-31, the other two 07-29; #9 merged / #10 open and the
    ANTHROPIC_API_KEY prereq in the 07-20 entries). 08-03 opened no feature branch of its own → verified no-op, nothing lost.
  - **08-04 (folded 08-12) was another earned no-op — the pattern-hunt came up empty.** 08-04 was a
    `## Nightly reflection` log (it archived 07-27). Diffed section-by-section: its SKILLS half was idle-day
    runbook upkeep (1 commit: bumped the idle streak to twelve, logged 07-27's verified no-op fold; noted
    honestly that mem%/ollama were not re-probed) — committed in the skills repo. Its MEMORY half was the
    07-27 verified no-op fold already recorded at `pantry.md` line 19 — and the 07-27 fold's own content (its
    lone SKILLS finding was the runbook's first live use, the `rev-list --count` switch, codified in this very
    runbook; its MEMORY half was the 07-19 no-op fold at `pantry.md` line 11). Its standing carry-overs named
    the fold-worthy pattern — the three still-open un-PR'd branches (`feat/nightly-pull-routine`,
    `feat/receipt-parsing`, `chore/spec-audit-tracking-issues` incl. `create-tracking-issues.sh`/the 18
    `[spec 2..19]` issues) plus PR #9/#10 review and the ANTHROPIC_API_KEY prereq — but **all** are already in
    the Status board (nightly-pull-routine folded 07-31, the other two 07-29; #9 merged / #10 open and the
    ANTHROPIC_API_KEY prereq in the 07-20 entries). 08-04 opened no feature branch of its own → verified no-op, nothing lost.
  - **08-05 (folded 08-13) was another earned no-op — the pattern-hunt came up empty.** 08-05 was a
    `## Nightly reflection` log (it archived 07-28). Diffed section-by-section: its SKILLS half was idle-day
    runbook upkeep (1 commit: bumped the idle streak to thirteen, logged 07-28's verified no-op fold) — committed
    in the skills repo. Its MEMORY half was the 07-28 verified no-op fold already recorded at `pantry.md`
    line 20 — and 07-28's own durable content (its lone SKILLS finding, the bare-file-glob approval-gate trigger,
    codified in `claude-worker-env` tagged "(07-28…)"; its 07-20 no-op fold at `pantry.md` line 13) is likewise
    already captured. Its standing carry-overs named the fold-worthy pattern — the three still-open un-PR'd branches
    (`feat/nightly-pull-routine`, `feat/receipt-parsing`, `chore/spec-audit-tracking-issues` incl.
    `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus PR #9/#10 review and the ANTHROPIC_API_KEY
    prereq — but **all** are already in the Status board (nightly-pull-routine folded 07-31, the other two 07-29;
    #9 merged / #10 open and the ANTHROPIC_API_KEY prereq in the 07-20 entries). 08-05 opened no feature branch of
    its own → verified no-op, nothing lost.
  - **08-06 (folded 08-14) was another earned no-op — the pattern-hunt came up empty.** 08-06 was a
    `## Nightly reflection` log (it archived 07-29). Diffed section-by-section: its SKILLS half was idle-day
    runbook upkeep (branch `nightly-2026-08-06` pushed, 1 commit bumping the idle streak to fourteen + recording
    07-29's verified no-op fold) — committed in the skills repo. Its MEMORY half was the 07-29 verified no-op fold
    already recorded at `pantry.md` line 21 — and 07-29's own twist (its *own* MEMORY half was the first-ever real
    fold, the 07-21 spec-audit deliverable, but that already landed on 07-29 at `pantry.md` line 12) is likewise
    already captured. Its standing carry-overs named the fold-worthy pattern — the three still-open un-PR'd branches
    (`feat/nightly-pull-routine`, `feat/receipt-parsing`, `chore/spec-audit-tracking-issues` incl.
    `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus PR #9/#10 review and the ANTHROPIC_API_KEY
    prereq — but **all** are already in the Status board (nightly-pull-routine folded 07-31, the other two 07-29;
    #9 merged / #10 open and the ANTHROPIC_API_KEY prereq in the 07-20 entries). 08-06 opened no feature branch of
    its own → verified no-op, nothing lost.
  - **08-07 (folded 08-15) was another earned no-op — the pattern-hunt came up empty.** 08-07 was a
    `## Nightly reflection` log (it archived 07-30, itself a verified no-op). Diffed section-by-section: its SKILLS
    half was idle-day runbook upkeep (branch `nightly-2026-08-07`, 1 commit bumping the idle streak to fifteen +
    recording 07-30's verified no-op fold) — committed in the skills repo. Its MEMORY half was the 07-30 verified
    no-op fold already recorded at `pantry.md` line 22 — and 07-30's own content (it archived 07-22, itself a
    verified no-op) is likewise already captured. Its standing carry-overs named the fold-worthy pattern — the three
    still-open un-PR'd branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`, `chore/spec-audit-tracking-issues`
    incl. `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus PR #9/#10 review and the ANTHROPIC_API_KEY
    prereq — but **all** are already in the Status board (nightly-pull-routine folded 07-31, the other two 07-29;
    #9 merged / #10 open and the ANTHROPIC_API_KEY prereq in the 07-20 entries). 08-07 opened no feature branch of
    its own → verified no-op, nothing lost.
  - **08-08 (folded 08-16) was another earned no-op — the pattern-hunt came up empty.** 08-08 was a
    `## Nightly reflection` log (it archived 07-31). Diffed section-by-section: its SKILLS half was idle-day
    runbook upkeep (branch `nightly-2026-08-08`, 1 commit: bumped the idle streak to sixteen, corrected the stale
    "errors.log frozen at 08-03" claim, recorded 07-31's verified no-op fold) — committed in the skills repo, and
    that errors.log correction is already in the `hermes-local-gateway-ops` runbook. Its MEMORY half was the 07-31
    verified no-op fold already recorded above (`pantry.md` line 23) — and 07-31's own twist (its own MEMORY half was
    a real fold, 07-23's `feat/nightly-pull-routine`, already at `pantry.md` line 15) is likewise already captured.
    Its standing carry-overs named the fold-worthy pattern — the three still-open un-PR'd branches
    (`feat/nightly-pull-routine`, `feat/receipt-parsing`, `chore/spec-audit-tracking-issues` incl.
    `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus PR #9/#10 review and the ANTHROPIC_API_KEY prereq —
    but **all** are already in the Status board (nightly-pull-routine folded 07-31 at `pantry.md` line 111, the other
    two 07-29 at lines 109–110; #9 merged / #10 open at lines 106–108 and the ANTHROPIC_API_KEY prereq in the 07-20
    entries). 08-08 opened no feature branch of its own → verified no-op, nothing lost.
  - **08-09 (folded 08-17) was another earned no-op — the pattern-hunt came up empty.** 08-09 was a
    `## Nightly reflection` log (it archived 08-01). Diffed section-by-section: its SKILLS half was idle-day
    runbook upkeep (branch `nightly-2026-08-09`, 1 commit: added 08-09 to the idle-days list as the 17th
    consecutive night + noted the curator's ~weekly cadence so an unchanged run_count reads as expected),
    committed in the skills repo. Its MEMORY half was the 08-01 verified no-op fold already recorded above
    (provenance line 24). Its health note — a chained `||`/`;` command tripping the "multiple operations …
    requires approval" gate, so a git op was re-run as a single `git -C` call — is already in the
    `claude-worker-env` skill (and this runbook's Environment quick-refs). Its standing carry-overs named the
    fold-worthy pattern — the three still-open un-PR'd branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`,
    `chore/spec-audit-tracking-issues` incl. `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus
    PR #9/#10 review and the ANTHROPIC_API_KEY prereq — but **all** are already in the Status board below
    (nightly-pull-routine folded 07-31 at line 112, the other two 07-29 at lines 110–111; #9 merged / #10 open at
    lines 107–109 and the ANTHROPIC_API_KEY prereq in the 07-20 entries). 08-09 opened no feature branch of its
    own → verified no-op, nothing lost.
  - **08-10 (folded 08-18) was another earned no-op — the pattern-hunt came up empty.** 08-10 was a
    `## Nightly reflection` log (it archived 08-02). Diffed section-by-section: 08-10 was **SKILLS-idle-but-real-finding**
    — it was the night that **first captured the MCP-parking class** (`codegraph`+`basic-memory` `parking until a
    reconnect is requested`), which is already codified in `hermes-local-gateway-ops` §"Behavior that is normal" and
    has been refined every night since. Its MEMORY half was the 08-02 verified no-op fold already recorded above
    (`pantry.md` line 25). Its health note — running each git op as a single `git -C` call to clear the
    "multiple operations … requires approval" gate — is already in `claude-worker-env`. Its standing carry-overs named
    the fold-worthy pattern — the three still-open un-PR'd branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`,
    `chore/spec-audit-tracking-issues` incl. `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus PR #10 review
    (#9 merged) and the ANTHROPIC_API_KEY prereq — but **all** are already in the Status board (nightly-pull-routine
    folded 07-31, the other two 07-29; #9 merged / #10 open and the ANTHROPIC_API_KEY prereq in the 07-20 entries).
    08-10 opened no feature branch of its own → verified no-op, nothing lost.
  - **08-11 (folded 08-19) was another earned no-op — the pattern-hunt came up empty.** 08-11 was a
    `## Nightly reflection` log (it archived 08-03). Diffed section-by-section: 08-11 was **SKILLS-idle-but-real-finding**
    — it refined the MCP-parking class with the steady-state-dominant volume + the *first* in-session end-to-end
    reconnect confirmation, both already codified in `hermes-local-gateway-ops` §"Behavior that is normal" (and further
    refined every night since — tonight's 08-19 reframe supersedes it). Its MEMORY half was the 08-03 verified no-op
    fold already recorded above (`pantry.md` line 26). Its standing carry-overs named the fold-worthy pattern — the three
    still-open un-PR'd branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`, `chore/spec-audit-tracking-issues`
    incl. `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus PR #10 review (#9 merged) and the
    ANTHROPIC_API_KEY prereq — but **all** are already in the Status board (nightly-pull-routine folded 07-31, the other
    two 07-29; #9 merged / #10 open and the ANTHROPIC_API_KEY prereq in the 07-20 entries). 08-11 opened no feature
    branch of its own → verified no-op, nothing lost.
  - **08-12 (folded 08-20) was another earned no-op — the pattern-hunt came up empty.** 08-12 was a
    `## Nightly reflection` log (it archived 08-04). Diffed section-by-section: 08-12 was **SKILLS-idle-but-real-finding**
    — it refined the MCP-parking class a *third* night dominant + the *second consecutive* in-session self-heal, both
    codified in `hermes-local-gateway-ops` §"Behavior that is normal" and refined every night since (its "1,588 total
    parks" cumulative framing was later superseded by the 08-14 rotation caveat → per-day rate, and the 08-19 reframe
    to a periodic ~5-min self-probe cycle). Its MEMORY half was the 08-04 verified no-op fold already recorded above
    (`pantry.md` line 27). Its standing carry-overs named the fold-worthy pattern — the three still-open un-PR'd branches
    (`feat/nightly-pull-routine`, `feat/receipt-parsing`, `chore/spec-audit-tracking-issues` incl.
    `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus PR #10 review (#9 merged) and the ANTHROPIC_API_KEY
    prereq — but **all** are already in the Status board below (nightly-pull-routine folded 07-31, the other two 07-29;
    #9 merged / #10 open and the ANTHROPIC_API_KEY prereq in the 07-20 entries). 08-12 opened no feature branch of its
    own → verified no-op, nothing lost.
  - **08-13 (folded 08-21) was another earned no-op — the pattern-hunt came up empty.** 08-13 was a
    `## Nightly reflection` log (it archived 08-05). Diffed section-by-section: 08-13 was **SKILLS-idle-but-real-finding**
    — it refined the MCP-parking class a *fourth* night dominant + the *third consecutive* in-session self-heal, both
    codified in `hermes-local-gateway-ops` §"Behavior that is normal" and refined every night since (its "2,150 total
    parks" cumulative framing was superseded by the 08-14 rotation caveat → per-day rate, then the 08-19 periodic
    ~5-min self-probe reframe, and now the **08-21 finding that the whole parking cycle ENDED on 08-20 13:32** across
    two gateway restarts). Its MEMORY half was the 08-05 verified no-op fold already recorded above (`pantry.md`
    line 28). Its standing carry-overs named the fold-worthy pattern — the three still-open un-PR'd branches
    (`feat/nightly-pull-routine`, `feat/receipt-parsing`, `chore/spec-audit-tracking-issues` incl.
    `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus PR #10 review (#9 merged) and the ANTHROPIC_API_KEY
    prereq — but **all** are already in the Status board below (nightly-pull-routine folded 07-31, the other two 07-29;
    #9 merged / #10 open and the ANTHROPIC_API_KEY prereq in the 07-20 entries). 08-13 opened no feature branch of its
    own → verified no-op, nothing lost.
  - **08-14 (folded 08-22) was another earned no-op — the pattern-hunt came up empty.** 08-14 was a
    `## Nightly reflection` log (it archived 08-06). Diffed section-by-section: 08-14 was
    **SKILLS-idle-but-real-finding** — its two genuine facts were the **`errors.log` rotation caveat**
    (it rolled 08-13 11:35 → track the *per-day* park rate, not a cumulative total) and the *fourth
    consecutive* in-session MCP self-heal, both codified in `hermes-local-gateway-ops` §"Behavior that is
    normal" and refined every night since (the 08-19 periodic ~5-min self-probe reframe, the 08-21 finding
    that the parking cycle ENDED 08-20 13:32, and tonight's 08-22 confirmation it stayed gone a second night
    + the DNS-blip-on-reconnect refinement). Its MEMORY half was the 08-06 verified no-op fold already
    recorded above (`pantry.md` line 29). Its standing carry-overs named the fold-worthy pattern — the three
    still-open un-PR'd branches (`feat/nightly-pull-routine`, `feat/receipt-parsing`,
    `chore/spec-audit-tracking-issues` incl. `create-tracking-issues.sh`/the 18 `[spec 2..19]` issues) plus
    PR #10 review (#9 merged) and the ANTHROPIC_API_KEY prereq — but **all** are already in the Status board
    below (nightly-pull-routine folded 07-31, the other two 07-29; #9 merged / #10 open and the
    ANTHROPIC_API_KEY prereq in the 07-20 entries). 08-14 opened no feature branch of its own → verified
    no-op, nothing lost.
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
