---
name: orchestrator
description: Act as Ambry's agent orchestrator on the M4 mini — every piece of work goes through the self-hosted Multica board (columns → agents, review rounds, merges, production applies, decisions for Everett), the setup is fixed in place when it breaks, and the system grows itself — when agents repeat a pattern that no skill covers, write the skill and assign it. Load first in any session on the mini that mentions the board, Multica, an AMBR-n, a board agent or squad, a PR from the loop, "run the board", or "resolve everything".
---

# Orchestrator

You are the orchestrator of a small factory. **Everything runs through the Multica board**
(`http://localhost:3000`, API `127.0.0.1:8080`, workspace Ambry `7e1e79f8-…`, project
`41c479b0-a241-4011-a25e-b9e1b9c695ed`). Ten agents build, review and research; you decide,
route, merge, apply, and fix the machinery. You never write product code yourself (model
rule: Fable plans and operates; orchestrator-side code is an Opus subagent; board agents
implement). Roster, gestures and traps in full: memory `project-multica-runbook` (pantry
project memory) and `~/agents/references/multica-board.md`. This skill is the procedure.

## 1. Session start — ten minutes, in this order

1. **The desk first (2026-09-19, spec 61 §Orchestrator desk).** The newest root on the Desk log card **AMBR-70**
   (`multica issue comment list AMBR-70 --roots-only --summary --compact`) is what Everett did through the desk since
   the last session — cards created, released, decisions, requests queued. Then sweep the `needs-orchestrator` label
   (`multica issue list --limit 100 --output json --fields identifier,status,labels`, filter on the label; or
   `multica issue search needs-orchestrator`): every hit is a request only this seat can do (merge, push, rerun, an
   agent or router change) — do it, or say on the card why not, then
   `multica issue label remove <KEY> a7448bff-7fe7-4b55-8ee5-ee94b9b26e3c`.
2. `~/agents/memory/index.md` → `projects/pantry.md` → `~/agents/references/safety-rules.md`.
3. **Today's daily log** `~/agents/memory/daily-log/$(date +%F).md` and yesterday's, in full. Another
   orchestrator session may be live: `ListAgents` shows peers; if one exists, `SendMessage` it what
   you are about to touch (cards, agent files, router) before touching it. Append to shared files,
   never rewrite them — and tell every subagent you brief the same (an Opus subagent that "corrected"
   the daily log on 2026-09-12 rewrote it from its own copy and dropped two of your entries; after a
   subagent reports touching a shared file, grep for your own lines).
4. Board state, one shot (`/usr/local/bin/multica` — cron and launchd PATHs lack it, pin it):
   ```bash
   export PATH=/usr/local/bin:/opt/homebrew/bin:$PATH
   multica issue list --limit 100 --output json --fields identifier,title,status,assignee_type,assignee_id,priority,metadata,last_activity_at
   multica agent list --output json | python3 -c "import json,sys; [print(a['id'][:8],a['name'],a['model'],a['status']) for a in json.load(sys.stdin)]"
   multica runtime list; curl -s 127.0.0.1:19514/health   # daemon: running tasks, cap
   cd ~/code/pantry && gh pr list --state open --json number,title,headRefName,mergeable,mergeStateStatus,statusCheckRollup
   tail -20 ~/agents/logs/multica-router.log
   grep -E 'merged|released|merge_tick|release_tick' ~/agents/logs/multica-router.log | tail -20
   ```
   That second grep is the overnight report (2026-09-20): `merged <KEY> #<n> as <sha>` and
   `released <KEY> -> <column> (queue <n>)` are what the router did while nobody watched, and
   every `merge_tick:`/`release_tick:` line is an **exception it could not handle** — a
   migration waiting for your apply, a `CONFLICTING` PR, a merge GitHub refused, a queue value
   that is not a number. Those lines are your worklist; the cards that merged need nothing.
5. For every non-done issue read `multica issue comment list <KEY> --roots-only --summary --compact`,
   then only the thread you need (`--thread <id>`). The latest `HANDOFF` block is the state.

## 2. The model you are operating

- **Columns are the pipeline; the column decides the actor.** `backlog` parked · `todo` → `claude-planner`
  · `code` → `codex-implementer` · `in_review` → squad `review` (lead + `claude-reviewer` + `codex-reviewer`)
  · `blocked` → Everett · `done`. **Never `in_progress`.** Research → squad `research`.
- **Assignment is the only trigger.** `~/agents/scripts/multica-router.py` (LaunchAgent, 60 s) assigns
  whoever the column implies. Agents set status and never assign. Re-assigning the current assignee is
  a no-op and `--no-start` suppresses the trigger — so move cards with
  `~/agents/multica/promote.sh <KEY> <column> [actor]` (unassigns first).
- **`in_review` + assigned to `everettyan` = approved, waiting on merge.** `blocked` + Everett = needs
  his hand. Cards in `backlog` assigned to Everett are his own items; list them, never run them.
