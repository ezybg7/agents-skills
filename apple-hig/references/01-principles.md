# Design principles & platform character (HIG: Getting started)

Source: developer.apple.com/design/human-interface-guidelines — Design principles
(reintroduced June 8, 2026), Designing for <platform>.

> "There's no one right way to apply these principles. Instead, they're tools to
> help you weigh competing priorities and make key decisions."
> Use them to *arbitrate tradeoffs*, not as a checklist to recite.

## The eight principles

### 1. Purpose — "Make something meaningful."
- **Create value.** At every stage ask what the product is *for* and whether the
  design serves that purpose.
- **Keep focused.** Prioritize the most important features by aligning with how
  people want to use it; make those truly great rather than spreading effort.
- **Find new ways to solve the problem.** Investigate existing solutions and
  avoid re-creating them. Define what sets this product apart.

### 2. Agency — "Let people do things their own way."
- **Stay out of the way.** Get people directly to the task or content at hand.
  The best designs are unobtrusive and present when people need them.
- **Give people the freedom to explore.** Don't lock people into specific flows
  or modes. When a guided flow is necessary, make it easy to skip or escape.
- **Help people recover from mistakes.** Reversibility makes an interface
  inviting. "Recovering from the unexpected shouldn't cost people their time or
  work." Build forgiveness in, and make it easy.

### 3. Responsibility — "Act in people's best interest."
- **Be fully transparent about what your product does and why.** Clear rationale
  when asking permission; be clear about what data you collect and how it's used.
- **Keep people's information safe.** Collect only what the product needs.
  Anticipate misuse and put protections in place *before* harm occurs.

### 4. Familiarity — "Build on what people know."
- **Use concepts that people know** — from the real world and other software.
- **Keep visuals and interactions consistent.** Once you establish a behavior or
  appearance for an element, apply it throughout. Consistency speeds learning and
  gives confidence that new interactions will behave as expected.
- **Provide clear feedback.** Show when controls are available, indicate when
  content changes, use system patterns for alerts and choices.

### 5. Flexibility — "Adapt to diverse contexts and needs."
- **Design for everyone.** Accessibility is a priority *from the start*, not a
  later pass. Design inclusively to reach the broadest audience — it produces a
  better experience for all.
- **Preserve a person's context.** Keep content and controls in consistent,
  predictable positions as the design adapts; use natural animation to ease
  transitions.
- **Consider a variety of input methods** — voice, touch, keyboard, pointer, and
  more — so people can use what works best for them.
- **Approach every platform with intention.** Give each platform you support the
  same level of care; software should feel at home wherever it runs.

### 6. Simplicity — "Be clear and direct."
- **Include just what's necessary.** *"Simplicity isn't minimalism."* Aim for a
  focused, useful experience that keeps important things close and lets the rest
  fall away.
- **Be concise.** Choose exactly the words needed to convey a concept or label a
  control. The simplest way to say something is often the most universal.
- **Establish hierarchy.** Prioritize recognizable controls and a consistent
  structure that shows where people are and what comes next.

### 7. Craft — "Care about every detail."
- **Quality sets the tone.** Stunning visuals, smooth animations, precise
  wording, thoughtful audio. Be deliberate with each decision.
- **Experiment and iterate.** Prototype early, discard what doesn't work, test in
  real-world settings for durability, reliability, performance.
- **Maintain your craft.** "Shipping isn't the finish line." Keep the interface
  current with the latest platform capabilities and design patterns.

### 8. Delight — "Make it human."
- **Identify the emotion you want to inspire.** Fitness energizes; meditation
  calms; a game thrills. Let that feeling shape the design.
- **Create defining moments.** From a button press to an error message, ask
  whether the moment can carry character that reflects the design's spirit.
- **Don't mistake delight for decoration.** People are trying to accomplish a
  task; never let delight-for-its-own-sake block the core purpose.
- **Consider the whole.** Delight is the *sum* of freedom to act, safety to
  explore, familiar metaphors, and flexibility across contexts.

## Designing for iOS

Fundamental device characteristics that should drive iOS design decisions:

- **Display.** Medium-size, high-resolution.
- **Ergonomics.** Held in one or both hands, portrait and landscape; viewing
  distance is typically no more than a foot or two.
- **Inputs.** Multi-Touch gestures, virtual keyboards, voice control — used *on
  the go*. People often want apps to use personal data plus gyroscope/
  accelerometer input, and may want spatial interactions.
- **App interactions.** Sessions range from a minute or two (checking updates,
  sending messages) to an hour or more (browsing, games, media). People keep
  many apps open and switch frequently among them.
- **System features to integrate:** Widgets, Home Screen quick actions,
  Spotlight, Shortcuts, Activity views.

