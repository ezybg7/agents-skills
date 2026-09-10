# Inputs (HIG) — gestures, eyes, focus, keyboards, pointers, hardware

**Universal rule across every input page:** *give people more than one way to
interact.* Never assume a person can use a specific input.

## Gestures
- **Give people more than one way to interact** — voice, keyboard, Switch Control.
- **Respond to gestures consistently with people's expectations.** People expect
  most gestures to work the same **regardless of context** (tap activates or
  selects).
- **Handle gestures as responsively as possible.** Provide feedback **during** the
  gesture that helps people predict its result.
- **Indicate when a gesture isn't available.** Otherwise people think the app has
  frozen or that they're performing the gesture wrong.
- **Add custom gestures only when necessary** — best for specialized, frequent tasks
  not covered by existing gestures (a game, a drawing app).
- **Make custom gestures easy to learn**, and test in real use scenarios.
  *If you find it difficult to describe a gesture in simple language, reconsider it.*
- **Use shortcut gestures to SUPPLEMENT standard gestures, not replace them.**
- **Avoid conflicting with gestures that access system UI** — edge swiping in
  watchOS, rolling your hand over in visionOS.
- **Consider simultaneous recognition of multiple gestures** when it enhances the
  experience — **unlikely to be useful in non-game apps**, but a game may need a
  joystick plus other onscreen controls.

### visionOS gestures
- **Support standard gestures everywhere you can.** Once someone looks at an object,
  **tap is the first gesture they'll try.**
- **Offer both indirect and direct interactions.** **Prefer indirect gestures for UI
  and common components like buttons**; reserve direct and custom gestures for
  objects that invite close-up interaction.
- **Avoid requiring specific body movements or positions** — not everyone can, due
  to disability, spatial constraints, or environment.
- **Prioritize comfort.** Continually test ergonomics. **Keeping arms raised even
  briefly is physically tiring**, and repeated small motions add up.
- **Carefully consider complex gestures involving multiple fingers or both hands** —
  people may not have both hands free; **offer an alternative.**
- **Avoid custom gestures that require a specific hand** — increases cognitive load
  and is less welcoming to people with limb differences.
- **Reserve the area around a person's hand for system overlays.** Don't anchor
  content to hands or wrists; for hand-anchored game content, place it outside that
  area.
- **Consider deferring system overlay behavior in an immersive app** — you may not
  want the Home indicator appearing when someone looks at their palm.
- **Use caution with custom gestures involving a rolling motion of the hand, wrist,
  and forearm** — **that motion is reserved for revealing system overlays**, which
  always display on top of app content.

### watchOS double tap
- **Choose the button people use most commonly as a view's primary action.**
- **Avoid setting a primary action in views with lists, scroll views, or vertical
  tabs** — it conflicts with the default navigation people expect from double tap.

## Eyes (visionOS)
- **Always give people multiple ways to interact.**
- **Design for visual comfort.** Keep objects people need **within their field of
  view**.
- **Place content at a comfortable viewing distance — at least one meter away** for
  content people read or engage with over time. **Don't place content very close.**
- **Prefer standard UI components** — they respond consistently when looked at.
  Custom components with different visual cues are hard to learn and recognize.
- **Minimize visual distractions.** Visual noise makes objects hard to find, and
  **movement is even more distracting — especially in peripheral vision.**
- **Provide enough space around an item so it's easy to look at.** Eyes make small,
  quick adjustments even while fixating, so **crowded UI is hard to target.**
- **Avoid a repeating pattern or texture filling the field of view** — eyes can lock
  onto different elements of the pattern, **making them appear to be at different
  depths.**
- **Consider subtle visual cues to encourage people to look at the likely item** —
  near the center of the field of view, gentle motion, increased size.
- **In general, give an interactive item a rounded shape.** Eyes are drawn toward
  corners; **the more rounded, the easier to keep looking at its center.**
- **A multi-element interactive component needs an overall containing shape visionOS
  can highlight** (e.g. an image plus a label below it acting as one control).
- **Prefer a custom hover effect only to emphasize a special moment** — people are
  used to standard hover effects.
- **Choose the right delay** — instant, short, or slightly longer, based on how you
  expect people to interact.
- **Keep one or more primary views unchanged in both states of a custom hover
  effect** — constancy provides visual stability.
- **Thoroughly test custom hover effects** — testing is the only way to know whether
  it looks good, responds appropriately, and enlivens without distracting.

## Focus and selection
- **Rely on system-provided focus effects** — precisely tuned to feel responsive,
  fluid, and lifelike.
- **Avoid changing focus without people's interaction.** People rely on focus to know
  where they are; an unrequested change costs them time to find the new location.
- **Be consistent with the platform.** iPadOS and macOS have full keyboard access
  reaching every control, so you only need to support focus for that.
