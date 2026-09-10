# Typography (HIG Foundations)

Typography's jobs: legible text, information hierarchy, communicating important
content, expressing brand/style.

## Ensuring legibility

- **Use font sizes most people can read easily.** Follow per-platform default and
  minimum sizes — **for custom fonts too**. Font *weight* also affects
  readability: with a thin-weight custom font, **aim larger than the recommended
  minimum**.

| Platform | Default size | Minimum size |
|---|---|---|
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

- **Test legibility in different contexts** — e.g. game text on every platform it
  runs on. Fixes, in order: larger type size → increase contrast via text or
  background color → switch to a typeface optimized for legibility (the system
  fonts).
- **In general, avoid light font weights.** Prefer **Regular, Medium, Semibold,
  Bold**; avoid **Ultralight, Thin, Light** — hard to see, especially at small
  sizes.

## Conveying hierarchy

- **Adjust font weight, size, and color to emphasize important information.**
  Crucially: **maintain the relative hierarchy and visual distinction when people
  change text size.**
- **Minimize the number of typefaces**, even in a highly customized interface.
  Too many obscures hierarchy, hurts readability, and reads as internally
  inconsistent or poorly designed.
- **Prioritize important content when responding to text-size changes.** Not all
  content is equally important — someone choosing a larger size wants *the
  content they care about* easier to read, not every word bigger. Tab titles
  shouldn't grow when body text does; a game's dialog matters more than transient
  hit-damage values.

## System fonts

- **San Francisco (SF)** — sans serif family: SF Pro, SF Compact, SF Arabic,
  SF Armenian, SF Georgian, SF Hebrew, SF Mono. Rounded variants exist for SF Pro,
  Compact, Arabic, Armenian, Georgian, Hebrew — use to coordinate with soft/
  rounded UI elements or for an alternative typographic voice.
- **New York (NY)** — serif family designed to work alone *and* alongside SF.
- System font per platform: **iOS/iPadOS/macOS/tvOS/visionOS → SF Pro;
  watchOS → SF Compact** (complications use **SF Compact Rounded**). NY is
  available on all; on macOS only via Mac Catalyst; on visionOS you must specify
  the type styles you want.
- Provided as **variable fonts** — one file, interpolation between styles.
  **Dynamic optical sizes** merge discrete optical sizes (Text, Display) and
  weights into one continuous design, interpolating each glyph to the exact point
  size. You don't need discrete optical sizes unless your design tool lacks
  variable-font support.
- Weights **Ultralight → Black**; SF adds widths including **Condensed** and
  **Expanded**. **SF Symbols use equivalent weights**, so symbols weight-match
  adjacent text at any size or style.
- **Never embed system fonts in your app.** Use `Font.Design` constants —
  `Font.Design.default` for the system font on all platforms, `Font.Design.serif`
  for New York.

### Text styles
A *text style* = a combination of font weight, point size, and leading for each
text size. `body` supports comfortable multi-line reading; `headline` distinguishes
a heading from surrounding content. Together they form the typographic hierarchy
**and scale proportionately** when people change system text size or turn on
Larger Text.

- **Consider using the built-in text styles** — consistent hierarchy, and
  automatic Dynamic Type + larger accessibility sizes support.
- **Modify built-in text styles when necessary via *symbolic traits*.** The bold
  trait adds a hierarchy level. Adjust **leading** for readability or space:
  - **Loose leading** for wide columns / long passages — easier to keep your place
    moving line to line.
  - **Tight leading** where height is constrained (e.g. a list row).
  - **Never use tight leading for three or more lines of text**, even where height
    is limited.
- **Adjust tracking in mockups if necessary.** A running app dynamically adjusts
  tracking at every point size; static mockups may need manual tracking. (HIG
  publishes full tracking tables per family/size.)

## Custom fonts

- **Make sure custom fonts are legible** at various viewing distances and
  conditions; respect the minimum sizes per style and weight.
- **Implement accessibility features for custom fonts.** System fonts support
  Dynamic Type and respond to **Bold Text** automatically — a custom font must
  implement the same behaviors. For Unity games use Apple's Unity plug-ins; if
  that's not viable, **let players adjust text size some other way.**

## Supporting Dynamic Type
Available on iOS, iPadOS, tvOS, visionOS, watchOS. (**macOS does not support
Dynamic Type.**)

- **Make sure your layout adapts to all font sizes.** Test with Settings >
  Accessibility > Display & Text Size > Larger Text (turn on Larger Accessibility
  Text Sizes) and confirm the app stays comfortably readable.
- **Increase the size of meaningful interface icons as font size increases.**
  SF Symbols scale automatically with Dynamic Type.
- **Keep text truncation to a minimum as font size increases.** Aim to show as
  much useful text at the largest accessibility size as at the largest standard
  size. **Avoid truncating text in scrollable regions** unless people can open a
  separate view to read the rest. Configure labels for as many lines as needed.
- **Consider adjusting your layout at large font sizes.** In horizontally
  constrained contexts, inline items (glyphs, timestamps) and container edges
  crowd text → truncation/overlap. Use a **stacked layout** (text above secondary
  items). **Reduce column count** as font size grows — multicolumn text is less
  readable at large sizes.
