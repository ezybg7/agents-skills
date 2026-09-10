# Components: presentation (HIG "Presentation")

## Alerts
"Gives people critical information they need **right away**."
- **Use alerts sparingly.** They interrupt. Each one must offer **only essential
  information and useful actions**.
- **Avoid an alert merely to provide information.** People don't appreciate an
  interruption that's informative but **not actionable** — find another way to
  communicate it.
- **Avoid alerts for common, undoable actions, even destructive ones.** Deleting an
  email or file is intentional data discard — don't warn every time.
- **Never show an alert when your app starts.** Make important information
  discoverable instead. If the app detects a startup problem, handle it in the UI.
- **Be direct, with a neutral, approachable tone.** Alerts describe problems and
  serious situations — **avoid being oblique or accusatory, or masking the
  severity.**
- **Write a title that clearly and succinctly describes the situation** — complete
  and specific without being verbose: what happened and in what context.
- **Include informative text only if it adds value** — as short as possible,
  complete sentences, **sentence-style capitalization**, appropriate punctuation.
- **Avoid explaining alert buttons.** If the text and titles are clear, no
  explanation is needed. In the rare case guidance is required, use a term like
  ***choose***.
- **Include a text field only if input is needed to resolve the situation** (e.g.
  a secure field for a password).
- **Create succinct, logical button titles** — **one or two words** describing the
  *result*; prefer verbs and verb phrases tied to the alert text: "View All",
  "Reply", "Ignore".
- **Avoid "OK" as the default button title unless the alert is purely
  informational.** "OK" is ambiguous — does it mean "OK, do it" or "OK, I
  understand"?
- **Place buttons where people expect.** The most likely choice goes **trailing in
  a row** or **at the top in a stack**. **Always place the default button trailing
  in a row / at the top of a stack.**
- **Use the destructive style for a destructive action people did NOT deliberately
  choose.** When people *deliberately* chose it (Empty Trash), the resulting alert
  **does not** apply the destructive style.
- **With a destructive action, always include a Cancel button** — always titled
  exactly **"Cancel"**, and **never make Cancel the default button.**
- **Provide alternative ways to cancel** — keyboard shortcuts and other quick paths.
- **Use an action sheet — not an alert — for choices related to an intentional
  action.**
- **Avoid an alert that scrolls.** Keep titles short and messages brief; large text
  sizes can force scrolling.
- **Use a caution symbol sparingly** (`exclamationmark.triangle`). Overuse
  diminishes its significance — reserve it for when extra attention is genuinely
  needed.

## Action sheets
A modal view presenting **choices related to an action people initiate**.
- **Use an action sheet — not an alert — for choices related to an intentional
  action.** (Cancelling a Mail draft → delete the draft or save it.)
- **Use action sheets sparingly** — they interrupt too.
- **Keep titles short enough for a single line.**
- **Provide a message only if necessary** — usually title + current-action context
  is enough.
- **Provide a Cancel button when an action might destroy data.** Place it **at the
  bottom** of the sheet — **or the upper-left corner in watchOS**.
- **Make destructive choices visually prominent** — destructive style, placed **at
  the top** where they're most noticeable.
- **Use an action sheet — not a menu — for choices related to an action.** People
  expect a *menu* when they choose something that reveals a list of commands, and
  an *action sheet* after performing an action that needs clarification.
- **Avoid letting an action sheet scroll** — more buttons cost more time and
  effort, and **scrolling risks inadvertently tapping a button.**
- **Avoid more than four buttons including Cancel** — so aim for **three or fewer
  real choices**.

## Sheets
Helps people perform a **scoped task closely related to their current context**.
- **For complex or prolonged flows, consider alternatives** — e.g. the iOS/iPadOS
  full-screen modal style for video, photos, camera, or multistep tasks.
- **Display only one sheet at a time from the main interface.** Closing a sheet
  should return people to the **parent view or window** — landing on another sheet
  makes people lose their place.
- **Use a nonmodal view for supplementary items that affect the main task** — a
  split view or panel keeps people interacting with the main window.
- **Provide an alternative to the Done button** — always pair Done with **Cancel**
  (dismiss without saving) or **Back** (previous step).
- **iPhone: consider the medium detent for progressive disclosure** — a share sheet
  shows the most relevant items at medium, with more available by expanding.
- **Include a grabber in a resizable sheet.** It signals resizability, **cycles
  through detents on tap**, and **works with VoiceOver**.
- **Support swiping to dismiss.** People expect a vertical swipe rather than a
  button. **If there are unsaved changes when the swipe starts, present an action
  sheet to confirm.**
- **iPadOS: prefer the page or form sheet presentation styles** — default sizes,
  centered on a dimmed background, consistent experience.
- **Present a sheet at a reasonable default size.** People don't generally expect to
  resize sheets, so pick a size appropriate to the content.
- **macOS: let people interact with other app windows without dismissing the
  sheet.** Opening a sheet brings its parent window forward (plus modeless
  document-related panels for a document window).