- **Indicate focus with platform-consistent appearances** — iPadOS/macOS draw focused
  list items with **white text on a background highlight.**
- **In general, use a focus ring for a text or search field, and a highlight in a
  list or collection.** A ring can work for an item filling a cell (a photo), but a
  highlight is usually easier to see.
- **Customize the halo focus effect when necessary** — by default the system infers
  the halo shape from the item's shape.
- **Ensure focus moves through custom views sensibly.** Tab moves focus through focus
  groups **in reading order: leading to trailing, top to bottom.**
- **Adjust an item's priority to reflect its importance in a focus group** — when a
  group receives focus, its **primary item** receives focus automatically.
- **tvOS:** **in a full-screen experience, let gestures interact with the content,
  not move focus** — a full-screen item shows no focus, so people assume gestures
  affect the object. **Avoid displaying a pointer** — people expect to navigate a
  fixed number of items by changing focus, not by dragging a tiny pointer around a
  huge screen (free-form movement can make sense in gameplay). **Design for up to
  five visually distinct focus states**, and remember **focusing often increases
  scale.**

## Keyboards
- **Support Full Keyboard Access** (iOS, iPadOS, macOS, visionOS) — navigate and
  activate windows, menus, controls, and system features with the keyboard alone.
- **Respect standard keyboard shortcuts.**
- **In general, don't repurpose standard shortcuts for custom actions.** Only
  consider redefining one if its action doesn't apply to your app at all.
- **Define custom shortcuts only for the most frequently used app-specific
  commands** — too many make an app seem difficult.
- **Use modifier keys as people expect** — Command-drag moves items as a group;
  Shift while drag-resizing constrains to aspect ratio.
- **List modifier keys in this order: Control, Option, Shift, Command.**
- **Avoid adding Shift to a shortcut that uses the upper character of a two-character
  key** — people already know Shift produces the upper character; **just list the
  upper character.**
- **Let the system localize and mirror your shortcuts** — it localizes primary and
  modifier keys to the connected keyboard and mirrors for RTL.
- **Avoid creating a new shortcut by adding a modifier to an existing shortcut for an
  UNRELATED command.** Command-Z is undo, so Shift-Command-Z must not be something
  unrelated.
- **Write descriptive shortcut titles** — the shortcut interface shows a **flat list
  per category**, so submenu titles provide no context.
- **visionOS: people see a virtual keyboard overlay** when they connect a physical
  keyboard.

## Pointing devices
- **Be consistent when responding to mouse and trackpad gestures.**
- **Avoid redefining systemwide trackpad gestures** — even in a game, people expect
  to reveal the Dock and other system UI.
- **Provide a consistent experience whether people use gestures, eyes, a pointing
  device, or a keyboard.** People move fluidly between inputs and don't want to
  learn different interactions for each.
- **Let the pointer reveal and hide controls that auto-minimize or fade out** — e.g.
  holding the pointer over the minimized Safari toolbar in iPadOS.
- **Be consistent with modifier keys held during interaction** — if Option-drag
  duplicates an object in one place, it should everywhere.
- **Allow multiple selection in custom views when necessary** — iPadOS 15+ lets
  people click and drag over multiple items, with the pointer expanding into a
  visible selection rectangle.
- **Distinguish between pointer and finger input only if it provides value** — e.g.
  a video scrubber that gives pointer users a finer targeting affordance.
- **Hit regions:** **add padding around interactive elements to create comfortable
  hit regions.** *If a hit region is too small, people feel they have to be
  precise.* **Create contiguous hit regions for custom bar buttons** — gaps cause a
  **distracting flicker** as the pointer reverts to its default shape between
  buttons.
- **Pointer and content effects:**
  - **When possible, support the system-provided content effects.**
  - **Prefer system pointer appearances for standard buttons and text-entry areas.**
  - **Prefer system pointer effects for custom elements that behave like standard
    ones.**
  - **Specify the corner radius of a nonstandard element that receives the lift
    effect** — the pointer transforms to match the element's shape as it fades out.
  - **Use pointer effects consistently throughout your app** so knowledge transfers.
  - **Avoid gratuitous pointer and content effects.** People notice pointer changes
    and **expect them to be useful** — purely decorative effects distract.
  - **Keep custom pointer shapes simple** — the shape should signal the available
    action **without drawing too much attention to itself.** *If people don't
    instantly understand it, it isn't working.*
  - **Use clear, simple images for custom accessories** — a pointer accessory is
    small.
  - **Consider the accessory transition to signal a state or behavior change** — the
    system animates transitions among accessory shapes as well as their appearance
    and disappearance.
  - **Consider custom annotations that provide useful information** — X and Y values
    over a graphing area; Keynote uses annotations while dragging.
  - **Avoid displaying instructional text with a pointer** — it makes an app seem
    complicated. **Prioritize clarity and simplicity in the interface instead.**
  - **Consider the interplay of shadow, scale, and element spacing in custom hover
    effects** — **reserve scaling for elements that can grow without crowding
    neighbors.**

