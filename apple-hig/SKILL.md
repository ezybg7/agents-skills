---
name: apple-hig
description: My working ruleset from Apple's Human Interface Guidelines — the eight design principles, hard numeric constraints, component-choice decision tables, and a pre-ship review checklist. Load before designing, building, or reviewing any Apple-platform UI (iOS, iPadOS, macOS, watchOS, tvOS, visionOS), and whenever a design question needs an HIG-grounded answer.
---
Built from a full read of developer.apple.com/design/human-interface-guidelines
(172 pages, 2,347 guidance rules; content current as of the June 2026 HIG).
Depth lives in `references/` — this file is what I apply from memory.

**Precedence:** an existing codebase's conventions and an explicit user request
always win. These are the defaults where nothing else dictates.

---

## 0. The move that prevents most mistakes

**Reach for the standard component first, and only build custom when the standard
one genuinely can't do the job.** Standard components get, for free: Dynamic Type,
Dark Mode, Increase Contrast, Reduce Transparency, Reduce Motion, RTL mirroring,
VoiceOver labels, Full Keyboard Access, focus states, hit-target sizing, Liquid
Glass adoption, and platform-correct animation. Every custom control silently
opts out of all of it and I then owe every one of those behaviors by hand.

When I do go custom, I owe the list above explicitly — not "later".

---

## 1. The eight principles — tie-breakers, not decoration

Use these to *arbitrate* when two good options conflict.

