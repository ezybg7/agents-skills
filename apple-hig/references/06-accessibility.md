# Accessibility (HIG Foundations)

An accessible interface is:
- **Intuitive** — familiar, consistent interactions; tasks are straightforward.
- **Perceivable** — **doesn't rely on any single method to convey information**;
  works via sight, hearing, speech, or touch.
- **Adaptable** — adapts to how people want to use their device, by supporting
  system accessibility features and letting people personalize settings.

Audit with **Accessibility Inspector**. Declare support via **Accessibility
Nutrition Labels** in App Store Connect.

> Accessibility is a *design constraint from the start* (Flexibility principle),
> not a remediation pass. It also covers **situational** limits — bright sun, a
> noisy room, one hand busy, a moving vehicle.

## Vision

- **Support larger text sizes.** Ideally let people enlarge text by **at least
  200%** (**140% in watchOS**). Via Dynamic Type or custom UI.
- **Use recommended defaults for custom type sizes** (same table as Typography):
  iOS/iPadOS 17/11 · macOS 13/10 · tvOS 29/23 · visionOS 17/12 · watchOS 16/12 pt
  (default/minimum).
- **Font weight affects readability** — a thin custom font needs to be **larger
  than** the recommended size.
- **Strive to meet color contrast minimums.** Standards: **WCAG** and **APCA**.
  Accessibility Inspector uses **WCAG Level AA**:

| Text size | Text weight | Minimum contrast ratio |
|---|---|---|
| Up to 17 pt | All | **4.5:1** |
| 18 pt | All | **3:1** |
| All | **Bold** | **3:1** |

  If you don't meet this by default, you must **at least** provide a
  higher-contrast scheme when **Increase Contrast** is on. **If you support Dark
  Mode, check contrast in both appearances.**
- **Prefer system-defined colors** — they carry accessible variants that adapt
  automatically to Increase Contrast and light/dark.
- **Convey information with more than color alone.** Hard pairings for color-blind
  people: **red-green** and **blue-orange**. Add distinct **shapes or icons**
  alongside color. Consider letting people **customize color schemes** (chart
  colors, game characters).
- **Describe your interface and content for VoiceOver.**

## Hearing

- **Support text-based ways to enjoy audio and video** — and let people customize
  the visual presentation of that text. Know the difference:
  - **Captions** — textual equivalent of *audible* information, synchronized live
    with media. Good for game cutscenes, video clips.
  - **Subtitles** — live onscreen dialogue in the person's preferred language.
    Good for TV shows and movies.
  - **Audio descriptions** — spoken narration of information presented **only
    visually**, placed in natural pauses in the main audio.
  - **Transcripts** — complete textual description of **both audible and visual**
    information. Good for long-form media (podcasts, audiobooks) where people
    review as a whole or follow along.
- **Use haptics in addition to audio cues.** Pair success chimes, error sounds,
  and game feedback with matching haptics for people who can't perceive audio or
  have it off. iOS/iPadOS also offer **Music Haptics** and **Audio graphs**.
- **Augment audio cues with visual cues** — especially in games and spatial apps
  where important content may be **off screen**. If audio guides people to an
  action, add a visual indicator pointing where to interact.

## Mobility

- **Offer sufficiently sized controls:**

| Platform | Default control size | Minimum control size |
|---|---|---|
| iOS, iPadOS | **44×44 pt** | 28×28 pt |
| macOS | **28×28 pt** | 20×20 pt |
| tvOS | **66×66 pt** | 56×56 pt |
| visionOS | **60×60 pt** | 28×28 pt |
| watchOS | **44×44 pt** | 28×28 pt |

- **Spacing between controls matters as much as size.** Rule of thumb:
  **~12 pt of padding around elements that include a bezel**; **~24 pt around the
  visible edges of elements without a bezel.**
- **Support simple gestures for common interactions.** For frequent actions use
  the simplest gesture possible — **avoid custom multifinger and multihand
  gestures** so repetitive actions stay comfortable and memorable.
- **Offer alternatives to gestures.** Core functionality must be reachable
  through **more than one physical interaction**. If a swipe dismisses a view,
  also provide a button people can tap or drive with an assistive device.
- **Let people use Voice Control** — they can perform gestures, interact with
  screen elements, dictate and edit text entirely by speaking. Requires
  **appropriately labeled interface elements**.
- **Integrate with Siri and Shortcuts** so tasks run by voice alone, and can be
  initiated from Siri, the Action button, Home Screen, or Control Center.
- **Support mobility assistive technologies:** VoiceOver, AssistiveTouch, Full
  Keyboard Access, Pointer Control, Switch Control. **Test them.**

## Speech

- **Let people use the keyboard alone to navigate and interact.** Support **Full
  Keyboard Access**. **Avoid overriding system-defined keyboard shortcuts.**
- **Support Switch Control** — control via separate hardware, game controllers,
  or sounds like a click or pop; people select, tap, type, and draw with it.

## Cognitive
"When you minimize complexity in your app or game, all people benefit."

- **Keep actions simple and intuitive.** Prefer familiar **system gestures and
  behaviors** over custom gestures people must learn and retain.
- **Minimize time-boxed interface elements.** Auto-dismissing views are a problem
  for people who need longer to process, and for assistive tech that takes longer
  to traverse the UI. **Prefer dismissing views with an explicit action.**
- **Consider difficulty accommodations in games** — reduce criteria for completing
  a level, adjust reaction time, enable control assistance.
- **Let people control audio and video playback.** **Don't autoplay without
  start/stop controls**; make them discoverable and easy to act on; consider a
  global opt-out of all autoplay.
- **Allow people to opt out of flashing lights in video playback.** Respond to the
  **Dim Flashing Lights** setting.
- **Be cautious with fast-moving and blinking animations** — distraction,
  dizziness, and in some cases **epileptic episodes**. When **Reduce Motion** is
  on, reduce automatic and repetitive animation including **zooming, scaling, and
  peripheral motion**. Specific techniques:
  - Tighten animation springs to reduce bounce
  - Track animations directly with people's gestures
  - Avoid animating depth changes in **z-axis** layers
  - **Replace x-, y-, z-axis transitions with fades**
  - Avoid animating **into and out of blurs**
- **Optimize for Assistive Access** (iOS/iPadOS streamlined mode that sets a
  default layout and control presentation to cut cognitive load). When it's on:
  - Identify core functionality; **remove noncritical workflows and UI elements**
  - Break multistep workflows into **a single interaction per screen**
  - **Always ask for confirmation twice** for actions that are hard to recover
    from, such as deleting a file

## visionOS — prioritize comfort
Immersion raises the risk of motion sickness and visual/ergonomic discomfort.
Features: head and hand **Pointer Control**, **Zoom**.
- Keep elements **within a person's field of view**. Prefer **horizontal layouts
  over vertical** (neck strain). Don't demand attention in different locations in
  quick succession.
- **Reduce speed and intensity of animated objects**, especially in **peripheral
  vision**.
- **Be gentle with camera and video motion.** Avoid making people feel the world
  is moving without their control.
- **Avoid anchoring content to the wearer's head** — feels stuck and confining,
  and blocks assistive tech like Pointer Control.
- **Minimize large and repetitive gestures** — tiring, and possibly difficult
  depending on surroundings.

_Change log: Assistive Access, Switch Control, Nutrition Labels added June 9,
2025. All guidance expanded/refined March 7, 2025 — Dynamic Type moved to
Typography, VoiceOver moved to its own page._
