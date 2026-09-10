# Components: input, content, status (HIG "Selection and input",
# "Content", "Status")

## Text fields
- **Use for a small amount of information** (name, email). Larger text → **text
  view**.
- **Show a hint (placeholder) to communicate purpose** — "Email", "Password".
  *Placeholder text disappears on input*, so don't rely on it alone.
- **Use secure text fields for private data** (`SecureField`).
- **Match field size to the quantity of anticipated text** — size helps people
  gauge how much to provide.
- **Evenly space multiple text fields** and **stack them vertically** so it's clear
  which introductory label belongs to which field.
- **Ensure tabbing between fields flows logically.**
- **Validate fields when it makes sense.**
- **Use a number formatter for numeric data** — restricts to numeric values and can
  format decimals, percentage, currency.
- **Adjust line breaks to the field's needs.** By default text beyond the bounds is
  **clipped**; you can wrap instead.
- **Present a text field only when necessary** — **prefer a list of options over
  requiring text entry.**
- **Consider a combo box when you need text input paired with a list of choices.**
- **iOS/iPadOS/tvOS/visionOS: show the appropriate keyboard type** (numbers, URL,
  email…) to streamline entry.
- **iOS/iPadOS: display a Clear button at the trailing end** so people erase input
  without repeated deletes. **Use images and buttons for clarity** — custom images
  at either end, or a system button like Bookmarks.
- **tvOS/watchOS: minimize text entry** — it's time-consuming; gather information
  another way.
- **macOS: consider an expansion tooltip to show clipped or truncated text.**

## Toggles (switches, checkboxes, radio buttons)
- **Use a toggle for two opposing values affecting the state of content or a
  view.** A toggle **always manages state** — other kinds of action need a
  different control.
- **Clearly identify the setting, view, or content it affects.**
- **Make the visual difference between states obvious** — add/remove a color fill,
  show/hide the background shape, change inner details (a checkmark).
- **Use the switch toggle style only in a list row** — no label needed, the row
  supplies context.
- **Change a switch's default green only if necessary** — your accent color is
  fine, but ensure enough contrast.
- **Outside a list, use a button that behaves like a toggle, not a switch** (Phone's
  filter button gains a blue highlight when on). **Avoid a label explaining the
  button** — the icon plus alternative backgrounds convey it.
- **macOS specifics:**
  - **Use switches, checkboxes, and radio buttons in the window body, not the
    window frame** — never in a toolbar or status bar.
  - **Prefer a switch for settings you want to emphasize** — more visual weight than
    a checkbox, so it suits controlling more functionality.
  - **In a grouped form, consider a mini switch** for a single row so row heights
    stay consistent with buttons and other controls.
  - **In general, don't replace an existing checkbox with a switch.**
  - **Use a checkbox instead of a switch for a hierarchy of settings** — checkboxes
    align well and communicate grouping.
  - **Accurately reflect a checkbox's state: on, off, or mixed.** Show **mixed**
    when subordinate checkboxes disagree.
  - **Consider a label to introduce a group of checkboxes** if the relationship
    isn't clear — **align the label's baseline with the first checkbox.**
  - **Prefer radio buttons for mutually exclusive options**; checkboxes when people
    can choose multiple.
  - **Consider radio buttons for more than two mutually exclusive options.**
  - **Avoid too many radio buttons — more than about five options → use a pop-up
    button** instead.
  - **For a single on/off setting, prefer a checkbox** — the presence or absence of
    the checkmark makes the state clearer than a lone radio button.
  - **Use consistent spacing for horizontal radio buttons** — measure the longest
    label and apply that spacing throughout.

## Pickers
- **Consider a picker for medium-to-long lists.** For a **fairly short** list,
  prefer a **pull-down button**.
- **Use predictable and logically ordered values** — many values are hidden before
  interaction, so people must be able to predict them (e.g. alphabetized).
- **Avoid switching views to show a picker.** Display it **in context**, below or
  near the field being edited — typically at the bottom of a window or in a popover.
- **Consider less granularity for minutes in a date picker.** Default is 0–59;
  you can increase the interval as long as it **divides evenly into 60**.
