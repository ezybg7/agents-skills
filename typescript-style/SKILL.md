---
name: typescript-style
description: My ruleset for writing and reviewing TypeScript/React code — flat control flow, discriminated unions, leaf-level data fetching, and the PEER self-review rubric. Load before writing or reviewing nontrivial TypeScript.
---
Precedence: an existing codebase's conventions, lint rules, and formatter always
win over this file. These are my defaults wherever the codebase doesn't dictate.
Goal: intent obvious on first read, control flow flat, the type system carrying
the design. Cleverness doesn't factor in.

## Control flow
- Keep functions and components short. If I scroll to follow one function, that
  is the signal to split it. If I can't summarize it in one sentence without
  "and", split along the "and".
- Early returns over nested conditionals: guard clauses handle edge cases at the
  top, one condition at a time; the happy path sits unindented at the bottom.
  A lookup table is fine when it reads better than a chain.
- Single-statement conditionals drop the braces: `if (!user) return null;`
- No `!` inside a ternary — swap the branches instead. `Boolean(x)` over `!!x`.
- No nested ternaries.

## Values and call sites
- `const` everywhere by default. `let` needs a justification (tight loop,
  measured hot path); a fresh value beats reassignment otherwise.
- Object parameters once a call has 3+ arguments or any boolean flag —
  `send({ to, subject, trackOpens: true })`, never `send(x, true, false)`.
- Returns follow the same rule: past two elements, named fields beat positions.
  Two-element tuples are fine for useState-shaped APIs.

## Types carry the design
- Model variants as discriminated unions with a literal tag whenever cases carry
  different data. Tag field is `kind` (not `type` — already overloaded). Never a
  single type with a pile of optional fields and an implicit "you'll figure out
  which go together" contract.
- When variants carry no payload, a plain string-literal union is lighter and fine.
- Pair every union switch with an exhaustive check so the compiler flags new
  variants at every site:

  ```ts
  function assertNever(value: never): never {
    throw new Error(`Unhandled variant: ${JSON.stringify(value)}`);
  }
  // last line of the dispatch: return assertNever(method);
  ```

- Extend the same union into the schema/database layer when variants diverge
  significantly (different required fields per case), so one `kind` drives
  rendering, validation, and writes. When variants share most fields and differ
  in one or two optionals, nullable columns are simpler — use them.
- `type` for unions, intersections, mapped types; `interface` for object shapes
  meant to be extended/augmented. Follow whichever the repo already uses.

## React
- Fetch in the leaf component that renders the data, and call mutations from the
  component that owns the button — when the data layer dedupes subscriptions
  (TanStack Query, Convex, Apollo all do). Don't drill fetched data through
  props; with a reactive query layer the database is already the source of
  truth, so the parent doesn't need to be.
- One component per file. Small helpers used only there may stay in the file;
  anything reused moves out.
- Early returns in JSX: loading, missing, and empty states handled and dismissed
  first; the happy-path render is the unindented baseline.
- Inline event handlers by default: `onClick={() => remove({ id })}`. Hoisting
  (and `useCallback`) is a deliberate decision — referential stability for a
  memoized child, or logic shared by two handlers. When sharing, extract the
  logic into a plain function; don't hoist the handlers themselves.
- JSX conditionals: prefer a ternary over `&&` when the left side can be `0` or
  `""` — otherwise React renders the stray falsy value.
- State placement: persistent state → database/query layer; high-frequency
  ephemeral state (per-frame, per-keystroke fan-out) → context or a parent
  provider, flushed to the db at checkpoints; form state → local component
  state. Reach for the db before reaching for context.
- Short mutation calls: promise chains read better than try/catch —
  `remove({ id }).then(() => toast.success("Deleted")).catch((e) => toast.error(e.message))`.
  When that boilerplate repeats across components, wrap it once in a hook.
  Optimistic updates are a polish pass after the mutation and failure path work.

## My known failure modes (self-check before finishing)
Generated first drafts drift toward: hoisted `handleClick` + `useCallback` for a
single-use handler; nested ternaries; optional-field piles where a union
belongs; fetching in a page container and prop-drilling five levels; `!!` and
negated ternaries; `&&` renders that leak a `0`. If any survived into the final
diff, fix them before reporting done.

## PEER rubric (run on the diff before opening a PR)
- **P**redictable control flow — each function reads top to bottom, no
  backtracking; conditionals flat, edge cases first.
- **E**xplicit variants — multi-shape values are tagged unions, not optional-field
  piles.
- **E**arly returns — loading/empty/error before the happy path, in TS and JSX
  both; happy path unindented.
- **R**ight-sized files — one component per file, functions visible without
  scrolling, files past ~200 lines have an obvious split pending.

Two or more "no" → refactor before shipping, not after.
