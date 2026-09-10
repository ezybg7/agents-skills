# App icons (HIG Foundations)

The icon appears on the Home Screen and in search results, notifications, system
settings, and share sheets. It must convey identity **clearly and consistently
across all Apple platforms**.

## Layers — the modern (Liquid Glass era) model
You *can* ship a flattened image, but **layers give the most control** and produce
depth and vitality; the system then applies effects that respond to environment
and interaction.

| Platform | Layer model | System treatment |
|---|---|---|
| iOS, iPadOS, macOS, watchOS | Background layer + **one or more** foreground layers | Liquid Glass attributes: **specular highlights, refraction, translucency**; auto-adapt to icon size, consistent across platforms, may differ between system versions |
| tvOS | **2–5 layers** | Parallax: icon elevates to the foreground following finger movement on the remote, **gently sways** while the surface illuminates; layer separation + transparency create depth |
| visionOS | Background + **one or two** layers on top | 3D object that **subtly expands** when viewed; shadows convey inter-layer depth; the **alpha channel of upper layers creates an embossed appearance** |

**Tooling:** iOS/iPadOS/macOS/watchOS → craft layers in your design tool, then
import into **Icon Composer** (ships with Xcode) to define the background, adjust
placement, apply effects, annotate default/dark/mono variants, preview across
system versions, and export. tvOS/visionOS → add layers directly to an **image
stack** in Xcode; use **Parallax Previewer / Parallax Exporter**.

### Layer craft rules
- **Prefer clearly defined edges in foreground layers.** **Avoid soft, feathered
  edges** — system-drawn highlights and shadows depend on crisp shapes.
- **Vary opacity in foreground layers to increase depth and liveliness.** (Photos'
  icon splits its centerpiece into multiple layers with translucent pieces.)
  Workflow tip: **import fully opaque layers and adjust transparency in Icon
  Composer** so you can preview how transparency and system effects interact.
- **Design a background that both stands out and emphasizes the foreground.** If
  using a gradient, make sure it responds well to system lighting. Icon Composer
  supports **solid colors and gradients**, so importing a custom background image
  is usually unnecessary — if you do, it must be **full-bleed and opaque**.
- **Prefer vector graphics (SVG, PDF)** — they scale gracefully and stay crisp.
  **Outline artwork and convert text to outlines.** For mesh gradients and raster
  artwork, prefer **PNG** (lossless).

## Icon shape
Square in iOS/iPadOS/macOS (system masks rounded corners **matching the curvature
of other rounded interface elements and the device bezel**); rectangular with
concentric edges in tvOS; square with **circular masking** in visionOS and watchOS.

- **Produce appropriately shaped, UNMASKED layers.** Square for
  iOS/iPadOS/macOS/visionOS/watchOS; rectangular for tvOS. **Pre-applied masking
  degrades specular highlights and makes edges look jagged.**
- **Keep primary content centered** to survive corner adjustment and masking —
  **especially in visionOS and watchOS** (circular masks). Use the grids in the
  app icon production templates in Apple Design Resources.

## Design
**Embrace simplicity.** Fine visual features look busy once rendered with
system shadows and highlights, and vanish at small sizes. Find one concept that
captures the essence of the app, and express it with a **minimal number of
shapes**. Prefer a simple background (solid color or gradient) — **you don't need
to fill the entire canvas with content.**

- **Provide a visually consistent design across all platforms you support** — so
  people find the app anywhere and don't mistake it for several different apps.
- **Consider basing the design on filled, overlapping shapes** — overlapping solid
  shapes, especially with transparency and blurring, create depth.
- **Include text only when essential to the experience or brand.** Text
  **doesn't support accessibility or localization**, is usually too small to read,
  and clutters. The app name often already appears nearby. A **mnemonic** (first
  letter) can aid recognition, but avoid nonessential words like "Watch" or
  "Play" and context terms like "New" or "For visionOS". **In tvOS, put any text
  above other layers so parallax doesn't crop it.**
- **Prefer illustrations to photos; don't replicate UI components.** Photos carry
  detail that fails across appearances, at small sizes, and when split into
  layers. **Avoid extremely thin line weights and sharp corners** — they lose
  detail and crispness at small sizes/low resolution. Don't use app screenshots
  or standard UI components as your icon.
- **Never use replicas of Apple hardware products** — copyrighted, can't be
  reproduced in app icons.

## Visual effects
- **Let the system handle blurring and other visual effects.** Do **not** bake in
  specular highlights, drop shadows between layers, beveled edges, blurs, or
  glows. Custom effects interfere with system effects **and are static where the
  system's are dynamic.** If you do include custom effects, use them
  intentionally and test in Icon Composer, Device Hub, or on a physical device.
- **Create layer groupings to apply effects to multiple layers at once.** System
  effects normally act per-layer; grouping in Icon Composer gives **additional
  Liquid Glass customization** for specular highlights, refraction, translucency
  at group level.

## Appearances (iOS, iPadOS, macOS)
People choose **default, dark, clear, or tinted** Home Screen icons. You may
design each variant; **the system auto-generates any you don't provide.**

- **Keep core visual features consistent across appearances.** Don't swap elements
  per variant — it makes the app harder to find when people switch appearance.
- **Design dark and tinted icons that sit well beside system icons and widgets.**
  You may preserve your default palette, but note **dark icons are more subdued,
  and clear and tinted even more so.** The icon must stay visible, legible, and
  recognizable in every variant.
- **Use your light icon as the basis for the dark one.** Complementary colors
  reflecting the default design; **avoid excessively bright images**; **color
  backgrounds generally give the greatest contrast in dark icons.**
- **Consider offering alternate app icons** (iOS, iPadOS, tvOS, compatible apps in
  visionOS) chosen from your app's settings — e.g. a sports app offering team
  icons. Each must stay closely related to your content and **must not be
  mistakable for another app**.
  > Alternate icons in iOS/iPadOS **require their own dark, clear, and tinted
  > variants**, and all alternates and variants are **subject to app review**.

## Platform notes
- **tvOS: include a safe zone.** Focusing crops content near the edges as the icon
  scales and moves. The safe zone **varies with image size, layer depth, and
  motion**, and **foreground layers get cropped more than background layers.**
- **visionOS: avoid shapes meant to look like a hole or concave area** in the
  background layer — system shadow and specular highlights make them **stand out
  instead of recede**.
- **watchOS: avoid black backgrounds** — lighten them so the icon doesn't blend
  into the display background.

## Specifications
| Platform | Layout shape | Shape after masking | Layout size | Style | Appearances |
|---|---|---|---|---|---|
| iOS, iPadOS, macOS | Square | Rounded rectangle | **1024×1024 px** | Layered | Default, dark, clear light, clear dark, tinted light, tinted dark |
| tvOS | Rectangle (landscape) | Rounded rectangle | **800×480 px** | Layered (Parallax) | N/A |
| visionOS | Square | **Circular** | **1024×1024 px** | Layered (3D) | N/A |
| watchOS | Square | **Circular** | **1088×1088 px** | Layered | N/A |

The system automatically scales your icon for smaller variants (Settings,
notifications).

**Supported color spaces:** sRGB (color), Gray Gamma 2.2 (grayscale),
Display P3 (wide gamut — iOS, iPadOS, macOS, tvOS, watchOS **only**, not visionOS).