- **iOS date picker styles: compact** (a button showing the current value in the
  accent color, opening a modal) **when space is constrained**, plus inline and
  wheels.
- **macOS: two date picker styles — textual and graphical.** Textual suits limited
  space and expects people to make specific edits.

## Segmented controls
- **Use for closely related choices affecting an object, state, or view.**
- **Consider one when grouping functions together or clearly showing selection
  state matters** — segmented controls **preserve their grouping regardless of the
  view.**
- **Keep control types consistent within one segmented control.** Don't mix action
  segments into a control representing selection state, and don't show selection
  state in a control of actions.
- **Limit the number of segments** — **no more than about five to seven in a wide
  interface**, fewer in narrow ones. Too many are hard to parse and slow to
  navigate.
- **In general, keep segment size consistent** — equal widths feel balanced; keep
  icon and title widths consistent too.
- **Prefer either text or images — not a mix — in a single control.**
- **Use similarly sized content in each segment** — since segments are equal width,
  it looks bad if some fill and others don't.
- **Use nouns or noun phrases for labels, title-style capitalization.** A
  text-labeled segmented control **doesn't need introductory text**.
- **Consider introductory text when the control uses symbols or icons**, or a label
  below each segment.
- **Consider a segmented control to switch between closely related subviews.**
- **macOS: use a tab view in the main window area — not a segmented control — for
  view switching.** **Consider supporting spring loading.**
- **tvOS: consider a split view instead** on content-filtering screens.
  **Avoid putting other focusable elements close to segmented controls** — segments
  **become selected when focus moves to them, not when people click.**

## Sliders
- **Customize appearance if it adds value** — track color, thumb image and tint,
  leading/trailing icons.
- **Use familiar slider directions** — **minimum leading, maximum trailing** for
  horizontal sliders, consistently with all other apps.
- **Consider supplementing a slider with a text field and stepper**, especially over
  a wide range, so people see and set the exact value.
- **Never use a slider to adjust audio volume** — use a **volume view** (includes a
  volume slider and an audio-route control).
- **Consider live feedback as the value changes** — Dock icons scale in real time as
  you drag the Size slider.
- **Choose a style matching expectations** — a horizontal slider suits moving
  between a fixed start and end point.
- **Consider a label to introduce a slider** — **sentence-style capitalization,
  ending with a colon.**
- **Use tick marks to increase clarity and accuracy**, and **consider labeling
  them** (numbers or words). **Don't label every tick** unless needed to avoid
  confusion.
- **Prefer horizontal sliders** — gesturing side to side is easier than up and down.
- **Create custom glyphs if needed** — the system shows plus and minus by default.

## Steppers
- **Make the value a stepper affects obvious** — a stepper displays no value itself.
- **Consider pairing a stepper with a text field when large changes are likely** —
  steppers alone suit small changes of a few taps.
- **macOS: consider supporting Shift-click for large value ranges** to change the
  value quickly.

## Virtual keyboards
- **Choose a keyboard matching the content type** — numbers and punctuation, email
  address, URL, phone pad, decimal pad, number pad, name phone pad, web search,
  ASCII capable, etc.
- **Consider customizing the Return key type** if it clarifies the experience.
- **Custom keyboards:** **make sure your custom input view makes sense in context**
  — people need to understand its benefit. **Play the standard keyboard sound while
  people type** — they expect the familiar feedback. **Provide an obvious, easy way
  to switch keyboards** (people know the **Globe key**, which replaces the Emoji key
  when multiple keyboards exist). **Avoid duplicating system keyboard features** —
  the Emoji/Globe and Dictation keys appear automatically on some devices.
  **Consider providing a keyboard tutorial** — learning a new keyboard takes time.
- **Use the keyboard layout guide** so the keyboard feels integrated and important
  parts of your interface stay visible.
- **Place custom controls above the keyboard thoughtfully** (an input accessory
  view).

## Combo boxes (macOS)
- **Populate the field with a meaningful default value from the list** that refers
  to the hidden choices.
