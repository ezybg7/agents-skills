---
name: figma-design
description: How board agents design in Figma for Ambry — reaching the Figma MCP, the house file and page conventions, building screens with the Figma Plugin API through use_figma, and handing designs off (node links, screenshots) to specs, builds and reviews. Use whenever a card, spec or dispatch comment names Figma, a figma.com link, or Ambry Web design work; and before any Figma MCP call (use_figma, get_design_context, get_screenshot, create_new_file).
---

# Designing in Figma (Ambry board)

Everett's ruling, 2026-10-06: **Ambry Web is designed in Figma.** The iPhone app's mocks
stay in `specs/mocks/` (the `pantry-mocks` skill) unless a card says otherwise.

## 0. Reach the Figma MCP

The tools are named like `mcp__figma__use_figma`, `get_design_context`, `get_screenshot`,
`get_metadata`, `create_new_file`, `search_design_system` and `get_figma_skill`. If they are
deferred, load them in **one** ToolSearch call: `select:` followed by every name you need.

If no Figma tool exists in your run, or `whoami` fails with an auth error, **stop**. Post
`figma: unavailable (<error>)` on the card and leave it for the orchestrator. Never work
around it by pasting tokens, opening figma.com in a browser, or drawing the design elsewhere
and calling it Figma.

## 1. Load Figma's own skills first. They are mandatory.

The Figma server ships its own skills. Read them with `get_figma_skill`, never from memory:

| Before you… | Read |
|---|---|
| any `use_figma` call | `skill://figma/figma-use/SKILL.md` and its `references/gotchas.md` |
| build or change a visible screen | also `skill://figma/figma-generate-design/SKILL.md` |
| build tokens, components or variants (the design system) | also `skill://figma/figma-generate-library/SKILL.md` |
| `create_new_file` | `skill://figma/figma-create-new-file/SKILL.md` |
| implement a Figma design in code | `skill://figma/figma-design-to-code/SKILL.md`, before `get_design_context` |

On every `use_figma` write, pass `skillNames` with the `resource:` prefix, for example
`resource:figma-use,resource:figma-generate-design`.

## 2. House conventions

- **Team plan:** `team::1508286979391652981` ("everett yan's team"). Do not create files
  anywhere else.
- **Files:** one per surface. Do not create a new file per card.
  - **`Ambry Web — Design Directions`** (`0ZU71Rz4WTBfmo12HFGwui`): the three directions
    Everett chose from. Treat it as read-only history.
  - **`Ambry Web — Design System`**: tokens, type, components, built in the chosen direction.
    It is created after Everett's pick.
  - **`Ambry Web — Screens`**: one page per spec milestone, named `<spec#> <milestone> — <name>`.
- **Frames:** name them `<code> <Screen> — <state>`, for example `P1 Plan — week (dark)`.
  - Desktop frames are 1440×900; phone-web frames are 390×844.
  - Every screen comes in **light and dark**.
  - Text-heavy screens also get an AX-size or 200% zoom variant.
- **Content:** use real content from the spec and the brief (recipes, foods, counts), never
  lorem. Keep text minimal: Everett wants only the words that carry meaning.
- **Fonts:** SF Pro is installed in Figma ("Regular", "Medium", "Semibold", "Bold"; verify
  with `listAvailableFontsAsync`). On the web it maps to `-apple-system, BlinkMacSystemFont`.
- **Building:**
  - Use auto-layout for everything that has structure.
  - Bind colours, spacing and radii to the Design System file's variables once it exists;
    don't hard-code values.
  - Write incrementally and return every node id.
  - Take one screenshot after composing each screen, plus one more only after a visual fix.

## 3. Hand-off on the board

- **Specs:** in the spec's `mocks:` line and its sections, link frames as
  `https://www.figma.com/design/<fileKey>/?node-id=<id with - not :>`. Also commit PNG
  exports to `specs/mocks/<spec#>/` (`get_screenshot`, 2×), so reviewers without Figma, and
  git history, can see them.
- **Builds:** the implementer reads `get_design_context` for the linked node (after the
  design-to-code skill) and builds from the spec. Figma is the visual reference; the spec is
  the contract. Where they disagree, the spec wins, and the implementer flags the gap under
  `open:` in the HANDOFF.
- **Review:** the screen lens compares Playwright screenshots of the built page
  (`playwright-cli`) with the linked frames: light, dark, 390 wide and 1440 wide.

## 4. Never

- Never paste, print or store a Figma token. Access is the MCP's OAuth only.
- Never delete or rename another card's frames or pages.
- Never publish libraries or change team or file sharing. Those are Everett's.
- Never apply a third-party playbook from `web-design-library` unless the card names it.
  Ambry Web's cards name it.

## Known gotchas (2026-10-06, the directions run)

- **SF Pro is listed but renders nothing** in the MCP's runtime: the text is 0 px wide and the screenshot blank. Use **Inter** in Figma through local text styles, so the family can be swapped in one place. Code uses `-apple-system, BlinkMacSystemFont, "SF Pro", Inter, sans-serif`.
- **The attached Apple UI kits (iOS and macOS 27) won't import** (`Not permitted to upsert from library`). Build status bars, tab bars and glyphs yourself, in SF Symbols style.
- **Emoji:** the Noto Color Emoji font renders as outlines. Emoji typed inside Inter text render as Apple colour emoji, so use that for food glyphs.
- **Tabular numerals** can't be set through the plugin API. Note `font-variant-numeric: tabular-nums` for the build instead.
