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
    `git -C ~/agents/skills merge-base --is-ancestor <last-nightly-branch> nightly-<date>`.
  - **Branch off the last SUCCESSFUL nightly, which is NOT always `<yesterday>`.**
    A nightly can no-op entirely (see the 429 failure mode below), leaving no
    `nightly-<that-date>` branch — so `<yesterday>` may not exist. Don't assume
    the date; take the base from live HEAD (`git -C ~/agents/skills branch
    --show-current`) and pass that to `merge-base --is-ancestor`. **2026-09-06
    branched off `nightly-2026-09-03`** because the 09-04 and 09-05 nightlies both
    died on the 429 (skipped two dates in the chain); the chain stays unbroken as
    long as you branch off whatever HEAD actually is.
- **KNOWN FAILURE MODE — the reflect job can 429 on the Claude session limit and
  no-op the WHOLE night (first seen 09-04/09-05).** The 03:00 `reflect-<date>` job
  runs through `claude-worker` on the same Claude account as the daytime
  interactive/worker sessions, so a heavy day can exhaust the shared **session
  limit** before 03:00. When it does, the job dies in **1 turn, 0 tokens** with
  `is_error:true, api_error_status:429, result:"You've hit your session limit ·
  resets <time>"` (a ~778-byte result JSON) — **no branch, no fold, no note.**
  This is DISTINCT from the gateway's Gemini free-tier 429 (that's the relay
  backend; this is the Claude Code account limit on the reflect job itself). It
  hit **two nights running, 09-04 and 09-05**, during the pantry
  production-readiness push (the 09-05 daily-log even records two mid-day "limit
  reset" relaunches). Detect it: `~/agents/logs/reflection.log` shows `FAILED
  (reflect-<date>)`, and `jq '.is_error,.api_error_status,.result'
  ~/agents/logs/claude-reflect-<date>-*.json` confirms the 429. **Two consequences
  the recovering nightly must handle:** (1) the branch chain skips the failed
  date(s) — branch off live HEAD, not `<yesterday>` (rule above); (2) Task 2 has a
  **backlog** — more than one daily-log will be past the 7-day line (see Task 2's
  "catch-up" note). Nothing else to do about the failures themselves — they're a
  clean no-op, not corruption.
  - **RECOVERED — the 429 did NOT recur on 09-06 or 09-07.** `reflection.log` shows
    `done (reflect-2026-09-06)` and `reflect-2026-09-07` processing normally, so the
    double-failure was the *shared Claude session limit exhausted by the 09-04/09-05
    pantry production-readiness PR storm*, NOT a standing regression. Once the heavy
    interactive days ended the 03:00 job had headroom again — the failure is real but
    load-triggered (expect it only after a very heavy interactive day; the chain
    self-heals the next quiet night, and branch-off-live-HEAD absorbs the gap).
- **Mine only genuinely-fresh material.** Sources:
  - `jq -r '.result' ~/agents/logs/claude-reflect-<date>-*.json` — the recent
    daily reflections (these session-result JSONs hold the distilled text in
    `.result`; today's own is 0 bytes until this job finishes).
  - `~/agents/logs/worker-runner.log` — did any NEW delegated worker session run
    since the last nightly? (look past the last `done (...)` line).
  - `~/.hermes/logs/errors.log`, `gateway.log`, `~/agents/logs/{mempressure,ollama}.log`,
    and curator state (`~/agents/skills/.curator_state` mtime) for infra events.
- **Idle days are the steady state here, not a fault.** "SKILLS-idle" = no NEW
  delegated worker session since the last nightly (worker-runner.log has only
  lock-exit / "no .task files" noise past the last real `done`). This held every
  night **07-24→08-19** (a 27-night streak) and again **08-21→09-03**; the last
  real worker session is still `jetson-orin-setup-plan` on 08-19 11:06. A long
  idle streak is the expected steady state — keep making ONE honest runbook
  refinement rather than inventing edits.
- **"SKILLS-idle" is independent of the MEMORY task (Task 2), so read the logs
  before declaring a pure no-op.** 07-29 and 07-31 were SKILLS-idle yet each had
  a real fold; 08-27 was SKILLS-idle yet landed the 08-19 jetson PR #101 fold;
  most other nights had a no-op fold but a non-empty SKILLS finding. Walk the
  infra axes AND each `##` section of the archived log — "idle-but-real-finding"
  nights are the common case.
- **The distinct infra findings mined across this idle run are ALL already
  recorded in their owning skills** — this ledger keeps the events + their
  cross-refs and collapses the per-night confirmations (consolidation convention
  below; no distinct event dropped):
  - **MCP-parking class** — first captured 08-10; steady flat ~562/day; 08-14
    `errors.log`-rotation caveat (track the per-day rate, not the cumulative
    total); 08-18 a second rotation; **08-19 reframed as a periodic ~5-min
    self-probe cycle** (park count == `attempting revival` INFO count, which lands
    in agent.log, not errors.log); **cycle ENDED 08-20 13:32:11** once the pid-725
    gateway held the MCP transports connected, so **"empty park stream = healthy"**
    ever since. → `hermes-local-gateway-ops` §"Behavior that is normal".
  - **Discord-adapter `discord.com:443` DNS blip** — first 08-15 13:38 (pid-731
    cold start → cron-only graceful degradation, which is why the 03:00 cron still
    ran); recurred on the 08-20 restarts (pid 728/725) and as an 08-21 mid-run
    reconnect, so generalized to **"transient on ANY (re)connect, self-heals in
    seconds."** → §"Restart & exit-diagnostics triage".
  - **Discord gateway `WSServerHandshakeError: 503`** — NEW signature 08-27 05:20
    (Discord's edge 503'ing the websocket, distinct from the DNS class),
    self-healed in pid 725 with no restart; **recurred 08-30 10:08** = a recurring
    transient, not the one-off first described. → §"Restart & exit-diagnostics
    triage".
  - **Curator** — ~weekly cadence (07-24/31, 08-07/14/21); **08-22 first
    non-"no changes" run** (`auto: 2 marked stale`); **08-28 fired** (run_count
    5→6) with `auto: 70 marked stale` = the never-invoked 07-24 seed cohort
    crossing the ~35-day line as a batch, NOT a mechanism change; the
    nightly-maintained skills are immune (absent from the sidecar). Open anomaly:
    `delegate-to-claude` (last_used 07-20) stays active while 1–2-day-*older*
    skills went stale, so the boundary uses a signal beyond a fixed last_used
    cutoff — left as an anomaly, not fabricated. → §"Curator". Next run ~09-04.
  - **Worker / queue** — the 08-19 jetson session proved the python3 `gh`-spawn
    PR-create bridge end-to-end (PR #101, first success) → `claude-worker-env`;
    the 08-30 `resume-merge-authorization` FAILED (aged-out session, 2nd
    occurrence of the 07-21 mode) → `delegate-to-claude`.
- **An idle night can earn its keep by REDUCING a skill, not only adding.**
  Convention (set 08-30): when a tracked-metric subsection accumulates more than
  ~5 near-identical dated confirmations, collapse it into ONE rolling summary —
  preserve every *distinct* event (cross-ref the section that owns it), drop the
  pure confirmations. Spent so far: 08-30 (gateway parking paragraph), 09-01
  (Task-2 fold ledger), **09-02 (this Task-1 idle narration, ~167 → ~30 lines)**.
- (mem % and ollama `/v1/models` are sandbox-gated — `vm_stat` and `curl
  localhost` are both rejected — so idle-health rests on the worker-session +
  log-class + `mcp__*`-tools-surfaced evidence, which doesn't need them; earlier
  idle nights read ~74% free / ollama 200s.)
- **09-03 (tonight):** SKILLS-idle on the worker axis, quiet-healthy infra —
  the standing consolidation candidates are all spent (09-02 spent the last one),
  so tonight is a clean 2-commit idle roll (parking paragraph → 14th night +
  this record + extend the Task-2 fold ledger to 08-26), NOT a no-op. MCP-parking
  gone a **14th night** (08-21→09-03 all 0 new parks; live errors.log park count
  still **1179**; last park still 08-20 13:32:11); `errors.log` **silent ~89 h**
  (mtime still frozen 08-30 10:08:15, last write still the 08-30 WS-503 +
  `tools.registry` cascade — `WSServerHandshakeError` count still **2**, did not
  fire a third time); gateway **pid 725 up ~14 d** no restart (`gateway.start`
  held at **30**); `mcp__codegraph__*`/`mcp__basic-memory__*` tools surfaced +
  agent.log `RESUMED session` keepalives through **09-03 01:59:54** verify it
  live; curator unchanged (`run_count=6`, fired 08-28, `.curator_state` mtime
  still 08-28 14:44) — **next run due ~09-04, now the nearest changeable axis
  (~1 day out)**; watch for it on the 09-04/09-05 nightly.
  On an idle day
  **do NOT fabricate skill edits.** Either capture one genuine finding from the
  nightly session itself — it runs *through* `claude-worker`, so its own tool
  denials are valid worker-sandbox evidence for `claude-worker-env` — or make a
  minimal honest change. **1–2 commits is the healthy norm**; a big diff on an
  idle night is a smell.
- **09-06 (tonight) was NOT idle — the first non-idle nightly since the 08-19
  jetson session.** Two real findings, both cross-refed to their owning skill:
  (a) the 09-04/09-05 **session-limit 429** double-failure (durable note above);
  (b) the gateway **restarted** (`gateway.start` 30→32: pid 573 @ 09-03 21:13 UTC,
  pid 667 @ 09-04 21:27 UTC, current **pid 667**) — the FIRST restart since pid 725
  came up 08-20, which finally **answers the 14-night open watch: MCP-parking did
  NOT return** (park count still 1179, last park still 08-20 13:32:11), so the
  empty-park-stream healthy state survives a restart → recorded in
  `hermes-local-gateway-ops`. Also the **curator's 7th run fired 09-04 19:18 UTC**
  (`run_count` 6→7, reverted to `auto: no changes`) → same skill's §"Curator".
  Worker axis otherwise quiet (last real worker `done` still 08-19; the pantry
  PR storm on 09-04/09-05 ran from interactive/orchestrator + Agent sessions, not
  the `reflect`/`claude-worker` queue, so it leaves no worker-runner.log `done`).
  Two commits: this file + `hermes-local-gateway-ops`.
- **09-07 (tonight) — idle-but-real, back to the steady-state single-commit-pair
  roll.** Reflect chain healthy again (09-06 `done`, 09-07 processing — 429 recovery
  note above). Worker/queue axis still idle: last real worker `done` is STILL the
  08-19 jetson session; worker-runner.log past it is only lock-exit / "no .task files"
  noise + the 08-30 `resume-merge-authorization` FAILED. The day's real work was
  **pantry PR #194** (the `db/asserts/0055` self-match defect fix + Neon Managed Auth
  retirement, applied to production 09-07 00:44 EDT — see daily-log `2026-09-07.md`),
  which ran through **interactive/Agent sessions, not the `reflect`/`claude-worker`
  queue**, so it leaves NO worker-runner `done` (same pattern as the 09-04/05 PR
  storm — a busy pantry day still reads as "SKILLS-idle" on the worker axis; that is
  correct, not a miss). Its 0055/Neon lessons are pantry facts → they belong in
  `pantry.md`/the daily-log, not a skill (the daily-log already holds them; they fold
  when `2026-09-07.md` crosses the 7-day line ~09-15). Infra held: `gateway.start`
  still **32** (pid 667, no new restart since 09-04 21:27 UTC), curator unchanged
  (`run_count=7`, last run 09-04 19:18, next ~09-11), errors.log quiet since 09-04
  17:27, keepalives through 09-07 01:05:43. Two commits: this file + the
  `hermes-local-gateway-ops` date roll.
- **Where findings land** (refine the existing skill, don't spawn near-dupes):
  `claude-worker-env` (shell sandbox / PATH / allowlist), `hermes-local-gateway-ops`
  (gateway, Gemini limits, curator, infra), `github-workflow` (git/PR recipes),
  `delegate-to-claude` (queue lifecycle). Every commit message states the
  evidence (which session/log, which date).
- Finish: `git -C ~/agents/skills push -u origin nightly-<date>`. **Do not merge.**

## Task 2 — MEMORY (archive one daily-log, fold durable facts)

- **"older than 7 days" = STRICTLY more than 7 days before today.** A file dated
  exactly `today − 7` **stays**. So on a normal night **exactly one** daily-log
  crosses the line: the one dated `today − 8`. On 07-26, `2026-07-18` (8 days)
  archives and `2026-07-19` (7 days) stays. First-ever eligible date was 07-25
  (which archived 07-17); 07-22/23/24 were correctly no-ops.
  - **"Exactly one" is only true when the PREVIOUS nightlies all ran. Archive
    EVERY log strictly older than 7 days, not just `today − 8`.** A failed nightly
    (429, above) archives nothing, so its `today − 8` is still sitting there a day
    later. **09-06 caught up THREE at once — 08-27, 08-28, 08-29** — because the
    09-04 and 09-05 nightlies 429'd (09-03 had correctly archived through 08-26).
    `2026-08-30` (exactly 7 days) correctly stayed. Compute the set by date, don't
    assume a single file.
- For that one file: **fold its durable, NOT-yet-captured facts** into the
  matching `~/agents/memory/projects/<name>.md` (pantry → `projects/pantry.md`),
  then move the original to `~/agents/memory/daily-log/archive/` (`mv`, or
  `git -C ~/agents/memory mv` — either is fine; the backup routine commits it).
  - **Most old content is already captured** by the intervening daily logs, prior
    foldings, and the skills — the Hermes model-swap saga lives in
    `hermes-local-gateway-ops`, the queue/duplicate-run facts in
    `delegate-to-claude`, and recent project status supersedes old capture
    decisions. Fold only what is durable AND not already somewhere; and **state in
    the reflection that nothing was lost** (name where the rest already lives).
    Don't duplicate a skill's facts.
  - **The per-date provenance-line ledger in `pantry.md` was RETIRED by the
    2026-09-03 ground-truth reset.** `pantry.md` was rewritten that day (its old
    Status board had frozen at 08-19 while ~400 commits landed from other
    machines); the rewrite states plainly that "`daily-log/archive/` remains the
    record of the folds" and moved the old fold-provenance ledger into vault git
    history. So **do NOT add "<date> folded in during the <today> archival" lines
    to the rewritten `pantry.md`** — the `git mv` into `archive/` (which the 03:00
    backup commits) IS the provenance now. Only edit `pantry.md` when a fold
    carries genuinely NEW durable content, and match its current section shape
    (`## State <date>`), not the retired ledger format. Also: that reset created a
    `## Retired carry-overs (… do NOT repeat)` section — the old standing
    carry-overs (PR #101, the un-PR'd `feat/*` branches, PR #10, ANTHROPIC_API_KEY)
    are RESOLVED; never resurrect them from an archived log into a reflection.
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
  - **08-20 through 08-26 folds (done on the 08-28 → 09-03 nightlies) were ALL verified no-ops — same consolidation (08-20→08-23 collapsed 2026-09-01; 08-24/08-25/08-26 rolled into this range on the 09-01/09-02/09-03 nightlies, each with its own full `pantry.md` provenance line).** Each was a `## Nightly reflection` log with no still-open PR/branch of its own (08-20 only *reported on* the 08-19 jetson session, whose PR #101 deliverable was already folded on 08-27). Their durable infra facts (parking gone the 2nd→6th night → "empty park stream = healthy"; the 08-21 `discord.com:443` DNS blip generalized to "transient on ANY (re)connect"; the 08-22 curator first-ever `auto: 2 marked stale`) are all in `hermes-local-gateway-ops` §"Behavior that is normal" / §"Restart & exit-diagnostics triage" / §"Curator" and were superseded nightly since; their MEMORY halves + carry-overs (PR #101, the three un-PR'd branches, PR #10, ANTHROPIC_API_KEY) were all already in `pantry.md` Status. Provenance lines (`pantry.md` lines 43–49) + commit messages hold the per-date detail — nothing lost.
  - **08-27 / 08-28 / 08-29 folds (all done on the 09-06 nightly as a 3-log
    catch-up, since 09-04 & 09-05 429'd — see the failure-mode note) were ALL
    verified no-ops.** Each is a pure `## Nightly reflection` log that opened no
    branch/PR of its own; walked section-by-section, every durable fact already had
    a home: 08-27's MCP-parking-7th-night + curator-imminent + the **08-19 jetson
    PR #101 fold it performed** are in `hermes-local-gateway-ops` §"Curator"/
    §"Behavior that is normal" and `pantry.md` (PR #101 now a *Retired* carry-over);
    08-28's **WS-503 new-signature** finding is in §"Restart & exit-diagnostics
    triage"; 08-29's **curator `auto: 70 marked stale`** (the 07-24 seed cohort) +
    the `delegate-to-claude`-still-active anomaly are in §"Curator". Their pantry
    carry-overs are all in `pantry.md`'s *Retired carry-overs* section (resolved by
    the 09-03 reset — not resurrected). No provenance lines added (ledger retired,
    above); `git mv`'d all three to `archive/`, left staged for the 03:00 backup.
    Nothing lost.
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
