# Materials & Liquid Glass (HIG Foundations)

A material is "a visual effect that creates a sense of depth, layering, and
hierarchy between foreground and background elements." Materials separate
foreground (text, controls) from background (content, solid colors) by letting
color pass through — establishing hierarchy so people **retain a sense of place**.

**Two kinds, two different jobs:**
- **Liquid Glass** — the dynamic material for the *functional layer* (controls and
  navigation). Unifies the design language across Apple platforms.
- **Standard materials** — visual differentiation *within the content layer*.

## Liquid Glass

Liquid Glass forms **a distinct functional layer that floats above the content
layer** — tab bars, sidebars, toolbars. Content scrolls and peeks through from
beneath, giving dynamism and depth while keeping controls legible.

- **Don't use Liquid Glass in the content layer.** It works by clearly
  distinguishing interactive elements from content; putting it *in* content
  creates unnecessary complexity and a confusing hierarchy. Use **standard
  materials** for content-layer elements like app backgrounds.
  - **Exception:** content-layer controls with a *transient* interactive element —
    **sliders and toggles** — take on a Liquid Glass appearance to emphasize
    interactivity **while a person is activating them**.
- **Use Liquid Glass effects sparingly.** Standard system components adopt it
  automatically. On *custom* controls, use it sparingly: Liquid Glass exists to
  bring attention to the underlying content, and overusing it across multiple
  custom controls distracts from that content. **Limit it to your app's most
  important functional elements.**

### Regular vs. clear variants
Both variants change appearance in response to system settings — a person's
preferred Liquid Glass look, Reduce Transparency, Increase Contrast.

| Variant | Behavior | Use when |
|---|---|---|
| **regular** (most system components) | Blurs and adjusts the **luminosity** of background content to keep foreground legible. Scroll edge effects further blur and reduce background opacity. | Background content might cause legibility issues, **or the component has significant text** — alerts, sidebars, popovers. |
| **clear** | Highly translucent; prioritizes visibility of underlying content and keeps rich backgrounds prominent. | Components floating **over media backgrounds** (photos, video) for a more immersive experience. |

- **Only use clear Liquid Glass over visually rich backgrounds.**
- **Dimming layer rule for clear Liquid Glass:**
  - Underlying content **bright** → add a **dark dimming layer at 35% opacity**.
  - Underlying content **sufficiently dark**, *or* you're using standard AVKit
    media playback controls (which bring their own dimming) → **no dimming layer
    needed**.

(Liquid Glass *color* guidance lives in the Color reference: no inherent color,
takes color from behind; color the background not the glyph for primary actions;
one colored control per bar; monochromatic over colorful content; sidebars are
more opaque than toolbars/tab bars.)

## Standard materials

Use `UIBlurEffect`, `UIVibrancyEffect`, `NSVisualEffectView.BlendingMode` to
convey structure **in the content beneath Liquid Glass**.

- **Choose materials and effects by semantic meaning and recommended usage —
  never by the apparent color they impart.** System settings can change a
  material's appearance and behavior. Match the material/vibrancy style to the
  **use case**.
- **Use vibrant colors on top of materials to ensure legibility.** System-defined
  vibrant colors free you from worrying about too dark / bright / saturated / low
  contrast in different contexts. **Whatever material you choose, put vibrant
  colors on it.**
- **Weigh contrast vs. context when combining material with blur and vibrancy:**
  - **Thicker (more opaque) materials → better contrast** for text and elements
    with fine features.
  - **Thinner (more translucent) materials → help people retain context** by
    keeping the background content visible as a reminder.

## Platform notes

### iOS / iPadOS
Four standard materials for the content layer: **ultraThin, thin, regular
(default), thick.**

Vibrancy values designed to work with each material — the level name indicates
**relative contrast: default is highest, quaternary is lowest.**
- Labels: `.label` (default), `.secondaryLabel`, `.tertiaryLabel`,
  `.quaternaryLabel`. All work on any material **except quaternary** —
  **avoid quaternary on thin and ultraThin: contrast is too low.**
- Fills: `.fill` (default), `.secondaryFill`, `.tertiaryFill` — all materials.
- Separators: a single default `.separator`, works on all materials.

### macOS
Several standard materials with designated purposes, plus vibrant versions of all.
- **Choose when to allow vibrancy in custom views and controls.** Test in a
  variety of contexts to find where vibrancy actually improves communication.
- **Choose a background blending mode that complements your design** — macOS
  defines **behind window** and **within window**.

### tvOS
Liquid Glass appears throughout navigation and system experiences (Top Shelf,
Control Center). **Image views and buttons adopt Liquid Glass when they gain
focus.** Standard material thickness controls how prominently content shows
through:

| Material | Recommended for |
|---|---|
| ultraThin | Full-screen views requiring a **light** color scheme |
| thin | Overlay views that partially obscure content, requiring a **light** scheme |
| regular | Overlay views that partially obscure content |
| thick | Overlay views that partially obscure content, requiring a **dark** scheme |

### visionOS
Windows use an **unmodifiable system material called *glass***, which keeps people
grounded by letting light, the Environment, virtual content, and physical
surroundings show through. Glass is **adaptive** — it limits the range of
background color information so the window keeps contrast for app content while
getting brighter or darker with surroundings.

> **visionOS has no distinct Dark Mode setting.** Glass automatically adapts to
> the luminance of objects and colors behind it.

- **Prefer translucency to opaque colors in windows.** Opacity blocks the view,
  makes people feel constricted, and reduces awareness of surrounding virtual and
  physical objects.
- Custom component materials: **thin** → brings attention to interactive elements
  (buttons, selected items). **regular** → visually separates sections (sidebar,
  grouped table view). **thick** → a dark element that stays distinct on top of a
  `regular` background.
- Vibrancy (applied to text, symbols, fills; enhances depth by pulling light and
  color forward from virtual *and physical* surroundings):
  `.label` standard text · `.secondaryLabel` descriptive text (footnotes,
  subtitles) · `.tertiaryLabel` **inactive elements only, and only when text
  doesn't need high legibility.**

### watchOS
- **Use materials to provide context in full-screen modal views.** They're common
  in watchOS, and material-layer contrast orients people and distinguishes
  controls and system elements from other content.
- **Don't remove or replace the default material backgrounds on modal sheets.**

Developer: `glassEffect(_:in:)`, `Material` (SwiftUI), `UIVisualEffectView`,
`NSVisualEffectView`, "Adopting Liquid Glass".
