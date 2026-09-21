---
name: debug-gate-failure
description: What to do when a gate fails — typecheck, lint, a test, an assert file, a rehearsal, or a reviewer's confirmed finding. Reproduce, isolate to the first mismatch, revise the understanding before the code, prove the fix with the test that was missing. Use before any second attempt at a failing check.
---

# Debugging a gate failure

A failing gate is a fact about reality contradicting your model of the change. The instinct is to patch until green. The discipline is the opposite: **reality outranks the model, and one mismatch voids the rest of the plan** — stop, understand, then continue.

## 1. Reproduce exactly, once

Run the *same* command the gate ran, unchanged, and keep its verbatim output. `npx jest --watchman=false <suite>`, `npm run typecheck`, the assert file with its exact `-v` parameters. A failure you cannot reproduce is a failure you do not understand; do not proceed on a guess.

## 2. Isolate to the first mismatch

Read the **first** error, not the last — later ones are usually consequences. Find the smallest input that triggers it: a single test case, a single assertion number (`A7 FAIL: …`), a single TypeScript location. Name it in one line before touching anything: *"`expiryLabel` returns 'Today' for a date that is tomorrow in Honolulu."*

## 3. Ask which is wrong: the code, the test, or the understanding

Three different fixes. **Decide before editing.**

- The code is wrong → fix it, keep the test.
- The test is wrong → prove it: the test must contradict the spec (`file:line`) or a merged ADR. Changing a test to match the code without that proof is how a gate becomes theatre.
- Your understanding was wrong → this is the common one on a second attempt. Re-read the spec section and the previous round's `decided:` lines; the fix may be to a different file than the one that failed.

If it is the understanding, **discard the remaining plan** — the later steps were built on the same misunderstanding.

## 4. Write the missing test first

Every real defect a gate caught is one the suite did not cover. Before fixing, add the failing case to the pure module's test (`matching.ts`, `expiry.ts`, `grouping.ts` are the standing examples) or the assert file; watch it fail; then fix; then watch the whole gate go green, not just the one case. Day-granularity rules run in all five timezones (`node scripts/test-timezones.mjs --watchman=false`).

## 5. Report the fix as evidence, not as a claim

In the PR and the HANDOFF block: the first mismatch in one line, which of the three was wrong, the test you added, and the verbatim green output. "Fixed the failing test" is not a report.

## Do not

- Retry the same command hoping for a different answer.
- Add `--force`, skip a suite, widen a `try/catch`, or loosen an assertion to get green.
- Delete a test you do not understand.
- Run `npm audit fix` with the force flag — it is a hard rule here for a reason.
