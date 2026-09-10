# Color (HIG Foundations)

Purpose of color: "enhance communication, evoke your brand, provide visual
continuity, communicate status and feedback, and help people understand
information." Color is a *communication channel*, never decoration alone.

## Best practices

- **Avoid using the same color to mean different things.** Use color
  consistently, especially when it communicates status or interactivity. If the
  brand color marks a borderless button as interactive, using the same/similar
  color on noninteractive text is confusing.
- **Make sure all colors work in light, dark, AND increased-contrast contexts.**
  System colors vary subtly by appearance to keep differentiation and contrast;
  with Increase Contrast on, the differences become far more apparent. Custom
  colors must supply light + dark variants **and an increased-contrast option for
  each variant** that gives significantly higher visual differentiation.
  *Even if your app ships in a single appearance mode, provide both light and
  dark colors to support Liquid Glass adaptivity.*
- **Test under a variety of lighting conditions.** Bright surroundings make
  colors look darker and more muted; dark environments make them look bright and
  saturated. In visionOS, surrounding walls/objects and their light reflection
  change perceived color.
- **Test on different devices.** True Tone (some iPhone/iPad/Mac) auto-adjusts
  display white point to ambient light — reading/photo/video/gaming apps can
  strengthen or weaken it via `UIWhitePointAdaptivityStyle`. Test tvOS on
  multiple HD and 4K TV brands and display settings. On Mac, test with different
  color profiles (P3, sRGB) via System Settings > Displays.
- **Consider how artwork and translucency affect nearby colors.** Maps switches
  from a light scheme in map mode to a dark scheme in satellite mode. Colors
  behind or on a translucent element (toolbar) appear different.
- **If people can choose colors, prefer system color controls** (`ColorPicker`) —
  consistent, and lets people reuse saved colors across apps.

## Inclusive color

- **Never rely on color alone** to differentiate objects, indicate
  interactivity, or communicate essential information. Provide the same
  information another way — text labels, glyph shapes, position.
- **Avoid colors that make content hard to perceive.** Insufficient contrast
  blends icons/text into background; color-blind people may not distinguish some
  combinations.
- **Consider cross-cultural perception.** Red = danger in some cultures, positive
  in others. Apple's own example: Stocks draws a rising stock **green in English,
  red in Chinese**. Make sure your colors send the message you intend.

## System colors

- **Never hard-code system color values.** Documented values are for design-time
  reference only; actual values fluctuate release to release with environmental
  variables. Use `Color` / `UIColor` / `NSColor` APIs.
- **Dynamic system colors** (iOS, iPadOS, macOS, visionOS) match standard UI
  components and adapt automatically to light/dark. Each is **semantically
  defined by purpose, not by appearance or value.**
- **Never redefine the semantic meaning of a dynamic system color.** Don't use
  the separator color as a text color, or secondary label color as a background.

### iOS/iPadOS background hierarchy
Two sets, each with primary / secondary / tertiary variants:
- **grouped** (`systemGroupedBackground`, `secondarySystemGroupedBackground`,
  `tertiarySystemGroupedBackground`) — use when you have a grouped table view.
- **system** (`systemBackground`, `secondarySystemBackground`,
  `tertiarySystemBackground`) — otherwise.

Variant meaning (both sets):
- Primary → the overall view
- Secondary → grouping content/elements *within* the overall view
- Tertiary → grouping content/elements *within secondary* elements

### iOS/iPadOS dynamic foreground colors
| Color | Use for | UIKit API |
|---|---|---|
| Label | Primary content text | `label` |
| Secondary label | Secondary content text | `secondaryLabel` |
| Tertiary label | Tertiary content text | `tertiaryLabel` |
| Quaternary label | Quaternary content text | `quaternaryLabel` |
| Placeholder text | Placeholder in controls/text views | `placeholderText` |
| Separator | Separator that lets underlying content show through | `separator` |
| Opaque separator | Separator that blocks underlying content | `opaqueSeparator` |
| Link | Text functioning as a link | `link` |

### macOS dynamic system colors (selected, semantic)
`controlAccentColor` (the accent people choose in System Settings),
`controlBackgroundColor`, `controlColor`, `controlTextColor`,
`disabledControlTextColor`, `selectedContentBackgroundColor`,
`unemphasizedSelectedContentBackgroundColor` (non-key window),
`selectedTextBackgroundColor`, `keyboardFocusIndicatorColor`,
`findHighlightColor`, `gridColor`, `headerTextColor`, `labelColor`,
`secondaryLabelColor`, `tertiaryLabelColor`, `quaternaryLabelColor` (watermark),
`linkColor`, `placeholderTextColor`, `separatorColor`, `shadowColor`,
`highlightColor` (virtual light source), `textColor`, `textBackgroundColor`,
`underPageBackgroundColor`, `windowBackgroundColor`, `windowFrameTextColor`,
`alternatingContentBackgroundColors`, `alternateSelectedControlTextColor`,
`selectedMenuItemTextColor`, `currentControlTint`.