- **Use an introductory label** — title-style capitalization, ending with a colon.
- **Provide relevant choices** — people value both entering a custom value and
  choosing from likely options.
- **Make sure list items aren't wider than the text field** — truncation is hard to
  read.

## Color wells / image wells / digit entry views
- **Color well: consider the system-provided color picker** — consistent, and lets
  people reuse saved colors across apps.
- **Image well: revert to a default image when necessary** if the well requires one
  and people clear it. **If it supports copy and paste, make the standard menu
  items available** (people also expect the keyboard shortcuts).
- **Digit entry view (tvOS): use secure digit fields** (asterisks) for sensitive
  data, and **clearly state the purpose** with a title and prompt explaining why
  digits are needed.

## Charts (component)
- **Choose a mark type based on what you want to communicate** (bar, line, point…).
- **Consider combining mark types when it adds clarity** — point marks on a line to
  highlight individual data points.
- **Use a fixed or dynamic axis range depending on meaning.** Fixed = bounds never
  change; dynamic = bounds vary with the data.
- **Define the lower bound based on mark type and usage** — **bar charts usually
  work best with zero** so people can visually compare bar lengths.
- **Prefer familiar sequences in tick and grid-line labels** — 0, 5, 10… is
  instantly readable.
- **Tailor grid lines and labels to the use case** — too many overwhelm and distract
  from the data; too few make values hard to estimate.
- **Write descriptions that help people understand what a chart does *before* they
  view it** — information-rich titles and labels.
- **Summarize the main message** — don't make people derive it from the data alone.
- **Establish a consistent visual hierarchy** — **the data itself most prominent**,
  descriptions and axes supporting.
- **In a compact environment, maximize the plot area's width.**
- **Make every chart accessible** — support VoiceOver; **consider Audio Graphs**
  (customize with a chart title and description); **write accessibility labels
  supporting the chart's purpose** (Maps' elevation chart describes *change in
  elevation over the route*); **hide visible axis and tick labels from assistive
  technologies** — VoiceOver conveys values and trends another way.
  Writing those labels:
  - **Prioritize clarity and comprehensiveness.** Reporting a bare data value is
    rarely enough — include the context that makes it meaningful (**the date or
    location associated with it**). Concisely set context **without repeating
    information available another way** (an axis name Audio Graphs or your
    overview already provides), then follow with a succinct description of the
    element's details.
  - **Avoid subjective terms.** Words like *rapidly*, *gradually*, *almost*
    communicate **your** interpretation. **Use actual values** so people form
    their own.
  - **Describe what the chart's details REPRESENT, not what they look like.**
  - **Maximize clarity by avoiding ambiguous formats and abbreviations** —
    *"June 6" is clearer than "6/6"; "60 minutes" or "60 meters" is clearer than
    "60m".*
  - For a chart using red and blue to distinguish two series, **label what each
    series represents — describing the colors adds noise and distracts.**
- **Let people interact with the data when it makes sense — but never require
  interaction to reveal critical information.**
- **Make it easy for everyone to interact** — small marks are hard to target for
  people with reduced motor control.
- **Make interactive charts navigable via keyboard commands (including Full
  Keyboard Access) and Switch Control**, which visit elements linearly by default.
- **Help people notice important changes** — animate changes to marks or axes, or
  people misread the chart.
- **Align a chart with surrounding interface elements** — typically leading edges.
- **Never rely solely on color** to differentiate data or communicate essential
  information.
- **Add visual separation between contiguous areas of color** — e.g. in a stacked
  bar chart where adjacent marks have different colors.
- **watchOS: avoid requiring complex chart interactions** — prefer glanceable
  information with simple interactions.

## Image views
- **Use when the primary purpose is simply to display an image.** For an
  interactive image, **configure a system-provided button** instead.
- **For an icon, prefer a symbol or interface icon over an image view.**
- **Take care when overlaying text on images** — it reduces both image clarity and
  text legibility; ensure contrast.
- **Use a consistent size for all images in an animated sequence** — prescaling to
  fit means the system does no scaling work.