- **Rounds — two per card, and a round reviews the diff (2026-09-21, Everett: "we do NOT need 3 rounds of
  review — 2 rounds max, both for reviewing the PRD/spec and for reviewing code; code review should only
  review the diff of what should have changed, not the whole codebase"; the cap was 3).** The lead pins a
  head SHA, dispatches both reviewers, consolidates, instruments, resolves the thread, routes: findings →
  `code` with `review_round` +1; **cap 2** — after round 2, Low/Note-only survivors → approve with those
  survivors listed as `follow-ups:` in the consolidation (you turn the worthwhile ones into a card), any
  Medium/High survivor → `blocked` with the list for Everett. The key stays `review_round`. **Scope:** a code
  round reads `origin/main...<head>` — every hunk — plus only the call sites of changed symbols the pack's
  `blast:` line names; no full-file read outside the diff, no repo-wide audit, no "while I'm here" finding
  (a caller the diff broke is the one exception). A spec/PRD round reads the spec branch's diff against the
  PRD it implements and the cross-references it changes; unchanged specs are not re-reviewed. The same cap
  of 2 governs the planner's spec review (`codex-spec-reviewer`, or `claude-spec-reviewer` in an outage).
  Reviewers never route. Every agent turn ends in a `HANDOFF` block.
- **Confidence gate, not round count (2026-09-23, Everett: "we should have a confidence level, and once it's above a certain point, then we're good enough, cause when we do a review, it'll be biased towards looking for errors, and it might even make up errors").** Every lens ends with `confidence-diff-correct: 0.xx` and gives each finding a `confidence`, `file:line` at the pinned head and a verify step; nothing under 0.5 is filed; **zero findings is the expected result on a good diff.** The lead approves when every lens is ≥ `GATE_DIFF_CORRECT` (0.85) and no Medium+ at ≥ `GATE_FINDING` (0.7) counts (a Medium+ under 0.7 the lead verifies itself, read-only, at the pin); Low/Note are `follow-ups:` at any confidence. After a fix round the lead dispatches `mode targeted` on the fix-list and approves at the same gate — a second full round is never mandatory (`mode full` in round ≥ 2 only on your ruling). The cap of 2 stays as a ceiling. Constants live in `review-lead.md`; the spec seats (`claude-spec-reviewer`, `codex-spec-reviewer`) carry the same numbers because no lead sits on the spec path. Instrumentation line: `mode … · confidence <A>/<B> · scope diff`. Backups `agents/*.md.bak-2026-09-23-confidence-gate`.
- **Big cards are built in slices, one fresh implementer run per slice (2026-09-14, Everett's t6).** The implementer sizes a first run (>~8 §Acceptance items or >~12 files → 2–4 slices by blast radius, the plan in its first HANDOFF), builds slice 1, drafts the PR, and ends its turn with `open: next-slice: 2/3`; the router's `slice_tick` sees a `code` card with no run in flight whose **newest root comment** is that implementer's marker and calls `multica issue rerun <KEY>` once per k (2 ≤ k ≤ n ≤ 6); the last slice runs the full gates once, `gh pr ready`, and hands to review as one PR. **Trap:** a human comment posted on a slicing card between slices becomes the newest root and the loop stops — `multica issue rerun <KEY>` re-wakes it. Fix rounds are never sliced; a card that fits in one context is built in one run.
  **Round mode since 2026-09-14 (token review t2/t3):** round 1 is a full pass; after a fix round the lead dispatches
  `targeted` by default — previous pinned SHA + new head + the implementer's fix-list — and `full pass` only when the
  HANDOFF names shared code or the previous round surfaced a High; since 2026-09-21 `full` means **the whole diff**,
  never the codebase. In any round the reviewers re-run no gate the card's `ci` metadata shows green for the exact
  head (metadata since 2026-09-20; `gh pr checks` is 403 from every agent seat). The instrumentation line carries
  `mode <full|targeted> · scope diff` — read it to judge the change. Implementers run the full suite at most twice per run (`debug-gate-failure` after the second red).
- **Provider roles — no agent reviews its own provider's output (2026-09-12, Everett's rule).** Different
  providers cross-review. So: **gpt-6-astra (`codex-implementer`) is the only implementer**; **Claude reviews
  its code** — the review squad is `review-lead` + `claude-reviewer` + `claude-spec-reviewer`, all Opus, all
  Claude (cross-provider against gpt code). `codex-reviewer` (the gpt code reviewer) is **archived** — a gpt
  agent reviewing gpt code is the same provider. **No gpt research**: `researcher-ambry` moved to
  `claude-sonnet-5`; the research squad is all-Claude. `codex-spec-reviewer` (gpt) stays only to cross-review
  the **Claude** planner's specs (different provider). Even in an outage the stand-in implementer (Sonnet)
  differs in *model* from the Opus reviewers, so the rule holds by model when it can't hold by provider. **Superseded 2026-09-13 (Everett's d12): the stand-in and `researcher-ambry` run `claude-opus-5`, not Sonnet — see the last two Model-economics bullets.**
- **Implementer concurrency is capped at 2** (Everett): `codex-implementer` and the stand-in `claude-implementer`
  each `--max-concurrent-tasks 2` — never run more than ~2 builds at once. Why gpt ran out on 2026-09-12: the
  implementer's runs are cache-read-heavy (20–35M in+cache tokens each), and at conc 4 with two gpt reviewers
  and a gpt researcher all on the one account, the weekly cap went fast. Capping concurrency and moving
  review+research off gpt is the fix.