- **Maintain a consistent information hierarchy at every font size.** Keep primary
  elements toward the top of the view even at very large sizes so people don't
  lose track of them.

## Platform notes
- **macOS:** no Dynamic Type. Use **dynamic system font variants** to match
  standard controls: `controlContentFont`, `labelFont`, `menuFont`,
  `menuBarFont`, `messageFont`, `paletteFont`, `titleBarFont`, `toolTipsFont`,
  `userFont` (document text), `userFixedPitchFont` (monospaced document text),
  `systemFont`, `boldSystemFont` — each `(ofSize:)`.
- **visionOS:** uses **bolder** versions of the Dynamic Type body and title
  styles; adds **Extra Large Title 1 / 2** for wide editorial layouts.
  **Prefer 2D text** — visual depth makes characters harder to read. A little 3D
  text can be a fun attention-getter, but anything people must read and
  understand should have little or no depth.
  - **Make sure text looks good and remains legible when people scale it.** Pick
    a text style that looks good at full scale, then test legibility at other
    scales.
  - **Maximize contrast between text and its container background.** The system
    displays text in **white** by default because it contrasts strongly with the
    default background material. Test any other text color in many contexts.
  - **Text with no background: consider bold rather than a shadow.** Avoid
    shadows to boost contrast — the space may have no visual surface to cast an
    accurate shadow on, and you can't predict what size/density would work in a
    person's current Environment.
  - **Keep text facing people as much as possible — use *billboarding*.** Text
    anchored to a point in space (a label on a 3D object) must face the wearer
    however either moves; viewed from the side or an oblique angle it becomes
    impossible to read. Concretely: the text baseline must **stay perpendicular
    to the person's line of sight**, rotating around the y-axis as they move.
- **watchOS:** SF Compact; complications SF Compact Rounded.

## Type scales (design-time reference)

### iOS / iPadOS — Large (default)
| Style | Weight | Size | Leading | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 34 | 41 | Bold |
| Title 1 | Regular | 28 | 34 | Bold |
| Title 2 | Regular | 22 | 28 | Bold |
| Title 3 | Regular | 20 | 25 | Semibold |
| Headline | Semibold | 17 | 22 | Semibold |
| Body | Regular | 17 | 22 | Semibold |
| Callout | Regular | 16 | 21 | Semibold |
| Subhead | Regular | 15 | 20 | Semibold |
| Footnote | Regular | 13 | 18 | Semibold |
| Caption 1 | Regular | 12 | 16 | Semibold |
| Caption 2 | Regular | 11 | 13 | Semibold |

_Point sizes assume 144 ppi @2x / 216 ppi @3x._
Non-accessibility sizes run xSmall → xxxLarge; **Large is the default.**

### iOS / iPadOS — AX1 (first accessibility size)
Large Title 44/52 · Title 1 38/46 · Title 2 34/41 · Title 3 31/38 ·
Headline 28/34 · Body 28/34 · Callout 26/32 · Subhead 25/31 · Footnote 23/29 ·
Caption 1 22/28 · Caption 2 20/25.

### iOS / iPadOS — AX5 (largest)
Large Title 60/70 · Title 1 58/68 · Title 2 56/66 · Title 3 55/65 ·
Headline 53/62 · Body 53/62 · Callout 51/60 · Subhead 49/58 · Footnote 44/52 ·
Caption 1 43/51 · Caption 2 40/48.

> **Body goes 17 pt → 53 pt (3.1×) between default and AX5.** Any layout that
> assumes a fixed row height, a fixed number of columns, or a single-line label
> will break. Design the AX5 state deliberately.

### macOS built-in text styles
| Style | Weight | Size | Line height | Emphasized |
|---|---|---|---|---|
| Large Title | Regular | 26 | 32 | Bold |
| Title 1 | Regular | 22 | 26 | Bold |
| Title 2 | Regular | 17 | 22 | Bold |
| Title 3 | Regular | 15 | 20 | Semibold |
| Headline | **Bold** | 13 | 16 | Heavy |
| Body | Regular | 13 | 16 | Semibold |
| Callout | Regular | 12 | 15 | Semibold |
| Subheadline | Regular | 11 | 14 | Semibold |
| Footnote | Regular | 10 | 13 | Semibold |
| Caption 1 | Regular | 10 | 13 | Medium |
| Caption 2 | Medium | 10 | 13 | Semibold |

### tvOS built-in text styles (note the scale — 10-foot viewing)
Title 1 76/96 · Title 2 57/66 · Title 3 48/56 · Headline 38/46 ·
Subtitle 1 38/46 (Regular) · Callout 31/38 · Body 29/36 · Caption 1 25/32 ·
Caption 2 23/30. All Medium weight, emphasized Bold (Subtitle 1 → Medium).
_72 ppi @1x / 144 ppi @2x._

### watchOS
Dynamic Type sizes xSmall → xxxLarge plus AX1–AX3. Defaults by case size:
Small = 38mm, Large = 40/41/42mm, xLarge = 44/45/49mm. Styles include
Large Title, Title 1–3, Headline, Body, Caption 1–2, **Footnote 1–2**.