- **macOS: use a panel instead of a sheet when people repeatedly provide input and
  observe results** — e.g. find and replace, where each replacement's result must
  be checked.
- **visionOS: avoid a sheet emerging from the bottom edge — center it in the field
  of view.** **Default size should help people retain context** — avoid covering
  most or all of the window; consider allowing resize.
- **watchOS: use a sheet only when the modal task needs a custom title or custom
  content presentation** — otherwise use an alert or action sheet. **Keep sheet
  interactions brief and occasional** — a temporary interruption for an important
  task, **never for navigating your content**. **If you change the default label,
  prefer SF Symbols**, and avoid a label suggesting hierarchical navigation.

## Popovers
A **transient** view appearing above other content when people click or tap a
control or interactive area.
- **Use a popover for a small amount of information or functionality** — it
  disappears after interaction, so limit it to **a few related tasks**.
- **Consider popovers when you want more room for content** — sidebars and panels
  consume a lot of space; a popover streamlines the interface for temporary content.
- **Position popovers appropriately.** The arrow should point **as directly as
  possible at the element that revealed it**, and **ideally cover neither that
  element nor essential content.**
- **Use a Close button for confirmation and guidance only** — worth it when it adds
  clarity (exiting with vs. without saving). Otherwise a popover closes on an
  outside click or tap.
- **Always save work when automatically closing a nonmodal popover.** People
  dismiss them unintentionally. **Discard work only on an explicit Cancel.**
- **Show one popover at a time. Never cascade or nest popovers.** Close the open
  one before showing a new one.
- **Don't show another view over a popover** — **except an alert**.
- **Let people close one popover and open another in a single click or tap**, e.g.
  when several bar buttons each open one.
- **Avoid making a popover too big** — only big enough for its contents and to
  point at its origin.
- **Provide a smooth transition when changing a popover's size** — animate, so it
  doesn't look like a *new* popover appeared.
- **Avoid the word *popover* in help documentation** — refer to the task or
  selection instead ("Select the Show button", not "…at the bottom of the popover").
- **Never use a popover to show a warning** — people miss them or close them
  accidentally. **Use an alert.**
- **Avoid popovers in compact views.** Adjust layout by size class; reserve
  popovers for wide views and use full screen space in compact ones.
- **macOS: consider letting people detach a popover** into a panel so they can view
  other information while it stays visible. **Make minimal appearance changes to a
  detached popover** so people keep context.

## Windows
- **Make windows adapt fluidly to different sizes** to support multitasking and
  multiwindow workflows.
- **Choose the right moment to open a new window** — great for multitasking or
  preserving context (Mail opens a new window for Compose).
- **Consider offering the option to view content in a new window**, while **avoiding
  new windows as *default* behavior** unless it clearly benefits people.
- **Avoid custom window UI.** Don't make custom window frames or controls, and
  **don't replicate the system-provided appearance.**
- **Use the term *window* in user-facing content** — not *scene* (an implementation
  term) or other synonyms.
- **Make sure window controls don't overlap toolbar items** — windowed apps put
  window controls at the **leading edge of the toolbar**, which can hide your
  leading toolbar buttons.
- **Consider a gesture to open content in a new window** — pinch expands a Notes
  item into a window.
- **Make sure custom windows use system-defined appearances** — people rely on the
  visual difference to identify the **foreground window** and know what will accept
  input.
- **Avoid critical information or actions in a bottom bar** — people relocate
  windows so the bottom edge is hidden. If you must, show only a small amount of
  information directly related to the content.

### visionOS windows and volumes
- **Prefer a window to present a familiar interface and support familiar tasks**;
  reserve immersive experiences for more.
- **Retain the window's glass background** — it grounds content in people's
  surroundings and adapts to lighting with specular reflections and shadows.
- **Choose an initial window size that minimizes empty areas.** Default is
  **1280×720 pt**, placed **about two meters in front of the wearer**.
- **Aim for an initial shape suiting the content** — Keynote defaults wide (slides
  are wide), Safari defaults tall (webpages are long).
- **Choose a minimum and maximum size for each window** so the layout stays good as
  people resize.
- **Minimize the depth of 3D content in a window** — the system already adds
  highlights and shadows for depth.
- **Prefer a volume for rich 3D content**; a window for a familiar, UI-centric
  interface.
- **Place 2D content in a volume so it looks good from multiple angles** — a
  person's perspective changes as they move around it.
- **In general, use dynamic scaling** so content stays legible and interactive at a
  distance.
- **Take advantage of the default baseplate** (visionOS 2+) — the volume's
  horizontal "floor" helps people discern its edges.
- **Consider offering high-value content in an ornament** (visionOS 2+ volumes can
  have one alongside a toolbar and tab bar) to reduce clutter.
- **Choose a baseplate alignment supporting how people interact with the volume** —
  parallel to the floor, or tilted to match the viewing angle.