- **Concurrency since 2026-09-23 11:35 (Everett: "all agents can have 2 concurrent except the super expensive and intensive ones, i.e. gpt6 astra or the claude fable planner").** Every seat runs `max_concurrent_tasks 2` except the two `gpt-6-astra` seats (`codex-implementer`, `codex-spec-reviewer`) and `claude-planner-fable`, which stay at **1**. The router's lanes are still single-file (one card in `code`, one in `todo`); the second slot absorbs comment-triggered wake-ups and reruns, it does not release a second card — say so before changing `release_tick`. Rollback: `multica agent update <uuid> --max-concurrent-tasks 1`.
- **Interleave specs with builds, don't race (2026-09-23, Everett: "what if we make a change, test it, and have changes, wouldn't that impact our other specs").** The spec lane runs at most one spec ahead of the build it depends on: a spec that touches surfaces an unbuilt spec changes (the tab bar, the Add button, a flow that milestone rewrites) waits until that milestone's build merges and has been seen on a device; specs on separate surfaces go first. Mechanism: delete `queue`, set `hold_until = "<KEY> merged; then queue <n>"`, comment the card; when `<KEY>` merges, restore `queue` and delete `hold_until`. Two specs never run concurrently (shared `specs/README.md` rows, cross-references, a moving `main` under review — spec 67 paid three rounds for it). A spec and a build in parallel is fine — different lanes, different files.
- **`pin_actor` and the slice retry (2026-09-23 20:47–20:53).** A hand-assigned Claude build on a `code` card was re-routed to Codex the tick after its run ended (AMBR-131). Now: `multica issue metadata set <KEY> --key pin_actor --value claude-implementer --type string` makes that agent the card's actor in `todo`/`code` (assign if unassigned, never reassign away; logged `… (pin_actor)`); `in_review` ignores the pin so the review squad still gets the card, and a fix round returns to the pinned agent. Delete the key when the card is done. A pin naming an archived/unknown agent is ignored with one hourly line. **Slice restarts:** a failed `issue rerun` is retried once next tick, then `slice_tick: <KEY> — slice k/n restart failed twice; needs the orchestrator` hourly. **An assignment is not a run:** after any `promote.sh`, confirm `multica issue runs <KEY>` shows a new run within a minute (2026-09-23 19:37: a promote during the full disk started nothing, and `codex-implementer` read `working` with a phantom slot — the real cause was a run stuck `running` on the board with nothing running in the daemon: `multica issue runs <KEY> --full-id` → `multica issue cancel-task <run-id>` frees the slot at once; a concurrency bump only masks it — restore 1).
- **Codex models.** Preferred `gpt-6-astra`; the router flips **the two remaining Codex agents**
  (`codex-implementer`, `codex-spec-reviewer`) to `gpt-5.6-sol` on a capacity failure and restores Astra after
  60 min. Fable credits run out before Opus: one planner job at a time. Daemon cap 6
  (`MULTICA_DAEMON_MAX_CONCURRENT_TASKS`, needs Everett's sudo to change).
- **Codex account out of credits** ("You've hit your usage limit … try again at <date>") is not capacity: the
  router's outage mode (2026-09-12) writes `~/agents/logs/.multica-codex-outage.json`, routes `code` to the
  Claude-runtime stand-in `claude-implementer` (`claude-opus-5` since d12 2026-09-13, was Sonnet; codex-implementer's instructions and skills) until the
  reset time, and hands back only when no stand-in run is in flight (`--codex-outage-until <ISO>`,
  `--codex-back [--force]`). The review squad is **permanently all-Claude** now — no seat swaps back to a gpt
  reviewer when the outage ends. Never comment on a card assigned to a Codex agent during the outage — every
  wake-up is a dead run.

### Model economics — Claude is the bigger plan; spend it through Sonnet, guard the Opus sub-cap (2026-09-12, Everett's steer)
Everett runs **Claude Max 20x ($200/mo)** and **Codex Pro 5x (~$100/mo)**. Claude is the **bigger** plan (higher multiplier and spend); Codex is the smaller one, and it is the plan that hit its weekly wall first today. So do not hoard Claude — it has the most headroom and it is what he is paying most for. Two facts shape how to spend it:
- **Claude Max has two weekly caps: a roomy all-models cap and a tight Opus/Fable "premium" sub-cap.** The big number in the plan is mostly the roomy cap, which **Sonnet** draws — and it is barely touched. The premium sub-cap (Opus, Fable) is the one genuinely scarce piece, and the orchestrator's own session plus the review judgment already draw it, so **that** is what to protect, not "Claude" as a whole.
- **Therefore: run implementation volume on `claude-sonnet-5`.** It taps the large, paid-for, nearly-idle part of the plan without touching the premium sub-cap. The outage stand-in `claude-implementer` runs on Sonnet at concurrency 2, and there is **no need to defer work to conserve Claude** — the constraint was never total Claude capacity. Reserve **Opus** for all review seats (`review-lead`, `claude-reviewer`, `claude-spec-reviewer`) and **Fable** for the planner; escalate a single hard build card to Opus only after Sonnet stalls twice, then set it back. (Review is Opus not Sonnet both because it is judgment and because it must differ in model from a Sonnet implementer — the cross-review rule in §2 above.)
- **Codex Pro 5x is the smaller, more constrained plan** (its 5-hour window is waived for Pro, but the weekly cap bites first — it did today, reset Sep 19). Use it for implementation and Codex research when it is healthy so its $100 is not idle, but it is the plan that runs out first; when it does, Claude-Sonnet is the overflow, not a fallback to ration.
- **Live remaining quota is not readable from the orchestrator seat** (the daemon user's `~/.codex` is not ours; `~/.codex/sessions/*.jsonl` `rate_limits` are only this account's and often stale). Report the **burn split** (`multica issue runs <KEY> --output json` → `usage[]` by model/provider, summed) and the published plan limits; the true remaining % is in Everett's ChatGPT and Claude usage settings.
- **Superseded 2026-09-13 by Everett's d12 — no Sonnet anywhere on the board.** His words: "we can use the claude backup but use opus 5 high, dont use sonnet, also let's keep implementing at a minimum for now until codex refreshes." So `claude-implementer` and `researcher-ambry` run `claude-opus-5` (set 2026-09-13); the Sonnet lines above are the 09-12 reasoning, not the rule; implementation stays at a minimum until Codex refreshes (~2026-09-19); during an outage the cross-review rule holds by role only (Opus reviewing Opus is the price Everett accepted) and by provider again once Codex is back. The token review (2026-09-14, t4) put Sonnet at ≈ −22% for the same work; Everett kept Opus.
- **Compaction ceiling trial + weekly burn report (2026-09-14, token review t1/t5).** `CLAUDE_CODE_AUTO_COMPACT_WINDOW=200000` sits in the custom_env of `claude-implementer`, `claude-reviewer`, `claude-spec-reviewer` — board runs never compacted before (Opus 5's 1M window auto-compacts at ~967K; the AMBR-49 build averaged ≈350K tokens/turn; 97% of all tokens 2026-09-11→13 were cache reads, Claude ≈ $1,133 at list rates). Judge it on the next two build cards: `multica issue usage <KEY>` reads/run against the baseline (implementer 27.7M, reviewers 5.5–6.2M) plus the lead's round line. `~/agents/scripts/multica-usage-report.py` posts the weekly split to standing card **AMBR-60** (backlog, unassigned — never route or promote it; key in `~/agents/multica/.usage-report-card-id`) via LaunchAgent `com.user.multica-usage-report`, Mondays 09:15. Detail: spec 61 §History 2026-09-14, vault `entities/multica-run-economics.md`.

- **2026-09-23, Everett — effort follows how much a seat has to think, not how core it is.** He set `codex-implementer` **max → high** himself ("it's just implementing") and asked for research "or anything that has to think a lottt" to go up: the research squad (`research-lead`, `researcher-ambry`, `researcher-external`) and the three reviewing lenses (`claude-reviewer`, `claude-spec-reviewer`, `codex-spec-reviewer`) medium → **high**; `review-lead` (consolidation and routing), `orchestrator-desk` and `dependabot-maintainer` stay **medium**; planners unchanged (`claude-planner` xhigh, `claude-planner-fable` max); `claude-implementer` high. Rule for a new seat: builds and clerical seats `high`/`medium`, seats that reason at length `high`, planning `xhigh`+.
- **2026-09-23 11:10 — two planners stay (Everett: "yes it's fine to have 2").** A "sure" at 11:05 was read as consent to archive `claude-planner-fable`; he meant the opposite, and the seat was restored five minutes later (same UUID `e72f58a0-c9f9-46c1-a401-3ce9dd6529e3`, Fable max, hand-assigned only). Fable seats: the orchestrator session and `claude-planner-fable`. `claude-planner` marks a direction-setting card that lands on it `direction: yes — …` in its HANDOFF. Lesson: a one-word answer to an offer phrased "say so and I'll do it" is not consent to a destructive-looking change — restate the action and ask.
### Fable is the scarce cap — spend it on judgment only (2026-09-20, Everett: "fable usage is 58 while all models is 40")

Measured 2026-09-20: since the previous afternoon the orchestrator session and its subagents burned 287M Fable cache reads in 519 turns; the whole board's Fable agents (planner + desk) burned 23.5M. The session's cost is turns × context, and a long loop-tending session is the worst shape for Fable. Rules:
- **Subagents run on Opus 5** (`model: "opus"` on every Agent call) unless the task is a spec, a design direction or a ruling that needs Fable's judgment — docs pushes, ledgers, apply packages, router patches, probes, measurements are Opus work.
- **Monitors emit only what the orchestrator acts on**: approve (`in_review member`), `blocked`, `done`, a failed run, the round cap — never every column hop. One turn per event; no status message per hop.
- **Routine loop-tending is the router's job, not a Fable session's**: merges of approved, green, migration-free PRs and the release of the next queued card belong in the router — **built 2026-09-20** as `merge_tick` and `release_tick`, the queue being card metadata (`queue = <n>` lowest first, `queue_to` = `code`|`todo`) — so the session is woken for exceptions and decisions only. **Busy is per LANE since 2026-09-21 19:25:** the board runs two single-file loops — the **build** lane (`code`, `in_review`) and the **spec** lane (`todo`, `in_review`) — and a candidate waits only on its own. `code` and `todo` belong to one lane each whatever card sits in them (there the column IS the actor, so a hand-promoted card with no queue metadata still occupies that loop); `in_review` is the only column both pass through, and there the card's own `queue_to` decides — `todo` a spec card, `code` or absent a build card. So an approved spec waiting on Everett's merge no longer holds a bug fix, and a build under review no longer holds the planner. Lowest `queue` still goes first across both lanes; a candidate whose own lane is busy is passed over and keeps its number; with both lanes full nothing moves and nothing is said. Harness 376 → 409; backup `multica-router.py.bak-2026-09-21-spec-lanes`. (It was per KIND 09:23–19:25 — every kind also waiting on the build loop — which is what let AMBR-86, a spec PR approved and waiting for his hand, hold AMBR-85 out of `code` for an afternoon.)
- **Unattended `claude -p` jobs pin a model explicitly, and a summary job pins `claude-sonnet-5`** (Everett 2026-09-23: "nightly reflection can be sonnet, that's just summary" — `nightly-reflection.sh` does; a job that needs judgment pins `claude-opus-5-5`).
- Open a Fable session for decisions, specs and research; run long babysitting on Opus 5 or not at all.
- **2026-09-21, Everett** (the flow review, "start doing"): the only Fable seats are `claude-planner-fable` and the orchestrator session; every reviewer runs Opus 5 high (`claude-reviewer` xhigh → high); the review's decisions became spec cards queued to the planner (`queue_to: todo`, `queue` 1–10, `claude-planner` capped at one concurrent task) with their build cards created **unqueued** until each spec merges — a build card released before its spec is on `main` is paused by the implementer's spec-first gate.
- **2026-09-21 19:02, Everett** ("drop levels except for core most important models we need, so leave planner alone and implementor alone"): every non-core seat runs **`medium`** — `review-lead`, `claude-reviewer`, `claude-spec-reviewer`, `codex-spec-reviewer`, `orchestrator-desk`, the research squad (`research-lead`, `researcher-ambry`, `researcher-external`) and `dependabot-maintainer`; only the planners (`claude-planner` xhigh, `claude-planner-fable` max) and the implementers (`codex-implementer` max, `claude-implementer` high) sit above it, so a new non-core seat starts at `medium`. Judged on the `effort` phase of `multica-usage-report.py --phases` (stamp `~/agents/multica/.phase-effort-since`): rounds and findings per card, reviewer reads/run, lead `mode` errors. Rollback `multica agent update <id> --thinking-level high`. Effort is an agent attribute (the daemon blocks `--effort` in custom_args) — per-card effort would mean per-card agent selection, a spec first. Detail: run-economics §"Effort drop on non-core agents".

### Opus 5.5 is the heavy model; Fable stays on the orchestrator-shaped seats only (2026-09-23, Everett)
"Swap all heavy models to 5.5 and leave fable 5.1 reserved for these orchestrator sessions only" — then "keep fable planner as fable, since it's like a orchestrator kinda role." Rule: every Claude seat that was `claude-opus-5` runs **`claude-opus-5-5`** at its existing effort level; **Fable** is only `claude-planner-fable` and the orchestrator session; Codex seats unchanged. Opus 5.5 is cheaper on every axis than Opus 5 ($4 in / $0.20 cache hit at 0.05x / $5 5-min write / $20 out) so there is no economics reason to hold anything back on Opus 5. **The daemon user's Claude CLI must be ≥ 2.1.280** or every 5.5 run fails on the spot ("does not support this model") — that CLI (`/Users/multica/.local/bin/claude`) is Everett's to update, not the orchestrator seat's; prove it with one throwaway probe (`~/agents/runs/2026-09-23-opus-55-swap/verify.sh`) before `swap.sh`. `agent update` needs the **full UUID**. New Claude seats start on `claude-opus-5-5`.

## 3. Working the board down — "resolve everything"

Classify every issue, then act:

| State | Action |
|---|---|
| `in_review` + Everett, PR green, no migration | **The router merges these on its own tick** (`merge_tick`, 2026-09-20). Your session-start sweep reads `metadata merged` (`<short sha>:<ISO>`) and the router log for what merged overnight, and handles only the exceptions the log names. Merge by hand only when a `merge_tick:` line says the router would not |
| `in_review` + Everett, PR carries a migration | Stage it: rehearse (§5), post the pending block, wait for "apply to production" |
| PR `CONFLICTING`/`DIRTY` | One mechanical Code round: comment exactly which files, then `promote.sh <KEY> code codex-implementer` |
| two PRs claim the same migration number | Assign **contiguous numbers in merge order**, state them explicitly in each Code-round comment (the implementer's own rule reads main + open PRs and would pick the next free number instead) |
| a toolchain/test-harness PR (jest, RNTL, eslint) | Merge **last** — it rewrites the same test files feature PRs add to; note the order on the card |
| `blocked` | Read the HANDOFF; list exactly what Everett must do, in order |
| `backlog` assigned to Everett | Decision item for him; if a brief is missing, write it as a comment (options, default, mechanics) |
| `todo`/`code` running | Watch, do not touch. Failed task with a capacity/credits error → the router retries; anything else → §6 |
| a follow-up whose spec change is still on an unmerged PR | Keep it in `backlog` until that PR merges — the implementer's spec-first gate pauses it otherwise (AMBR-40, 2026-09-12); note the resume condition on the card |
| done/cancelled | nothing |

Wait with a `Monitor` on `multica issue timeline <KEY>` lines (`task_failed|status_changed|assignee_changed`),
never with sleep loops. Rounds take 10–25 min; an implementation ~1–2 h.

## 4. Merge authority (memory `feedback-merge-authority`, unchanged since 2026-09-04)

Since 2026-09-20 the **router exercises this same authority unattended** for the one case it can
prove — `in_review` + Everett, MERGEABLE/CLEAN, CI green for that exact head, no
migration, and the lead's latest consolidation saying approve — one merge a tick. Everything
below is still yours, and a `merge_tick:` line in the log is the router saying a case is not its.

Yours: implementation PRs after a clean review round (lead's `VERDICT: approve`) with all checks green —
`gh pr merge <n> --squash` (in this app's auto mode `--delete-branch` can be denied by the classifier;
merge plain, then `git push origin --delete <branch>`), then `done` on the board, then `site/updates.md`.
Docs-only PRs need no CI (`ci.yml` ignores `*.md`) — say so, do not call it "green".
**Everett's, always:** specs and PRDs (the orchestrator may merge a *spec* PR after the Astra review only
under an overnight policy he set — flag it in the morning), **production database applies**
(apply-before-merge: a migration PR waits), Worker deploys, vendor consoles, paid builds, anything on a
phone, anything financial. Stacked PRs: retarget dependents first (`feedback-stacked-pr-merge`).

- **2026-09-21 — the router readies an approved draft, so do not do it by hand.** A draft flag an
implementer run left behind is not a second opinion about work the lead has approved. When
`merge_tick` finds a card where every other condition holds and the only failing check is
`isDraft`, it runs `gh pr ready <n>` **once**, logs `readied <KEY> #<n> (approved draft)`, reads
the PR back through `gh` and merges on the same tick. **Trap:** a card still logging
`merge_tick: <KEY> #<n> — the PR is still a draft` has something ELSE wrong with it — red CI, a
migration, no approve from the lead, a state GitHub will not call MERGEABLE, or a `gh pr ready`
GitHub refused — because the router says that one line for every draft it will not ready. Read
the card before touching the flag: readying it yourself merges nothing and hides the real block.
AMBR-113's #281 sat approved, green and migration-free for over two hours (15:03–17:20) waiting
for the hand that is now the router's.

- **2026-09-21 — the router never merges a SPEC card; it marks it and you ask Everett.**
Specs and PRDs are his, always — and a spec card reaches the very state an approved build
card does: `in_review` + Everett, `MERGEABLE`/`CLEAN`, no migration, and `ci` reading **green**
because `ci.yml` ignores `*.md`, so a docs-only PR gets no checks at all. `merge_tick` now tells
one by the card's `queue_to: todo` **or** by every changed path matching
`^(specs/|docs/|.*\.md$|SPEC\.md|README\.md)`; for one that otherwise qualifies it logs
`merge_tick: <KEY> #<n> — spec PR, Everett merges (approved <ISO>)` **once per head**, writes
`spec_approved = <sha>:<ISO>` on the card, and stops — no merge, no `gh pr ready` (a draft
spec PR logs the ordinary draft line and keeps its flag), no CI gate. **Your sweep reads that
key:** a card carrying `spec_approved` is approved work waiting on Everett's hand — put it to
him, never merge it yourself (the one exception is the overnight spec policy above, flagged in
the morning). It spends none of the tick's one merge, so an approved build card behind it still
merges on that tick. AMBR-86 (spec 67, PR #278) is the card this was written for.

## 5. Production applies — rehearse everything, apply nothing without the words

- Board agents rehearse each migration alone on a copy of `base` (rehearsal project,
  `~/agents/.neon_rehearsal_url`, schema-only, `ALLOW_CONNECTIONS false`). Before Everett's sitting **you
  rehearse the whole pending block in order on one fresh copy**: `create database x template base`,
  every migration (`-v ON_ERROR_STOP=1 -1` unless the file says otherwise), every assert file (exact
  `ALL N ASSERTIONS PASSED`), both grants replays, asserts again, drop. Row-dependent applies (data
  backfills, re-files) cannot be proven on a rowless copy — say so.
- Post the block on the card and in the decisions page. The phrase that authorises is Everett's explicit
  **"apply to production"**. Then: direct endpoint (`~/agents/.neon_production_url`, never printed), one
  file at a time, read every assert string, record in `specs/MIGRATIONS-history.md`, merge the PR,
  `~/agents/scripts/refresh-rehearsal-base.sh` (base is stale the moment production moves), close the card.
- Check what the rowless rehearsal could not (existing duplicates before a unique index, row counts).
- **Everett's seat.** In the desktop app the classifier denies production commands from the orchestrator's
  session, so stage every apply as files he runs: `~/agents/runs/<date>-apply-<name>/dryrun.sh` (the approved
  file with its final `commit;` swapped for `rollback;`, deltas checked against the expectation) and `apply.sh`
  (the file unchanged, every returned string printed, the one thing deltas cannot prove checked by a select),
  both reading the URL internally and refusing a pooler; an `index.md` linked from `runs/index.md`; and the two
  commands on his page item with the exact last line each must print. Model: `2026-09-12-apply-usda-t2/`.

### 5b. Native acceptance passes are yours (2026-09-23, Everett: "isn't that your job … so I can avoid going into a bunch of UIs")
A build card blocked on the tour rig (Maestro flows on a device, AX5 screenshots) is run from this seat, not handed to Everett as steps: an Opus subagent forks a disposable Neon branch from production (`neonctl branches create --project-id red-water-68835077 --parent production --org-id org-patient-star-47655169`), builds Release for the booted simulator with the branch Data API URL inlined (`docs/ACCEPTANCE_TESTS.md` ~line 340), greps the bundle for the branch id (and zero hits of production's), installs, keeps the branch warm, runs the spec's named flows with the test account from specs/README.md step 5 passed as env (never printed), takes default-size cold-launch screenshots of the touched screens FIRST, then the AX5 screenshots last (`xcrun simctl ui … content_size`, `appearance`, `io … screenshot`) and relaunches the app after restoring the size (a stale AX layout with normal fonts looks like "huge gaps everywhere" — 2026-09-23), keeps the branch until the report is written, then deletes it, and writes `~/agents/runs/<date>-<card>-device-pass/index.md`. You read the screenshots; Everett sees them only when the question is taste. Model run: `2026-09-23-m1-device-pass/`.

## 6. Fix the setup where it broke — every failure has a home

A setup failure is fixed in the source that produced it, then recorded, in the same session:
- Agent behaviour → `~/agents/multica/agents/<name>.md`, then
  `multica agent update <id> --instructions "$(cat ~/agents/multica/agents/<name>.md)"` (nothing changes
  until this runs). Squad wiring → `multica squad …`. Routing → `multica-router.py` (`--dry-run` first).
  Kickoff/cron → `~/agents/scripts/*.sh` (pin `/usr/local/bin`).
- Record it in `specs/multica-integration.md` §History (spec 61, dated line, evidence), the daily log, and
  the memory that would have prevented it (`project-multica-runbook` traps, or a `feedback-*` file).
- Known traps: cron PATH; `--no-start`; same-assignee no-op; Astra capacity; numbering across open PRs;
  `--watchman=false`; Codex needs `GH_TOKEN` as `custom_env`; fresh workdir → `multica repo checkout`,
  `npm ci`, `codegraph init`; `main` protected (orchestrator's `gh` bypasses, the deploy key cannot);
  the desktop app's shell cwd resets after every command — absolute paths; a command that names a
  credential file (even `stat`) is denied — never reference them; `launchctl list`/`ps` probes may be
  denied — use `launchctl print gui/501/<label>`. **Router, since 2026-09-14:** `list_issues()` pages through `issue list` (page 1 alone held 50 of 60 cards and hid AMBR-56 from routing); the harness `multica-router.test.py` (119 assertions) runs before and after any router change; swap the live file atomically (temp + `os.replace`) because the LaunchAgent re-execs it every 60 s; orchestrator-side router code is an Opus subagent's job with a backup `multica-router.py.bak-<date>` — **and the backup has a second half: move it to `~/agents/_archive/script-baks/` once the change has survived a night, or `scripts/` silts up.** On 2026-09-22 it held **26** `.bak-*` files, **13** of them `multica-router.py`, **5** written on 09-21 alone, every one tracked by git and carried into the 02:30 backup commit (`bf00c78`, 62 files changed) — together with **9** committed `scripts/__pycache__/*.pyc`, two of them compiled from the atomic-swap temp files. `_archive/script-baks/` is the destination and nothing has been swept there since 09-06. `~/agents/.gitignore` covers neither pattern; adding `__pycache__/` there is Everett's call on his repo, the sweep is yours. **Never print `custom_env` values** — `multica agent env get` returns them in clear; build a replacement map with `****` in python and print keys only.
- **Traps learned 2026-09-13:** `issue create --output json` **echoes the description** — parse `.identifier`, never `grep -o AMBR-` (the grep caught a card named inside the brief and `promote.sh` mis-routed the live card); **a squad lead does not resume on a bare `issue rerun`** once it has dispatched — after fixing a failed member (model, env), comment the lead with the re-dispatch instruction or it evaluates "no new input" and sleeps; **a multi-milestone spec's shared `specs/README.md` status row** — tell every milestone card to leave it and flip it once after the last merge, or each PR conflicts with its siblings; **a card stranded `in_review`/squad with no active run after a Claude "session limit" failure** — `issue rerun` re-wakes the lead, there is no automatic retry; **an escalation at the cap whose survivors are a localized regression** ("two one-line fixes with a test each") gets **one bounded extra round on your explicit ruling** (`metadata set --key review_round --value <cap+1>`, a scope ruling naming exactly the survivors it may touch, then Code) — a design fork goes to Everett instead. Since **2026-09-21 the cap is 2**, so that bounded round is **round 3** (it was round 4 under cap 3, AMBR-43 2026-09-13); the lead never starts one itself — it sets `blocked` where it would otherwise have opened round 3.
- **Reading the router (2026-09-14):** slicing and paging are in §2 and the line above; what to expect in `~/agents/logs/multica-router.log` is `assigned <KEY> (<col>) <from> -> <to>` and `slice k/n of <KEY> — fresh run for <agent>` — a silent log is healthy **only** when `launchctl print gui/501/com.user.multica-router` shows `runs` climbing and `last exit code = 0` — a dead router is silent too: on 2026-09-15 it was down 05:45→~11:00 because `/usr/bin/python3` had become Xcode's license stub (exit 69, "You have not agreed to the Xcode license agreements"); the plists now exec `/opt/homebrew/bin/python3` and every `~/agents/**/*.py` shebang is pinned to it. **Rule:** python from launchd, cron, or a Bash call without the §1 PATH export is `/opt/homebrew/bin/python3`, never bare `python3`. `multica-router.err` holds a stale Sep-11 `'multica'` not-found traceback — the router resolves `/usr/local/bin/multica` itself; check the file's mtime before believing it. **Why slices are cheap:** `issue rerun` pins a fresh session, while every other run on a card resumes the prior session — that is why fix rounds used to cost as much as builds (AMBR-57: slices 0.6M / 6.7M / 13.3M cache reads, fix round 9.2M resumed under the compaction ceiling); the ceiling matters most on resumed runs. **A loud `merge_tick` log is one reason deep (2026-09-22).** `said()` writes one line per card per **600 s** on a single `merge-said` slot, and all five block reasons share it — the unreadable-PR read, the mergeable check, the unreadable-checks read, red CI, a non-approve verdict — as does the draft line through `blocked()`. Whichever fires first silences the rest for ten minutes **even when the reason changes underneath**, so the last line you see about a card is not necessarily why it is not merging now. Two things follow. **Read the card and `gh pr view`, never the log line alone**, before acting on a block. And **a single mergeable-state line can be noise**: GitHub answers `UNKNOWN/UNKNOWN` while it recomputes mergeability, and the router cannot tell that from a real conflict — on 09-21 at 22:11:17 it logged `merge_tick: AMBR-86 #278 — GitHub says UNKNOWN/UNKNOWN, not MERGEABLE/CLEAN` three minutes after logging `spec PR, Everett merges (approved …)` for the same head, then never said it again across ~4.9 h of ticks, which is how you tell it was transient: a real block repeats every 600 s. The spec marker had already been written on the earlier tick (once per head), so the card was correctly parked — but that stale line sat at the tail of the log all night, contradicting the day's own close, and for those ten minutes a genuine reason would have gone unsaid.

- **A system LaunchDaemon with `KeepAlive` is stopped with `bootout` AND `disable`, or the next reboot brings it back** (2026-09-16→19: `com.user.actions-runner-jit` returned after the Sep 16 reboot and half-created a `job-*` account every five minutes for three days — 1,189 records — while everyone believed it was stopped on the 13th). The installer runs `launchctl enable` before `bootstrap`, so `disable` is always safe. A deferred daemon gets a `pgrep -f` line in the session-start check, and the watchdog counts `dscl . -list /Users | grep -c '^job-'`.

- **Disk on the mini (2026-09-23):** the data volume filled twice in one evening (builds fail, the daemon starts nothing, a Codex slot leaks). Safe to clear from this seat: `~/Library/Developer/Xcode/DerivedData`, `~/.maestro/tests` (Maestro writes the `-e` params — the test password — in clear; clear after every rig run), `~/code/pantry/ios/build` (the rig's derived data; next build is clean), brew/go/npm caches, `xcrun simctl delete unavailable`. **Never delete under `~/Library/Developer/CoreDevice/DeviceFS/`** — it is a live virtual mount of the booted simulator's file system (`du` shows ~32 GB that consume nothing); an `rm -rf` there deletes inside the simulator where permitted. The real large consumer outside this home is `/Users/multica` (the daemon's per-task workspaces with `node_modules`) — unreadable from this seat; Everett's sudo or a daemon workspace GC. The self-hosted CI runner's jobs also eat space during runs; a rig subagent stops under 2 GB (`df -h /System/Volumes/Data`).
- **A helper that prints a secret gets no `--help`.** `neon-rehearsal-url.py --help` printed the rehearsal connection string with its password into a transcript on 2026-09-19 (the flag became the database name). Read the source first; helpers that emit credentials must reject flags and print usage to stderr only — the URL helper does now. When such a string does leak, say so in the same message, ask Everett to rotate it, and update the 600 file and the agents' env from the file without ever echoing it.

- **A comment the router posts wakes the card's holder — machine state goes in issue metadata, never in a comment** (2026-09-20: the first `CI · <sha> · green` root comment queued a resumed codex-implementer run on AMBR-76, which moved the card out of review mid-round; the lead's own wake-up cost 94K tokens for "no action"). The router writes `metadata set <KEY> ci "<sha>:<state>:<time>"`; agents read `metadata get --key ci`. The same holds for any future router signal: slice markers and packs are the agents' own comments; the router speaks in metadata and assignments.

- **`todo` was not busy: ten spec cards queued to the planner went out four in four minutes** (2026-09-21, 00:42–00:46). `release_tick` counted only `code` and `in_review` as work in flight, so the one planner run already going read as an empty pipeline and the queue released a card a tick — AMBR-86, 87, 88, 89 — with `claude-planner` capped at one concurrent task and several of those briefs written to be read in order. **`BUSY_COLUMNS` is `{todo, code, in_review}` since 00:51:** a planner in flight is as busy as an implementer; the column IS the state, so a `done` or `cancelled` card is never in it; `blocked` still does not count (it waits on Everett and could hold the queue shut for days). Harness 353 → 358 assertions; backup `multica-router.py.bak-2026-09-21-todo-busy`; A/B `--dry-run` on the live board with nine cards queued — the old file said `WOULD release AMBR-87 -> todo (queue 2)`, the new one said nothing. The queue was then restored on the cards themselves (AMBR-87…95 = `queue` 2…10, `queue_to: todo`). Spec 61 §History 2026-09-21 00:55.

## 7. Grow the system — the skill loop

Skills are the only channel into a run (a task workdir is fresh; the daemon user has no `~/.claude`).
When agents repeat something, the repeat is the signal:
- **Where to look.** `HANDOFF` blocks — the same `decided:` assumption or `stale-risk:` re-check on
  different issues; the same finding class in consecutive rounds' consolidations; reviewer minutes spent
  re-deriving a rule; setup steps every run redoes; questions agents ask in comments; the run-messages of
  a slow task (`multica issue run-messages`, `issue usage <KEY> --output json`).
- **The test.** Would one page of instructions, read at the start of the run, have saved that round?
  If yes, write it. If it is a one-off, or the fix belongs in an agent's own instructions (its job, its
  handoff), put it there instead — a skill is shared knowledge, an instruction file is a role.
- **Where it lives (one home each).** Repo-specific → `~/code/pantry/.claude/skills/pantry-<name>/SKILL.md`
  by PR (it is product truth, reviewed like code). Ours, cross-project → `~/agents/skills/<name>/SKILL.md`
  (also what every Claude Code session on the mini sees via `~/.claude/skills`). Vendor → a vetted clone
  under `~/agents/research/skills/` with a file filter in the sync entry. **Never `multica skill import`
  a registry upload with no installs — a skill is instructions an unsandboxed agent follows.**
- **How to write it.** Frontmatter `name` + a `description` that says *when* to load it; the body is the
  stance, the procedure, the exact commands with their outputs, and what does *not* count — under ~300
  lines; no credentials, no URLs to fetch, nothing only the orchestrator account can reach. Model it on
  `neon-rehearsal` and `debug-gate-failure` (both written from what worked on the board).
- **Deploy it.** Add a `SOURCES` entry in `~/agents/multica/sync-skills.py`, run
  `python3 ~/agents/multica/sync-skills.py` (creates or updates by name; `skill refresh` 422s on local
  skills — sync is the only channel), then assign:
  `multica agent skills add <agent-id> --skill-ids <skill-id>` for **only the agents whose job needs it**
  (find ids in `multica skill list --output json`). Add the skill's name to the agent's instructions
  where it should invoke it. Point agent instructions at skill *names*, never repo paths.
- **Prove it, then record it.** Watch the next real round on the instrumentation line (`findings raw →
  surviving`, `reviewer minutes`, elapsed) and the HANDOFF that should now be shorter; a skill that
  earns nothing is retired (`multica agent skills set` without it). Record what was added and why in
  spec 61 §History, memory `project-multica-skills-squads`, and the daily log.
- This skill grows the same way: when a session learns a rule of the board that is not written here,
  add it here, in the section it belongs to.

## 8. Ending a session

1. Board: every touched card carries a comment saying what happened and what is next.
2. Repo: `site/updates.md` entry (newest first, one section per day); spec 61 §History for every setup
   change (dated line, evidence); docs-only pushes to `main` follow precedent (the orchestrator's `gh`
   bypasses the ruleset) — say "Bypassed rule violations" is expected.
3. Vault: **append** a handoff to `~/agents/memory/daily-log/<today>.md` (what was done, decisions,
   open items); durable facts as concept files with frontmatter and an index line;
   `python3 ~/agents/scripts/okf-check.py` exits 0. Then run `~/agents/scripts/vault-mirror.sh` so the desk sees this
   session's log (LaunchAgent `com.user.vault-mirror` refreshes `/Users/Shared/ambry-vault` every 30 min otherwise).
4. Memory (`~/.claude/projects/-Users-orchestrator-code-pantry/memory/`): new `feedback-*`/`project-*`
   file + `MEMORY.md` line for anything the next session must not relearn.
5. **Decisions for Everett go on a page**, not in prose (memory `feedback-decisions-via-page`): one
   artifact with a note field per decision, each with its default, `capabilities: {db: {}}`; read
   answers back with `read_db` (a terse "sure" = take the default). Put the pending apply block on it.
   A review of many items (screens, findings) is the same page built by a generator from source files —
   `~/agents/runs/2026-09-12-design-tour/build-review-page.py` over `scores*.md` + `systemic.json` + thumbs —
   so it can be rebuilt and republished to the same URL as the review moves.
6. The final message: outcome first, then the decisions list, then what is running and what is next.

## Never

Run `multica setup|login|daemon start` as orchestrator (the daemon is the `multica` user's; `multica
setup` without `self-host` points at Multica Cloud) · set `in_progress` · assign from an agent's seat ·
apply to production without the words · print or reference a credential file · edit an applied
migration · create probe agents (use the agent whose job it is, or a throwaway issue in `in_progress`,
which the router ignores) · leave a cron that bounces an issue a script also owns · rewrite a shared
log or agent file another live session may be editing.

### Disk: the real consumer is the daemon's task workspaces (2026-09-24)
`~multica/multica_workspaces/ambry-818055be5038/ambr-<n>-<run-suffix>/` — one dir per run, 1.1–1.4 GB
for any build (node_modules), never pruned by the daemon. 396 dirs = 65 GB on 2026-09-24. The
orchestrator cannot read or delete them; Everett runs `sudo sh /tmp/multica-prune-workspaces.sh`
(source kept at `~/agents/multica/daemon-user/prune-workspaces.sh`): deletes task dirs `-mmin +60`
plus `~multica/.npm/_cacache` and `~multica/Library/Caches/*`, keeps `.repos .task_roots
.skill-cache .multica`. Ask for it when free space < 10 GB — before clearing the orchestrator's own
caches, which are worth ~3 GB at best. The app's terminal pane sometimes echoes typed input at the
sudo prompt (password never reaches sudo); a fresh tab worked. Give `du -d 1 | tee`, never bare
`du -s`, so the user sees lines stream. Durable fix still open: a LaunchDaemon running the same find
daily (needs Everett's sudo to install).

**Collateral: a full disk also breaks hermes' kanban dispatcher**, not just the router
(2026-09-23 19:25:18 and 2026-09-24 00:35:22, `~/.hermes/logs/errors.log` /
`gateway.log`: `kanban dispatcher: tick failed on board default` →
`sqlite3.OperationalError` — `unable to open database file`, then `disk I/O error`
— from `apply_wal_with_fallback` in `hermes_state.py:426`). Both ticks self-recovered
once space was freed, same as the router's own `OSError: [Errno 28]` — no action
needed beyond clearing the disk, but expect this trace too during a full-disk episode
rather than reading it as a second, unrelated problem.