| Principle | The question it settles |
|---|---|
| **Purpose** | What is this *for*? Does this element serve it, or just exist? |
| **Agency** | Can people act their own way, skip guided flows, and undo mistakes? |
| **Responsibility** | Is the data ask minimal, explained, and safe? |
| **Familiarity** | Am I reusing a pattern people know, consistently? |
| **Flexibility** | Does this survive other inputs, sizes, languages, abilities? |
| **Simplicity** | Does every element earn its place? (**Simplicity isn't minimalism.**) |
| **Craft** | Would I ship this detail if someone were watching me do it? |
| **Delight** | Does this feel human — without getting in the way of the task? |

Two lines to keep quoting at myself:
- *"Simplicity isn't minimalism."* Don't strip usefulness in the name of clean.
- *"Don't mistake delight for decoration."* People are trying to finish a task.

---

## 2. Hard numbers I must not get wrong

**Hit targets** — design to *default*, never ship below *minimum*:

| Platform | Default | Minimum | Text default / min |
|---|---|---|---|
| iOS, iPadOS | **44×44 pt** | 28×28 | 17 / 11 pt |
| macOS | **28×28 pt** | 20×20 | 13 / 10 pt |
| tvOS | **66×66 pt** | 56×56 | 29 / 23 pt |
| visionOS | **60×60 pt** | 28×28 | 17 / 12 pt |
| watchOS | **44×44 pt** | 28×28 | 16 / 12 pt |

- **Padding between controls: ~12 pt around bezeled elements, ~24 pt around
  unbezeled ones.**
- **Contrast (WCAG AA):** **4.5:1** up to 17 pt · **3:1** at 18 pt · **3:1** for
  bold. Check in **light AND dark**. If you can't meet it by default, you must at
  least meet it under **Increase Contrast**.
- **Dynamic Type:** body runs **17 pt → 53 pt** (3.1×) from default to AX5.
  Support ≥ **200%** enlargement (**140%** watchOS).
- **tvOS safe area: 60 pt top/bottom, 80 pt sides.** Grids: 40 pt horizontal
  spacing, 100 pt minimum vertical.
- **visionOS: button centers ≥ 60 pt apart**; content **≥ 1 meter** away;
  default window **1280×720 pt** placed ~2 m in front.
- **Font weights:** prefer **Regular / Medium / Semibold / Bold**. Avoid
  **Ultralight / Thin / Light**, especially small. Thin custom font → go larger
  than the minimum.
- **Toolbar:** ≤ **3** groups; window title < **15 characters**.
- **Action sheet:** ≤ **4** buttons including Cancel. **Page control:** ≤ **10**
  dots. **Tab view (macOS):** ≤ **6** tabs. **Segmented control:** ~**5–7** max.
- **App icons:** 1024×1024 (iOS/iPadOS/macOS/visionOS), 800×480 (tvOS),
  1088×1088 (watchOS). **Widget margin 16 pt; widget text ≥ 11 pt.**

---

## 3. Choosing the right component

**Modal presentation — the distinction I must get right:**

| Use | When |
|---|---|
| **Alert** | Critical, ideally actionable information the app raises. Never merely informational, never at launch, never for expected data loss. **Only one at a time.** |
| **Action sheet** | Choices related to an action **the person just intentionally took** (cancelling a draft). |
| **Sheet** | A scoped task closely related to the current context. One at a time; Done always pairs with Cancel or Back. |
| **Popover** | A small amount of transient information or a few related tasks. **Never for warnings.** Never nested, never in compact widths. |
| **Menu** | A list of commands revealed by choosing something. |
| **Full-screen modal** | In-depth content or a complex multistep task (video, camera, markup). |

**Navigation and structure:**
- **Tab bar** = navigate top-level sections. **Toolbar** = act on the current view.
  Never confuse them. Prefer a tab bar over a sidebar; convert to a sidebar when
  there are more areas than fit.
- **Sidebar** = max **two levels** of hierarchy. Deeper → split view with a content
  list between sidebar and detail.
- **Layout comes from size classes, never device type or orientation.** Resizing
  changes *how much* is visible, never *what the app can do*.
- **Table/list** for text; **collection** for visual content; **outline view** for
  hierarchy.

**Buttons:**
- **One or two prominent buttons per view**, max.
- **Distinguish the preferred option by STYLE, never by size.**
- **Never give the primary role to a destructive action** — people press prominent
  buttons without reading them.
- Destructive = system red, and **always paired with a Cancel** titled exactly
  "Cancel" (and Cancel is never the default).

---

## 4. Liquid Glass (the current design language)

- Liquid Glass is the **functional layer** — controls and navigation floating
  **above** content. **Never put it in the content layer** (exception: sliders and
  toggles adopt it transiently *while being manipulated*).
- **Use it sparingly on custom controls.** Standard components adopt it
  automatically; overusing it on custom ones distracts from content.
- **regular** variant = blurs and adjusts luminosity; use where legibility is at
  risk or there's significant text (alerts, sidebars, popovers).
  **clear** variant = highly translucent; only over visually rich media.
  Clear over **bright** content needs a **35%-opacity dark dimming layer** (not
  needed over dark content or with AVKit's own dimming).
- **It has no inherent color** — it takes color from behind. To emphasize a primary
  action, **color the background, not the glyph or label** — and only **one**
  colored control per bar.
- Over colorful content, go **monochromatic** in toolbars and tab bars.
- **Don't put a solid or semi-opaque background behind controls** — use a
  **scroll edge effect**. Extend full-screen background content **under** sidebars,
  toolbars, and tab bars.
- **Provide light and dark colors even in a single-appearance app** — Liquid Glass
  adaptivity needs both.

---

## 5. States I must design, not discover

For every screen, these are part of the deliverable, not follow-ups:

1. **Empty** — guide the next action, with a control to take it. Don't put crucial
   information in a state that will vanish.
2. **Loading** — show something immediately (placeholders); determinate when
   duration is known; keep indicators moving; let people work meanwhile.
3. **Error** — next to the problem, no blame, says the fix.
   *"Choose a password with at least 8 characters"*, not *"That password is too
   short"*. No "oops".
4. **Largest accessibility text (AX5)** — stacked layout, fewer columns, primary
   elements still near the top, minimal truncation.
5. **Dark + Increase Contrast + Reduce Transparency** — together, not just
   separately.
6. **RTL** — mirrored layout; **numerals never reverse**; back button points right;
   don't flip logos, photos, or real-world objects.
7. **Reduce Motion** — replace x/y/z transitions with fades, no zoom/scale/parallax,
   no animating in and out of blurs.
8. **Offline / permission denied** — the app still does something useful.

---

## 6. Never (the anti-pattern list)

- **Never rely on color alone** to convey state, interactivity, or meaning.
  (Red-green and blue-orange are the hard pairs.)
- **Never hard-code system color values**, and never repurpose a semantic color
  (separator as text, secondary label as background).
- **Never disable or hide tab bar items** — explain the empty section instead.
- **Never redefine standard gestures or system keyboard shortcuts.**
- **Never make a gesture the only way to do something** — always an onscreen path.
- **Never use an alert to deliver information that isn't actionable.**
- **Never show two modal views at once** (an alert may sit on top; never two alerts).
- **Never put critical actions at the bottom of a macOS window or sidebar** —
  people drag that edge offscreen.
- **Never autoplay audio or video without controls to stop it.**
- **Never use a Time Sensitive notification for marketing.**
- **Never prepopulate a password field**, and never store secrets outside a keychain.
- **Never say "click" on touch, or "tap" on macOS.**
- **Never write "Click here"** — use descriptive link text.
- **Never use *we*** in UI copy — *"Unable to load content"*, not *"We're having
  trouble…"*.
- **Never refer to people as *the user* or *the player*** in UI copy — use *you*.
- **Never use an app-specific Dark Mode setting** — follow the system.
- **Never bake shadows, highlights, or blurs into app icon layers** — the system
  applies them dynamically.
- **Never put text in a launch screen** (it can't be localized) or treat it as a
  branding moment.
- **Never let a custom screen precede a permission alert with more than one button**,
  or with any way to dodge the system alert.

---

## 7. Copy rules

- Buttons and links start with a **verb**; title case for controls; **sentence case**
  for alert messages and box titles.
- **Ellipsis** on a control that needs more input before completing.
- Menu items: drop articles (*a*, *an*, *the*); ellipsis when more input follows;
  changeable labels ("Show Map" / "Hide Map") over paired items.
- Tooltips: **60–75 characters**, start with a verb, don't repeat the control's name.
  *If a control needs a lot of text to explain, simplify the interface.*
- **Avoid colloquialisms and humor** — culture-bound, hard to translate, and some
  carry exclusionary origins (*grandfathered in*, *peanut gallery*).
- Define technical terms, or use plain language instead.
- **People-first language** about disability; find out how a community
  self-identifies.

---

## 8. Pre-ship review checklist

Run this against any Apple-platform UI I produce or review:

- [ ] Standard components used wherever possible; every custom control justified
- [ ] Hit targets ≥ platform default; padding 12/24 pt
- [ ] Contrast passes 4.5:1 (or 3:1 for 18 pt/bold) in **light and dark**
- [ ] Renders correctly at **AX5** text size — no truncation of useful content
- [ ] No information carried by color alone
- [ ] All eight states from §5 designed
- [ ] VoiceOver: labels on every control and meaningful image; decorative images
      excluded; headings and grouping expressed; layout changes announced
- [ ] Full Keyboard Access works; no standard shortcut overridden
- [ ] Every gesture has a non-gesture equivalent
- [ ] Destructive actions confirmable, reversible, or both; undo available
- [ ] Permissions requested in context, minimal, and explained
- [ ] Copy: verbs on buttons, no "we", no blame in errors, localizable
- [ ] Liquid Glass in the functional layer only; ≤ one tinted control per bar
- [ ] Layout driven by size classes; safe areas respected
- [ ] Reduce Motion honored

---

## 9. Where the detail lives

Load the reference file when I need specifics beyond the above.

| File | Contents |
|---|---|
| `references/01-principles.md` | The 8 principles in full; per-platform device characteristics, viewing distances, inputs, session shapes |
| `references/02-color.md` | Best practices, inclusive color, semantic system colors, Liquid Glass color, color management, **full system RGB tables** |
| `references/03-typography.md` | Legibility, hierarchy, system fonts, Dynamic Type, **full type scales** (iOS default/AX1/AX5, macOS, tvOS, watchOS) |
| `references/04-layout.md` | Visual hierarchy, adaptability, size classes, guides and safe areas, tvOS grid specs |
| `references/05-materials.md` | Liquid Glass in depth, regular vs clear, standard materials, vibrancy per platform |
| `references/06-accessibility.md` | Vision, hearing, mobility, speech, cognitive; control sizes; Assistive Access; visionOS comfort |
| `references/07-app-icons.md` | Layer model per platform, Icon Composer, shapes, appearances, specs |
| `references/08-patterns.md` | Launching, onboarding, loading, modality, feedback, undo, data entry, search, drag & drop, settings, help, notifications, accounts, charts, haptics, multitasking, full screen, sharing, files, printing, audio/video, ratings, live-viewing, workouts |
| `references/09-components-actions.md` | Buttons, toolbars, menus, context menus, edit menus, pop-up/pull-down buttons, menu bar, activity views, quick actions, Dock menus, ornaments |
| `references/10-components-navigation.md` | Tab bars, sidebars, search fields, split views, lists/tables, collections, disclosure, labels, boxes, lockups, tab/column/outline views, path and token fields |
| `references/11-components-presentation.md` | Alerts, action sheets, sheets, popovers, windows and volumes, panels, scroll views, page controls |
| `references/12-components-input-content.md` | Text fields, toggles, pickers, segmented controls, sliders, steppers, keyboards, combo/color/image wells, charts, image/text/web views, progress, gauges, ratings, Activity rings |
| `references/13-components-system.md` | Widgets, Live Activities, notifications, controls, complications, watch faces, Top Shelf, App Shortcuts, snippets, status bars |
| `references/14-foundations-rest.md` | Writing, inclusion, motion, Dark Mode, right-to-left, privacy, branding, SF Symbols, icons, images |
| `references/15-inputs.md` | Gestures, eyes, focus and selection, keyboards, pointing devices, Action button, Digital Crown, Apple Pencil, Camera Control, remotes, game controls, motion sensors, nearby interactions |
| `references/16-spatial-and-platform-detail.md` | visionOS spatial layout, immersion styles, iPhone Duo layout, games in full |
| `references/17-technologies.md` | Generative AI, machine learning, VoiceOver, Siri, Sign in with Apple, Apple Pay, in-app purchase, AR, App Clips, CarPlay, HealthKit, HomeKit, iCloud, Maps, Wallet, SharePlay, Game Center, and the rest |