## Panels (macOS)
- **Use a panel for quick access to important controls or information related to
  the content people are working with.**
- **Consider a panel for inspector functionality** — an *inspector* shows details
  of the current selection and **updates automatically** as the item changes or the
  selection changes.
- **Prefer simple adjustment controls.** Avoid controls requiring typing or
  multi-step selection.
- **Write a brief title describing the panel's purpose** — a short noun phrase; a
  panel floats above windows so it **needs a title bar** for positioning.
- **Show and hide panels appropriately.** When your app becomes **active, bring all
  open panels to the front** regardless of which window was active; when the app is
  **inactive, hide all panels.**
- **Don't include panels in the Window menu's documents list** — commands to
  show/hide them are fine, but they aren't documents or standard windows.
- **In general, don't make a panel's minimize button available** — it appears when
  needed and disappears when the app is inactive.
- **Refer to panels by title** — menus say "Show Fonts", "Show Colors", "Show
  Inspector" **without the word *panel***.
- **HUDs:** **prefer standard panels.** A HUD can distract or confuse without a
  logical reason and **may not match the current appearance setting**.
  **Maintain one panel style when your app switches modes** (keep the HUD when
  leaving full screen if you used one in it). **Use color sparingly** — small
  amounts of high-contrast color only. **Keep HUDs small** — don't obscure the
  content they adjust or compete with it.

## Scroll views
- **Support default scrolling gestures and keyboard shortcuts.** Custom scrolling
  must still behave the way people expect systemwide.
- **Make it apparent when content is scrollable** — scroll indicators aren't always
  visible, so **show partial content at the edge** to signal more.
- **Never nest scroll views with the same orientation** — unpredictable and hard to
  control. Perpendicular nesting is acceptable.
- **Consider page-by-page scrolling** where a fixed amount of content per
  interaction suits the content.
- **Scroll automatically in some cases** — when relevant content is no longer in
  view.
- **If you support zoom, set appropriate maximum and minimum scale values** —
  zooming until a single character fills the screen rarely makes sense.
- **Scroll edge effects:**
  - **Prefer the automatic style** — more opaque separation for top toolbars with
    many controls.
  - **Only use a scroll edge effect when a scroll view is behind floating interface
    elements. They aren't decorative** — they don't block or darken like overlays;
    they exist to keep controls visually distinct.
  - **Apply one scroll edge effect per view.** In iPad/Mac split views each pane can
    have its own — **keep their heights consistent for alignment.**
- **Consider a page control in page-by-page mode.**
- **macOS: use small or mini scroll bars in a tight panel**, keeping all controls in
  that panel the same size. **Account for the indicator's size** — it's slightly
  thicker than iOS; **increase margins if your content uses tight ones.**
- **visionOS Look to Scroll:**
  - **Support it for reading or browsing views** — it's **off by default** and must
    be added **per scroll view**.
  - **Avoid it for secondary content** — views with UI controls or dense information
    needing quick, precise scrolling.
  - **Maintain consistency** — if one view supports it, all similar views must.
  - **Define clear scroll areas** — prefer making the view the **full width or
    height of the window** for generous space and clear edges.
  - **Remove custom scroll effects and animations before supporting it** —
    parallax and scroll-position-driven animation **break Look to Scroll.**
- **watchOS: prefer vertically scrolling content** (the Digital Crown scrolls
  vertically). **Use tab views for page-by-page scrolling** — watchOS displays them
  as pages; in a vertical stack the Digital Crown moves through full-screen pages.
  **Consider limiting each page to a single screen height** for a glanceable design.

## Page controls
A row of indicator images, one per page in a **flat list**.
- **Use page controls for movement through an ordered list of pages.** They **do
  not** represent hierarchical or nonsequential relationships — use a sidebar or
  split view for those.
- **Center a page control horizontally near the bottom of the view or window.**
- **Don't display too many** — **more than about 10 dots are hard to count at a
  glance.** More than 10 peer pages → use a different arrangement.
- **Keep custom indicator images simple and clear.** Avoid complex shapes, negative
  space, text, and inner lines — they turn muddy at small sizes.
- **Customize the default indicator only when it enhances meaning** — e.g.
  `bookmark.fill` when every page holds bookmarks.
- **Avoid more than two different indicator images** — a single special page (like
  Weather's current-location page) can have a unique one.
- **Avoid coloring indicator images** — custom colors reduce the contrast that
  distinguishes the current page and keeps the control visible.
- **Avoid animating page transitions during scrubbing** — people scrub fast, and
  animating each transition causes lag and distracting visual flashes.
- **Don't support the scrubber with the minimal background style** — it gives no
  visual feedback while scrubbing. Use the automatic or prominent style instead.
- **tvOS: use page controls on collections of full-screen pages** — content-rich
  peers in the page hierarchy.
- **watchOS: use vertical pagination to separate views into distinct, purposeful
  pages**, scrolled with the Digital Crown; **consider limiting each page to a
  single screen height.**