## Action button (iPhone, Apple Watch)
- **Support the Action button with a set of your app's essential functions.**
- **Write a short label for each action** — people see them in Settings when
  configuring the button.
- **Prefer letting the system show people how to use the Action button** — it
  automatically helps people configure it.
- **Let people use your actions without leaving their current context** — Live
  Activities and custom snippets.
- **Consider a secondary function that supports or advances the primary action.**
  *People often use the Action button without looking at the screen.*
- **Prefer using subsequent button presses to add functionality rather than to stop
  or conclude a function.**
- **Pause the current function when people press the Action button and side button
  together.** **Exception: a diving app** — pausing a dive may be dangerous.

## Digital Crown (watchOS)
- **Anchor your app's navigation to the Digital Crown.** Since watchOS 10, turning it
  is **the main way people navigate within and between apps** — list, tab, and scroll
  views respond to it.
- **Consider using it to inspect data** where navigation isn't necessary.
- **Provide visual feedback in response to Digital Crown interactions.**
- **Update your interface to match the speed of turning** — people expect **precise
  control**.
- **Use the default haptic feedback when it makes sense.** If the default detents
  don't match your app's increments, it may not feel right.

## Apple Pencil and Scribble
- **Support behaviors people intuitively expect from a marking instrument** — they
  bring real-world knowledge.
- **Let people choose when to switch between Apple Pencil and finger input** — app
  controls must respond to both.
- **Let people make a mark the moment Apple Pencil touches the screen** — mirror
  pencil-to-paper.
- **Respond to how they use it** — Apple Pencil may sense **tilt (altitude), force
  (pressure), orientation (azimuth), and barrel roll.**
- **Provide visual feedback indicating a direct connection with content** — marks
  must appear to follow the tip **directly and immediately**.
- **Design a great left- and right-handed experience.** Avoid controls in locations
  either hand may obscure; consider letting people move them.
- **Use hover to help people predict what will happen** — a preview of dimensions or
  the resulting mark.
- **Avoid using hover to initiate an action** — hovering is **imprecise** and doesn't
  make people think about distance from the screen.
- **Prefer showing a preview value near the middle of a range of dynamic values** —
  opacity or flow is hard to depict at the extremes.
- **Consider hover to support interactions close to where people are marking** — a
  contextual menu of tool sizes.
- **Prefer hover previews for Apple Pencil, not for a pointing device** — the same
  feedback for both can be confusing.
- **Double tap:** **respect people's system settings** (default toggles between the
  current tool and eraser). **Provide a control to configure custom behavior** if
  you add your own. **Never use double tap to modify content** — accidental double
  taps happen and people may not notice.
- **Squeeze (Apple Pencil Pro):** treat it as **a single, quick, DISCRETE action —
  not continuous.** **Display any revealed UI close to Apple Pencil Pro** to
  strengthen the connection. **Define squeeze actions that are nondestructive and
  easy to undo** — accidental squeezes happen.
- **Barrel roll: use only to modify marking behavior** — not for navigation or
  displaying controls.
- **Scribble:** works in all standard text components by default. **Make text entry
  feel fluid and effortless.** **Make Scribble available everywhere people might
  enter text.** **Avoid distracting people while they write** — behaviors fine for
  keyboard input can disrupt writing. **Keep a text field stationary while people
  write in it.** **Prevent autoscrolling text while people write and edit** — people
  avoid writing over scrolled text, and scrolling mid-stroke is worse. **Give people
  enough space to write** — increase field size where Pencil input is likely.
- **PencilKit: colors adjust dynamically to Dark Mode**, so content made in either
  mode works in both. **Consider custom undo and redo buttons in a compact
  environment** — the tool picker includes them only in a regular environment.

## Camera Control (iPhone)
- **Use SF Symbols to represent control functionality** — **custom symbols are not
  supported.**
- **Keep control names short** — labels follow Dynamic Type and **long names obscure
  the viewfinder.**
- **Include units or symbols with slider values** — EV, %, or a custom string.
- **Define prominent values for a slider control** — the most frequently chosen
  values, or evenly spaced major increments (zoom factors).
- **Make space for the overlay in the viewfinder** — it occupies the area adjacent to
  the Camera Control in **both portrait and landscape.**
- **Minimize distractions in the viewfinder** — a large preview with as few visual
  distractions as possible; **avoid duplicating controls.**