- **macOS: use an image well for an editable image view** (supports copy, paste,
  drag, Delete-to-clear); **use an image button for a clickable image.**
- **watchOS: use SwiftUI for animations** where possible.

## Text views
- **Use for text that's long, editable, or in a special format** — text views offer
  the most options for specialized text.
- **Keep text legible** — multiple fonts, colors, and alignments are possible, but
  **adopt Dynamic Type** so text stays readable.
- **Make useful text selectable** — error messages, serial numbers, IP addresses.
- **Show the appropriate keyboard type** when editing.

## Web views
- **Support forward and back navigation when appropriate** — web views support it
  but **it isn't available by default**.
- **Never use a web view to build a web browser.** Brief in-app website access is
  fine; **Safari is the primary way people browse the web.**

## Progress indicators
- **When possible, use a determinate progress indicator** — indeterminate shows
  something is happening but doesn't help people estimate duration.
- **Be as accurate as possible when reporting advancement.** Consider **evening out
  the pace** so people feel confident about the remaining time.
- **Keep progress indicators moving** — a stationary indicator reads as a **stalled
  process or frozen app**. If a process stalls, say so.
- **When possible, switch from indeterminate to determinate** once duration becomes
  knowable.
- **Never switch from the circular style to the bar style** — different shapes and
  sizes; transitioning disrupts the interface.
- **Display a description only if it provides context** — accurate and succinct.
  **Avoid vague terms like *loading* or *authenticating*** — they seldom add value.
- **Display progress indicators in a consistent location.**
- **When feasible, let people halt processing** — include a **Cancel** button when
  interruption is safe.
- **Let people know when halting has a negative consequence** — an alert confirming
  cancellation or resuming, when progress would be lost.
- **Refresh controls: perform automatic content updates periodically** — don't make
  people responsible for initiating refreshes. **Supply a short title only if it
  adds value** — usually the animation is enough.
- **Prefer an activity indicator (spinner) for background operations or constrained
  space** — small and unobtrusive. **Avoid labeling a spinner** — it appears right
  after people initiate a process, so a label is usually unnecessary.

## Gauges
Displays a specific numerical value within a range.
- **Write succinct labels describing the current value and both endpoints.** Not
  every style displays all labels, but **VoiceOver reads the visible ones**.
- **Consider filling the path with a gradient to communicate purpose** — red-to-blue
  for hot-to-cold temperature.
- **Capacity indicator styles:** **continuous** (a translucent track filling with a
  solid bar) and **discrete** (equally sized rectangular segments matching total
  capacity, filling **completely — never partially**).
- **Consider the continuous style for large ranges** — discrete segments become too
  small to be useful.
- **Consider changing the fill color to mark significant parts of the range** —
  default is green.

## Rating indicators
- **Make it easy to change rankings** — let people adjust an item's rank **inline**,
  without navigating to a separate editing screen.
- **If you replace the star with a custom symbol, make its purpose clear** — the
  star is highly recognizable as a ranking symbol; other symbols may not read as a
  rating scale.

## Activity rings (watchOS/iOS)
- **Display Activity rings when relevant to your app's purpose** — expected in
  health/fitness apps, especially those contributing to HealthKit.
- **Use Activity rings ONLY to show Move, Exercise, and Stand.** **Never replicate
  or modify them for other purposes.**
- **Show progress for a single person only** — never multiple people — and make it
  obvious whose progress it is via a label, photo, or similar.
- **Always keep the visual appearance identical wherever you display them.**
- **Use matching colors for labels or values directly associated with a ring** —
  for the *Move*, *Exercise*, *Stand* labels and current values.
- **Maintain Activity ring margins** — a **minimum outer margin no smaller than the
  distance between rings**. Never let other elements crop, obstruct, or encroach.
- **Differentiate other ring-like elements from Activity rings** using padding,
  lines, or labels — mixing ring styles is visually confusing.
- **Don't send notifications repeating what the Activity app already sends.**
- **Never use Activity rings for decoration** — not in labels or background
  graphics.
- **Never use Activity rings for branding** — not in your app icon or marketing.