### iOS best practices (verbatim intent)
- **Limit onscreen controls; make secondary details and actions discoverable
  with minimal interaction.** Help people concentrate on primary tasks/content.
- **Adapt seamlessly to appearance changes** — device orientation, Dark Mode,
  Dynamic Type — letting people choose the configurations that work for them.
- **Support interactions that match how people hold the device.** Controls in the
  middle or bottom of the display are easier and more comfortable to reach. It is
  "especially important" to let people swipe to navigate back and to initiate
  actions in a list row.
- **With permission, integrate platform capabilities so people don't have to
  enter data** — payments, biometric authentication, location-based features.

## Other platforms — verified device characteristics

Viewing distance and input mode are the two facts that should change a layout.

| Platform | Display | Viewing distance | Primary inputs | Session shape |
|---|---|---|---|---|
| **iOS** | Medium, high-res | 1–2 ft | Multi-Touch, virtual keyboard, voice | 1–2 min bursts to 1 hr+; frequent app switching |
| **iPadOS** | Large, high-res | ~3 ft | Multi-Touch, hardware keyboard, pointer, Apple Pencil, voice — **often combined** | Quick actions to hours; multiple apps onscreen; drag and drop between apps |
| **macOS** | Large, high-res, often multi-display (incl. iPad as a display) | 1–3 ft | Keyboard, pointing devices, game controls, Siri — any combination | Minutes to hours of deep concentration; many apps open; smooth active/inactive transitions |
| **tvOS** | Very large, high-res | **8 ft or more**, and people move around the room | Remote, game controller, voice, other Apple devices | Hours of immersion; picture-in-picture alongside another app |
| **watchOS** | Small, on the wrist | < 1 ft, wrist raised, opposite hand interacting | Digital Crown (vertical nav / data inspection), tap/swipe/drag while in motion, Action button (eyes-free) | **Under a minute each**, many times a day. People use complications, notifications, and Siri *more than the app itself* |
| **visionOS** | Limitless spatial canvas | Content is brought to the person, not vice versa | **Eyes + indirect pinch** (default), direct touch gestures, Digital Crown for passthrough | Shared Space (side-by-side apps) ↔ Full Space (sole app) |
| **iPhone Duo** | Two displays + center hinge | As iPhone | As iOS | Continuous across open/close |

### Platform-specific facts worth remembering
- **watchOS:** the related experiences (complications, notifications, Siri) are
  used more than the app. Design those first, not last.
- **visionOS best practices (the platform's own guidance, not just its specs):**
  - **Embrace the unique features of Apple Vision Pro** — space, Spatial Audio, and
    immersion, integrating passthrough and spatial input from eyes and hands.
  - **Consider different types of immersion for your most distinctive moments.**
    Experiences can be windowed and UI-centric, fully immersive, or anything
    between. **For each key moment, find the MINIMUM level of immersion that suits
    it — don't assume every moment needs to be fully immersive.**
  - **Use windows for contained, UI-centric experiences.** For standard tasks prefer
    standard windows — planes in space containing familiar controls. People can
    relocate windows anywhere, and **the system's scaling keeps window content
    legible whether it's near or far.**
  - **Prioritize comfort** so people stay physically relaxed while interacting.
  - **Help people share activities with others.** Shared activities let people see
    the **spatial Personas** of other participants, so it feels like everyone is
    together in the same space.
- **visionOS:** `Shared Space` is the launch default; `Full Space` is opt-in.
  Passthrough is user-controlled via the Digital Crown. Visual comfort is
  *paramount* — people see everything through cameras. Apple's stated safety
  limits: not while driving/operating machinery, not while moving through unsafe
  environments, 13+ only.
- **iPhone Duo:** you are still designing for iPhone — iOS patterns still apply.
  Two displays, each with its own front camera; on the outer display the system
  puts **toolbars and tab bars on the side** to maximize vertical content space,
  and they *stay on the side* when opened in landscape for continuity. The hinge
  eats content space as the device folds. Poses: book-fold, flat on a surface,
  standing on edge. Standard components + resizing support = adapts with little
  work.
- **Games:** ship playable content in the initial install, **download ≤ 30 min**,
  stream the rest in background. Great defaults over settings screens. Teach
  through play; a written tutorial is a reference, not a prerequisite. Defer
  permission requests into the scenario that needs them.

### Minimum text sizes for games (per platform)

| Platform | Default text size | Minimum text size |
|---|---|---|
| iOS, iPadOS | 17 pt | 11 pt |
| macOS | 13 pt | 10 pt |
| tvOS | 29 pt | 23 pt |
| visionOS | 17 pt | 12 pt |
| watchOS | 16 pt | 12 pt |

**Cross-platform rule:** approach every platform with intention. Don't port one
platform's interface verbatim to another — port the *purpose*, then rebuild it
with that platform's native patterns, inputs, and viewing distance in mind.
