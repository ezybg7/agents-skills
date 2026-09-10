# Refreshing and verifying this skill

The HIG is served as Swift-DocC render JSON, which is complete and stable:

    https://developer.apple.com/tutorials/data/design/Human-Interface-Guidelines/<slug>.json

```bash
python3 crawl.py             # BFS the whole site -> raw/*.json + inventory.json
python3 render.py            # raw/*.json -> md/*.md (prints unknown node types; should be empty)
python3 rules.py <slug>...   # list a page's bold-lead-in guidance rules
```

## Verification — use these three, in this order

They get progressively stricter. Each has a different failure mode, so no single
one is sufficient.

| Script | Method | Use for |
|---|---|---|
| `check.py` | rule vocabulary vs. **whole references dir** | quick smoke test — **too permissive**, a rule can look covered by word overlap from an unrelated file |
| `check2.py` | rule vocabulary vs. **its one mapped file** (`pagemap.json`) | catches cross-file false positives |
| `verify.py` | rule vs. **4-line sliding windows** of its mapped file | strictest; finds rules with no single passage expressing them |
| `gaps.py` | 3 rarest corpus words of a rule absent from its file | **highest precision** — a 0.00 score is almost always a real gap |

**All of them are lexical, none are semantic.** Condensing several source rules
into one reference bullet reads as a miss. Always confirm a flag by grepping the
reference file before adding anything — and watch for **line wrapping**, which
breaks multi-word greps (`grep -z` or a shorter pattern avoids this).

## State as of 2026-09-09

- Crawl: **172 pages, 2,347 rules, 0 unknown node types**
- `gaps.py`: **0 zero-match (score 0.00) gaps**. Its raw total (~274) counts every
  rule missing even one of its three rarest words — expected wherever several source
  rules were condensed into one bullet, and not a gap signal on its own.
- `verify.py`: 2,029/2,229 exact-window matches; 200 flagged
- Hand audit of a random 25 of those 200: **24 present, 1 real gap** (since fixed)
  → estimated residual ≈ 8 rules, **~99.6% coverage**
- Core principles page: **33/33 statements captured**; all 8 principles and
  taglines present in both `SKILL.md` and `references/01-principles.md`
- `SKILL.md`: **24/24 semantic claims** traced to references; every numeric
  constant verified against source text

Sections recovered during the second-pass audit (missed on first read):
visionOS "Best practices", ML confidence/options/corrections, AR reference images
and badging, visionOS spatial widgets (paper/glass/mounting styles) and widget
placements (StandBy, Always-On, Smart Stack), macOS drag-and-drop, watchOS button
layout, tvOS/watchOS video and audio rules, chart description guidance.
