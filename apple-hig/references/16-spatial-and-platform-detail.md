# Spatial design (visionOS) + iPhone Duo + games detail

## Spatial layout (visionOS)
- **Center important content within the field of view.** visionOS launches an app
  directly in front of people by default.
- **Avoid anchoring content to the wearer's head.** Content statically fixed in
  front of someone makes them feel **stuck, confined, and uncomfortable**, and
  blocks assistive tech.
- **Provide visual cues that accurately communicate depth.** Missing or conflicting
  cues cause **visual discomfort**.
- **Use depth to communicate hierarchy.** People notice changes in depth — a sheet
  appearing over a window makes the window recede.
- **In general, avoid adding depth to text.** Text hovering above its background is
  **hard to read, slows people down, and can cause vision discomfort.**
- **Make sure depth adds value** — use it to clarify and delight, **not
  everywhere**. Consider object size and relative importance.
- **Consider fixed scale when a virtual object should look exactly like a physical
  one** — e.g. keeping a product life-size so it looks realistic in someone's space.
- **Avoid displaying too many windows.** They obscure surroundings, making people
  feel **overwhelmed, constricted, uncomfortable**, and make relocating the app
  cumbersome.
- **Prioritize standard, indirect gestures.** An **indirect** gesture needs no hand
  movement into the field of view; a **direct** gesture requires touching the
  virtual object, which is tiring.
- **Rely on the Digital Crown to let people recenter windows.**
- **Include enough space around interactive components** so the hover effect can
  confirm the right element.
- **Let people use your app with minimal or no physical movement** unless movement
  is essential to the experience.
- **Use the floor to place a large immersive experience** — align a flat horizontal
  plane with the floor so content extending upward blends seamlessly.

## Immersive experiences (visionOS)
- **Offer multiple ways to use your app or game**, supporting accessibility features.
- **Prefer launching in the Shared Space or the `mixed` immersion style** — people
  can reference your app while using other software and switch seamlessly.
- **Reserve immersion for meaningful moments and content.** *Not every task benefits
  from immersion, and not every immersive task needs to be fully immersive.*
- **Help people engage with key moments regardless of immersion level** — dimming,
  tinting, motion, scale.
- **Prefer subtle tint colors for passthrough** (visionOS 2+) — coordinates
  surroundings with your content and **makes hands look like they belong**. Avoid
  bright tints.
- **Be mindful of visual comfort.** Even in a Full Space where you can place 3D
  content anywhere, **prefer placing it within the field of view**, and display
  motion comfortably.
- **Choose an immersion style that supports the movements people might make** — it
  lets the system respond appropriately.

### The three immersion styles (Full Space)
| Style | What it does | Boundary |
|---|---|---|
| **`mixed`** | Blends your content with passthrough — **unbounded 3D experiences**. In a Full Space you can request access to nearby physical objects and room layout (ARKit) to place virtual content in someone's surroundings. | **No boundary.** When a person gets too close to a physical object, **the system automatically makes nearby content semi-opaque** to keep them aware of their surroundings. |
| **`progressive`** | A custom environment that **partially replaces** passthrough. You can define the immersion range that suits your app, in portrait or landscape. **People adjust immersion with the Digital Crown** within the default **120°–360°** range or a custom one. | System defines an **~1.5-meter boundary** on transition. |
| **`full`** | A **360° custom environment completely replacing passthrough**, transporting people to a new place. | System defines an **~1.5-meter boundary** at start. |
- **Avoid encouraging people to move in a progressive or fully immersive
  experience** — some people can't, due to disability or physical surroundings.
- **With `mixed`, avoid obscuring passthrough too much** — people use passthrough to
  understand and navigate their physical surroundings.
- **Adopt ARKit to blend custom content with someone's surroundings.**
- **Design smooth, predictable transitions when changing immersion.** **Avoid
  sudden, jarring transitions** — gentle ones let people visually track the change.
- **Let people choose when to enter or exit a more immersive experience** — a clear
  action, never a surprise.
- **Indicate the purpose of an exit control** — does it return to a less immersive
  context, or **quit the experience altogether**?
- **Virtual hands:** **match familiar characteristics** — the viewer's hand positions
  and gestures. **Use caution with hands larger than the viewer's** — they block
  content and make interactions feel clumsy. **If hand-tracking data is interrupted,
  fade out the virtual hands and reveal the viewer's own** — never let them freeze;
  fade back in when data returns.
- **Custom environments:**
  - **Minimize distracting content** — avoid a lot of movement or high-contrast
    detail during a primary task like watching a video.
  - **Help people distinguish interactive objects** — people use **proximity** to
    judge interactivity; a distant 3D object won't invite touch.
  - **Keep animation subtle** — clouds drifting or transforming. **Always avoid too
    much movement near the edges of the field of view.**
  - **Create an expansive environment** regardless of the place depicted — a small,
    restrictive one feels **claustrophobic**.
  - **Use Spatial Audio to create atmosphere** — sound perceived as coming from
    specific locations in space.
  - **In general, avoid a flat 360-degree image.** It **gives no sense of scale** and
    reduces immersiveness.
  - **Help people feel grounded — always provide a ground plane mesh** so people
    don't feel like they're floating. (Also makes a 360-degree image feel more
    realistic if you must use one.)
  - **Minimize asset redundancy** — reusing the same assets or models too often makes
    an environment feel less realistic.

## iPhone Duo (foldable) — layout detail
The core pattern: on the outer display (and in landscape when opened), the system
places **toolbars and tab bars on the side**, along a **vertical axis**.

- **Build your app to resize.** Standard components plus resizing support adapt to
  the device's poses with little work.
