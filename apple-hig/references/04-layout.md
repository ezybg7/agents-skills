# Layout (HIG Foundations)

"A consistent layout that adapts across display sizes, orientations, and
multitasking configurations helps people understand and enjoy your app."
Familiar relationships between controls and content let people discover features
right away.

## Visual hierarchy

- **Order content by relative importance.** People view in reading order — top to
  bottom, leading to trailing — so put the most important items **near the top
  and leading side**. Prefer standard system components so RTL languages adapt to
  their natural reading order automatically.
- **Align elements to make them easier to scan; use indentation to convey
  hierarchy.** People assume **aligned items are related**, and perceive
  **indented items as subordinate** to the item they follow. Use both
  deliberately — they *are* your information hierarchy.
- **Group related items** using negative space, container shapes, or separator
  lines to show what's related and what isn't.
- **Use progressive disclosure.** Too much content and too many choices makes
  information hard to find and choices hard to understand. Use disclosure
  triangles, menus, or nested views to cut what's shown initially; use scrollable
  sections to showcase more (especially for video/music/books apps).
- **Differentiate controls from content.** Use **Liquid Glass** for a distinct
  control appearance. **Do not** put a solid or semi-opaque background color
  beneath controls — use a **scroll edge effect** to visually elevate controls
  above content. For full-screen background content, **extend it underneath
  sidebars, toolbars, and tab bars** to fill the whole screen/window.
  - If scaling a background image to the window edge means sidebars/inspectors
    cover important parts, use a **background extension effect** — flips and blurs
    the image, mirroring it beneath adjacent components
    (`backgroundExtensionEffect()`, `UIBackgroundExtensionView`).

## Adaptability

Handle at minimum:
- Regular/compact horizontal and vertical **size classes**
- Different screen sizes, orientations, aspect ratios
- System features like the **Dynamic Island**
- External displays, Display Zoom, resizable windows on iPad and Mac
- **Text-size changes**
- Locale internationalization: LTR/RTL direction, date/time/number formatting,
  font variation, **text length**

Rules:
- **Design a layout that adapts gracefully and consistently.** Respect
  system-defined safe areas, margins, and guides; use layout modifiers to
  fine-tune placement. **Even an orientation-locked app (e.g. a landscape-only
  game) must resize well** across devices and window sizes.
- **Be prepared for text-size changes.** Concretely: horizontally adjacent views
  may need to **stack vertically**; table rows/containers may need to **grow in
  height** so text isn't cropped or overlapping; single-line rows may need to
  become multi-line.
- **Preview on multiple devices, size classes, localizations, and text sizes.**
  Shortcut: **test the largest and smallest layouts first.** Use Device Hub to
  check clipping — including resized iPad and iPhone Mirroring on Mac.
- **Scale background artwork in response to display changes.** If artwork appears
  cropped/letterboxed/pillarboxed, **never change its aspect ratio** — scale it so
  it fills the screen completely. Windows can be very wide-and-short or
  tall-and-narrow, so background art often must extend well beyond the visible
  area of a standard aspect ratio.

### Size classes (iOS, iPadOS)
Each dimension is **compact** or **regular**. Horizontal = narrow vs wide;
vertical = short vs tall. Set by device type, window configuration, and
multitasking state (full screen, Slide Over, iPhone-mirrored to Mac). Apps can
exist in **every** combination.

- **Determine layout from size classes, NOT device type or orientation.**
  Orientation and idiom don't tell you how much space is available; size classes
  do.
- **Consider all possible combinations.** A layout designed only for iPhone
  landscape (regular width, compact height) may waste iPad landscape's regular
  height; designing only for compact portrait leaves space unused at regular
  width on iPad.
- **Keep functionality the same as size classes change.** Don't change *what* the
  app can do based on space — change **how much is visible**. Use bigger spaces to
  switch a **tab bar → sidebar**, or surface functionality otherwise hidden in an
  overflow menu.
- **The idiom never changes when resizing.** Keep the layout recognizable and
  familiar to the platform it's made for.

## Guides and safe areas
- A **layout guide** is a rectangular region for positioning, aligning, spacing.
  Predefined guides give standard margins and **restrict text width for optimal
  readability**. Custom guides allowed (`UILayoutGuide`, `NSLayoutGuide`).
- A **safe area** is the region not covered by a hardware feature or another view
  (toolbar, tab bar, status bar). **Respecting it is essential** so system UI and
  hardware features like the Dynamic Island don't obstruct content and controls.

## Platform notes

**iOS / iPadOS:** no additional layout considerations beyond the above.

**macOS**
- **Avoid controls or critical information at the bottom of a window** — people
  often drag windows so the bottom edge is off-screen.
- **Avoid content behind the camera housing** at the top window edge
  (`NSPrefersDisplaySafeAreaCompatibilityMode`).

**tvOS**
- **Safe area insets: 60 pt top and bottom, 80 pt on the sides.** Guarantees
  visibility regardless of TV compatibility settings or overscan cropping.
- **Pad between focusable elements** — focused elements *grow*; make sure they
  don't overlap important information when they do.
- **Grid specs** (horizontal spacing **40 pt**, minimum vertical spacing **100 pt**
  in every case; only content width changes):

| Columns | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|
| Unfocused content width (pt) | 860 | 560 | 410 | 320 | 260 | 217 | 184 | 160 |

- **Add extra vertical spacing for titled rows** — between the previous unfocused
  row's bottom and the title's center, and between the title's bottom and the
  row's unfocused items.
- **Use consistent spacing** — inconsistent spacing stops reading as a grid and is
  harder to scan.
- **Make partially hidden content look symmetrical** — keep offscreen partial
  content the same width on both sides to direct attention to fully visible items.

**visionOS**
- **In general, support resizing** (standard behavior, as on macOS/iPadOS). At
  very large sizes, **keep content horizontally centered**. You may set min/max
  sizes to stop overlap when small and unwieldiness when large — **but never use
  min/max as a way to prevent resizing.** (Safari: window resizes freely; the
  custom navigation-bar ornament has a fixed max size so controls stay reachable.)
- **Use 3D content sparingly in windows** — reserve fixed-depth 3D for meaningful
  moments alongside 2D content. **Inset inline 3D content** so it can't collide
  with other content/controls or appear unpredictably outside the window edge.
  Larger models or primarily-3D views belong in a **volume or immersive space**.
- **Put supplemental content in an adjacent window, not an ornament.** Ornaments
  are for app-specific interactive controls (toolbars, video playback controls).
  Open a new window with `defaultWindowPlacement(_:)`.
- **Space controls generously** so they're identifiable and the hover effect
  doesn't obscure other content: **button centers at least 60 pt apart.**

**watchOS**
- **No more than two or three controls side by side.** Max **three glyph buttons**
  or **two text buttons** in a row. Text buttons are usually better spanning the
  full width; two short-labeled buttons side by side work if the screen doesn't
  scroll.
- **Support autorotation in views people might show others** — an image, a QR code
  for a reader (`isAutorotating`). (Flipping the wrist away normally sleeps the
  display.)

> Hit-target sizes live in **Accessibility**, not here. HIG gives a *default*
> (what to design to) and a hard *minimum*:
> iOS/iPadOS **44×44** (min 28×28) · macOS **28×28** (min 20×20) ·
> tvOS **66×66** (min 56×56) · visionOS **60×60** (min 28×28) ·
> watchOS **44×44** (min 28×28) pt.
> Padding: **~12 pt** around bezeled elements, **~24 pt** around unbezeled ones.