**macOS app accent colors (macOS 11+):** your accent customizes buttons,
selection highlighting, and sidebar icons — but **only when the user's
General > Accent color is set to *multicolor***. If they pick a specific accent,
the system overrides yours everywhere *except* a sidebar icon you gave a fixed
color (fixed color carries meaning, so it's preserved).

## Liquid Glass color

- By default **Liquid Glass has no inherent color** — it takes color from the
  content directly behind it. You may apply color to some Liquid Glass elements
  (like colored/stained glass) to draw emphasis, e.g. a primary call to action;
  this is how the system styles prominent buttons.
- **Small elements (toolbars, tab bars):** the system adapts Liquid Glass between
  light and dark appearance based on underlying content. Symbols and text default
  to **monochromatic** — darker over light content, lighter over dark content.
- **Large elements (sidebars):** Liquid Glass is **more opaque**, to preserve
  legibility over complex backgrounds and support richer content on its surface.
- **Apply color sparingly** — to the material, and to symbols/text on it. Reserve
  it for things that truly benefit from emphasis (status indicators, primary
  actions).
- **To emphasize a primary action, color the BACKGROUND, not the symbol/text.**
  The system applies the app accent color to the background of prominent buttons
  (e.g. Done). ❌ Multiple colored control backgrounds in one toolbar.
  ✅ Exactly one (the Done button).
- **Avoid similar colors in control labels if your app has a colorful
  background.** For colorful/visually rich apps, prefer a **monochromatic**
  toolbar and tab bar, or an accent with clear visual differentiation. For
  primarily monochromatic apps, the brand color as app accent is effective.
- **Watch color placement in the content layer.** Avoid overlapping similar
  colors between content and controls. Colorful content may scroll under controls
  intermittently, but its **default/resting state (e.g. top of the scroll) must
  stay clearly legible.**

## Color management

- *Color space / gamut*: sRGB, Display P3. *Color profile* maps colors to
  numbers; images embed theirs so displays reproduce them correctly.
- **Apply color profiles to your images.** sRGB is accurate on most displays.
- **Use wide color (Display P3) on compatible displays** — richer, more saturated;
  more lifelike photos/video and more meaningful status indicators. Use
  **Display P3 at 16 bits per channel, exported as PNG**. You need a wide-color
  display to design P3 images.
- **Provide color-space-specific variants when needed.** Two similar P3 colors can
  be hard to distinguish on sRGB; P3 gradients can appear clipped on sRGB. Use the
  Xcode asset catalog to supply per-color-space versions.

## Platform notes
- **tvOS:** limited palette coordinating with the app logo; subtle use of color
  communicates brand while deferring to content. **Never use color alone to
  indicate focus** — subtle scaling and responsive animation are the primary
  focus signals.
- **visionOS:** use color *sparingly, especially on glass* — physical surroundings
  show through and affect legibility. Prefer color in **bold text and large
  areas**; color in lightweight text or small areas is harder to see. In fully
  immersive experiences keep **brightness balanced** — make content fully bright
  only when the visual context is also bright; avoid a bright object on a very
  dark background, especially flashing or moving.
- **watchOS:** background color should support content or supply information (an
  Activity infographic background matching the ring color), **not be a visual
  flourish**. Avoid full-screen background color in views that stay onscreen a
  long time (workouts, audio players). People may prefer *tinted* graphic
  complications over full color.

## System color values (design-time reference only — never hard-code)

RGB, in order: Default light / Default dark / Increased-contrast light /
Increased-contrast dark. visionOS uses the **default dark** values.

| Name | SwiftUI | Light | Dark | ↑Contrast light | ↑Contrast dark |
|---|---|---|---|---|---|
| Red | `red` | 255,56,60 | 255,66,69 | 233,21,45 | 255,97,101 |
| Orange | `orange` | 255,141,40 | 255,146,48 | 197,83,0 | 255,160,86 |
| Yellow | `yellow` | 255,204,0 | 255,214,0 | 161,106,0 | 254,223,67 |
| Green | `green` | 52,199,89 | 48,209,88 | 0,137,50 | 74,217,104 |
| Mint | `mint` | 0,200,179 | 0,218,195 | 0,133,117 | 84,223,203 |
| Teal | `teal` | 0,195,208 | 0,210,224 | 0,129,152 | 59,221,236 |
| Cyan | `cyan` | 0,192,232 | 60,211,254 | 0,126,174 | 109,217,255 |
| Blue | `blue` | 0,136,255 | 0,145,255 | 30,110,244 | 92,184,255 |
| Indigo | `indigo` | 97,85,245 | 109,124,255 | 86,74,222 | 167,170,255 |
| Purple | `purple` | 203,48,224 | 219,52,242 | 176,47,194 | 234,141,255 |
| Pink | `pink` | 255,45,85 | 255,55,95 | 231,18,77 | 255,138,196 |
| Brown | `brown` | 172,127,94 | 183,138,102 | 149,109,81 | 219,166,121 |

### iOS/iPadOS system grays
| Name | UIKit | Light | Dark | ↑Contrast light | ↑Contrast dark |
|---|---|---|---|---|---|
| Gray | `systemGray` | 142,142,147 | 142,142,147 | 108,108,112 | 174,174,178 |
| Gray 2 | `systemGray2` | 174,174,178 | 99,99,102 | 142,142,147 | 124,124,128 |
| Gray 3 | `systemGray3` | 199,199,204 | 72,72,74 | 174,174,178 | 84,84,86 |
| Gray 4 | `systemGray4` | 209,209,214 | 58,58,60 | 188,188,192 | 68,68,70 |
| Gray 5 | `systemGray5` | 229,229,234 | 44,44,46 | 216,216,220 | 54,54,56 |
| Gray 6 | `systemGray6` | 242,242,247 | 28,28,30 | 235,235,240 | 36,36,38 |

In SwiftUI the equivalent of `systemGray` is `gray`.

_Change log: Liquid Glass guidance updated Dec 16, 2025; system color values and
Liquid Glass added June 9, 2025._