- **Enable or disable controls depending on camera mode** — disable video controls
  when taking photos. **You can't add or remove controls dynamically.**
- **Consider how to arrange your controls** — commonly used toward the **middle** for
  quick access, **lesser used on either side.**
- **Let people launch your experience from anywhere** via a locked camera capture
  extension.

## Remotes (tvOS)
- **Prefer standard gestures for standard actions.** Outside active gameplay, people
  expect the remote to behave the same in every app.
- **Be consistent with the tvOS focus experience.**
- **Provide clear feedback showing what your gestures do** — resting a thumb on the
  remote shows people where to swipe.
- **Define new gestures only when it makes sense** — fine within gameplay, rarely
  elsewhere.
- **Differentiate between press and tap, and avoid responding to inadvertent taps.**
  **Pressing is intentional** — use it for choosing a button, confirming a selection,
  initiating an action.
- **Consider using tap position for navigation or gameplay** — the remote
  differentiates up, down, left, and right taps.
- **Back button: in almost all cases open the parent of the current screen.** At an
  app's top level the parent is **the Apple TV Home Screen.**
- **Respond correctly to Play/Pause during media playback.**
- **Swipe** scrolls large numbers of items, starting fast and slowing based on swipe
  strength. **Press** activates a control, selects an item, and **precedes swiping
  to activate scrubbing mode.**
- **Live-viewing apps: respond to a remote's EPG-browsing buttons as expected** —
  "guide"/"browse" opens the EPG; **"page up"/"page down" changes the channel while
  content plays.**

## Game controls
- **Determine whether virtual controls on top of game content make sense** — they
  benefit games with many actions or requiring precise input.
- **Place virtual buttons where they're easy to access** — account for device
  boundaries and safe areas, plus comfortable hand positions.
- **Make controls large enough: frequently used ≥ 44×44 pt; less important (menus)
  ≥ 28×28 pt.**
- **Always include visible AND tactile press states** — without both a virtual
  control feels unresponsive.
- **Use symbols that communicate the actions they perform** — a weapon graphic for
  attack.
- **Show and hide virtual controls to reflect gameplay** — adapt to context.
- **Combine functionality into a single control.** Redesign mechanics requiring
  simultaneous or sequential multi-button presses; **use gestures like double tap.**
- **Map movement and camera controls to predictable behavior** — **movement on the
  left side, camera direction on the right.**
- **Support the platform's default interaction method.** A game controller is an
  optional purchase; **every iPhone and iPad has a touchscreen, every Mac a keyboard
  and trackpad or mouse.**
- **Tell people about game controller requirements** — tvOS and visionOS can require
  one, and the App Store shows a **"Game Controller Required"** badge.
- **Automatically detect whether a controller is paired** — don't make players set it
  up manually.
- **Customize onscreen content to match the connected controller.**
- **Map controller buttons to expected UI behavior** outside of gameplay — navigation
  should match the platform's familiar behavior.
- **Support multiple connected controllers** — use labels and glyphs matching the one
  the player is actively using.
- **Prefer symbols, not text, to refer to controller elements** — the Game Controller
  framework provides SF Symbols for most elements across controller brands.
- **Keyboard bindings:** **prioritize single-key commands** — faster, especially
  while using a mouse or trackpad. **Test key binding comfort on an Apple keyboard**
  — a Control-key binding from a non-Apple keyboard may be better as Command.
  **Take key proximity into account** — with W/A/S/D movement, put other high-value
  commands nearby. **Let players customize key bindings** — many need to, for comfort
  and play style.
- **visionOS: match spatial game controller behavior to hand input.**

## Gyroscope and accelerometer
- **Use motion data only to offer a tangible benefit.**
- **Outside of active gameplay, avoid using accelerometers or gyroscopes for direct
  manipulation of your interface** — motion gestures can be **hard to replicate
  precisely, may be impossible for some people, and can force awkward device
  positions.**

## Nearby interactions
- **Consider a task from the perspective of the physical world** for inspiration.
- **Use distance, direction, and context to inform an interaction** — prioritize
  nearby, contextually relevant information.
- **Consider how changes in physical distance guide the interaction.** In the
  physical world **perception sharpens as people get closer** — mirror that.
- **Provide continuous feedback** — reflects the dynamism of the physical world.
- **Consider multiple feedback types** — fluid transitions among visual, audible, and
  haptic feedback.
- **Never make a nearby interaction the only way to perform a task** — you can't
  assume everyone can experience one.
- **Encourage people to hold the device in portrait orientation** — landscape
  **decreases accuracy and availability** of distance and direction information.
- **Design for the device's directional field of view** — similar to the Ultra Wide
  camera in iPhone 11 and later.
- **Help people understand how intervening objects affect the experience** — other
  people, animals, or sufficiently large objects between participants degrade it.