- **Two conditional screen regions to design around:**
  - **The inner front-facing camera** — present **only when the camera is active**.
    When inactive it isn't visible; when it activates, **the UI moves aside** to
    indicate its presence. (The outer camera is in the corner and **always
    visible**, vertically aligned with the side controls.)
  - **The folding region** — conditional on how the device is held. When **partially
    open**, it **divides the inner display into multiple usable regions, excluding
    the center region** as the display folds.
- **Avoid extreme layout changes as people fold the device.** Move **only what's
  necessary** to keep elements visible and tappable. *Controls that disappear or
  shift dramatically are harder to find and track* — favor small adjustments.
- **Arrangement views:** **consider one when your layout already resembles it** — an
  HStack or VStack maps directly to a **split arrangement**; a layered layout maps to
  an **overlay arrangement**.
- **Keep navigation outside of arrangement views.** An arrangement view lays out
  content but **doesn't handle navigation** — put navigation split views and tab
  views *around* it, not within.
- **Account for asymmetry in your layouts.** Controls sit along one edge, so content
  space is asymmetrical. **Use safe areas** so controls (including ones on the
  opposite edge) don't cover content.
- **Keep controls consistent across device poses.** Not every pose puts controls
  vertically on the side, and available space varies — keep **relative positions as
  similar as possible.**
- **Follow the standard placement order for toolbar items.** **Top of the vertical
  axis = primary navigation** (Back, Close), **followed by prominent actions** (Done).
- **Prioritize frequently used toolbar items.** Items **overflow from bottom to top**
  by default — assign visibility priorities (groups first, then individual items) to
  change that order.
- **In general, don't override the default bar placement.** Control position on the
  vertical axis is **a core pattern of iPhone Duo.**
- **Consider using the full display width where bars aren't necessary** — good for
  visual, immersive, non-scrolling interfaces, as long as nothing conflicts with the
  Dynamic Island.
- **Group related toolbar items rather than spacing them manually** —
  `ToolbarItemGroup` / `UIBarButtonItemGroup` space items automatically and adapt.
- **Locate controls near the content they affect.** Controls belonging to a content
  area other than the trailing one **stay with that area** — proximity communicates
  the relationship.
- **Provide both a title and a symbol for each toolbar item that isn't text-only** —
  the system picks the right representation for the context, and **uses the title
  even when showing the symbol.**
- **Keep text-based buttons to a minimum** — text labels **stay in a horizontal
  bar**, so prefer a symbol wherever one works.
- **When space is limited, preserve either the toolbar or the tab bar based on what
  the view provides.** Navigation-focused experiences → **move toolbar items into the
  overflow menu** so the tab bar and primary destinations remain.
- **Use the system overflow menu.** Move your own overflow actions into it so people
  find everything in one place. **Reserve the ellipsis symbol for overflow** and give
  other menus a distinct symbol.

## Designing for games — full detail
- **Let people play as soon as installation completes.** Include as much playable
  content as possible in the initial install; **keep download time to 30 minutes or
  less** and download the rest in the background.
- **Provide great default settings.** Use device information to pick the best
  defaults — resolution, automatic accessory and controller recognition, the
  player's accessibility settings.
- **Teach through play.** Players learn better discovering mechanics in the context
  of the game world. Integrate configuration and onboarding into a **playable
  tutorial**. A written tutorial should be **a reference, not a prerequisite.**
- **Defer requests until the right time.** Integrate a permission request **into the
  scenario that requires the data** — e.g. ask for hand-tracking permission between
  the opening cutscene and the first hand-controlled action. **Let people spend
  quality time with the game before asking for a rating.**
- **Make sure text is always legible** — contrast well with the background and meet
  each platform's minimum text size (iOS/iPadOS 17/11, macOS 13/10, tvOS 29/23,
  visionOS 17/12, watchOS 16/12 pt default/minimum).
- **Make sure buttons are always easy to use** — too small or too close together
  frustrates players. Respect each platform's recommended minimum button size.
- **Prefer resolution-independent textures and graphics.** If that's not possible,
  **match your game's resolution to the device's**. **In visionOS prefer vector-based
  art.**
- **Integrate device features into your layout** — rounded corners, camera housing.
- **Make sure in-game menus adapt to different aspect ratios** — 16:10, 19.5:9, 4:3.
- **Design for the full-screen experience.**
- **Support each platform's default interaction method** — touch on iPhone, keyboard
  and mouse/trackpad on Mac, eyes and hands in visionOS.
- **Support physical game controllers, while also giving people alternatives.**
  Every platform **except watchOS** supports them.
- **Offer touch-based controls that embrace the touchscreen** on iPhone and iPad —
  direct interaction with game elements plus virtual controls.
- **Prioritize perceivability.** People must perceive content by **sight, hearing, or
  touch** — don't rely solely on color, and don't ship a cutscene without captions.
- **Help players personalize their experience.** *There's no universal configuration
  that suits everyone.*
- **Give players the tools to represent themselves.** Support the **spectrum of
  self-identity** in avatars, names, and descriptions.
- **Avoid stereotypes in your stories and characters.** Ask whether your depictions
  perpetuate real-life stereotypes — e.g. do enemies share a particular
  characteristic?
- **Integrate Game Center** so players discover your game across devices and connect
  with friends.
- **Support GameSave** so people resume on any device via their iCloud account.
- **Support haptics via Core Haptics** (iOS, iPadOS, tvOS, visionOS) — custom haptic
  patterns, optionally combined with custom audio.
- **Use Spatial Audio** — multichannel audio adapts automatically to the current
  device.
- **Take advantage of Apple technologies for unique gameplay mechanics** — augmented
  reality, machine learning, HealthKit, location.
