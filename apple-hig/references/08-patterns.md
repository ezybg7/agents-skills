# Patterns (HIG) — how experiences behave over time

Patterns are *flows*, not widgets. They answer "what happens when…".

## Launching
- **Launch instantly.** People sometimes don't want to wait **more than a couple
  of seconds**.
- **Provide a launch screen where the platform requires it** (iOS, iPadOS, tvOS —
  **not** macOS, visionOS, watchOS).
- **Downplay the launch experience.** A launch screen "isn't an opportunity for
  artistic expression." Its **sole function** is to make the app feel quick to
  launch and immediately ready.
- **Design a launch screen nearly identical to your first screen.** Different
  elements cause an **unpleasant flash** on transition. Solid color first screen →
  launch screen is only that solid color. Match the device's current
  **orientation and appearance mode**.
- **Avoid text on the launch screen** — its content doesn't change, so text
  **won't be localized**.
- **Don't advertise.** No logos or branding unless they're a fixed part of the
  first screen. It's not a splash screen or an About window.
- **Restore the previous state on restart.** Restore **granular** detail — scroll
  position, window state and location. Don't make people retrace steps.
- **iOS/iPadOS:** launch in the device's **current** orientation if you support
  both. A landscape-only interface must work whether people rotated left or right.
- **visionOS:** consider **launching in the Shared Space even if fully
  immersive** — gives context while loading and lets people choose when to
  transition to a Full Space (they may be running other apps).
- **tvOS live-viewing:** consider auto-starting playback after a few seconds of
  inactivity.

## Onboarding
Ideally people understand the app **by experiencing it**. Onboarding happens
*after* launching — it is **not** part of the launch experience. Design it
**fast, fun, and optional**.
- **Teach through interactivity.** People retain more by *performing* the task
  than by viewing instructional material. Let them safely test an action.
- **Consider context-specific tips instead of one onboarding flow** (TipKit).
  A contextual tip lets people concentrate on a single action before meeting new
  information. Display instructions **near the interface area they refer to**.
- **If a prerequisite flow is needed, keep it brief and enjoyable** and don't make
  people memorize a lot. Teaching too much overwhelms and reduces recall.
- **Make a separate tutorial optional.** If skipped at first launch, **don't
  present it again** — but keep it easy to find later (help, account, settings).
- **Keep onboarding focused on your experience** — people don't need to learn how
  to use the system or the device.
- **Postpone nonessential setup and customization.** Provide reasonable defaults.
- **If you need private data before the app can function, integrate the permission
  request into onboarding** so you can show why and what the benefit is.
  Otherwise, request when people **first access the specific function**.
- **Let people experience the app before prompting for ratings or purchases.**
- **Don't let large downloads hinder onboarding** — include enough media in the
  package to start immediately.
- **Avoid licensing details in onboarding** — let the App Store display agreements.
- **Splash screen:** display just long enough to absorb at a glance without
  feeling delayed. If you have onboarding, put it at the start of that flow.

## Loading
"The best content-loading experience finishes before people become aware of it."
- **Show something as soon as possible.** Absence of content reads as **a problem
  with your app**. Use placeholder text/graphics/animations, replacing them as
  content arrives.
- **Let people do other things while content loads** (background loading).
- **If loading is unavoidably long, give people something interesting to view** —
  gameplay hints, tips, new features. **Gauge remaining time accurately** so
  placeholder content is neither too brief to enjoy nor repeated.
- **Download large assets in the background** (Background Assets framework) —
  immediately after installation, during updates, or other nondisruptive times.
- **Communicate that content is loading and how long it might take.**
  **Determinate** progress indicator when you know the duration; **indeterminate**
  when you don't.
- **For games, consider a custom loading view** matching the game's style.
- **watchOS: avoid loading indicators** — people expect quick interactions. But
  **a loading indicator beats a blank screen** if content needs a second or two.

## Modality
Modality = a separate, dedicated mode that **prevents interaction with the parent
view and requires an explicit action to dismiss**. Use it to: deliver critical
information; let people confirm/modify their most recent action; support a
distinct, narrowly scoped task without losing context; or give an immersive
experience.
- **Present modally only when there's a clear benefit** — it takes people out of
  context. Justify it by focus or by choices affecting content/device.
- **Keep modal tasks simple, short, streamlined.** Too complicated and people
  **lose track of the suspended task**, especially if the modal obscures context.
- **Avoid an "app within your app."** A hierarchy of views inside a modal makes
  people forget how to retrace steps. If subviews are required, provide **a
  single path** through the hierarchy and **avoid buttons mistakable for the
  dismiss button**.
- **Consider full-screen modal style for in-depth content or complex tasks** —
  videos, photos, camera views, markup, photo editing. (In visionOS Shared Space
  this fills a window; in a Full Space it can become more immersive.)
- **Always give an obvious way to dismiss**, following platform convention:
  iOS/iPadOS/watchOS → button in the **top toolbar** or **swipe down**;
  macOS/tvOS → button in the **main content view**.
- **Confirm before closing if it could lose user-generated content** — regardless
  of whether people used a gesture or a button. (iOS: an action sheet with a save
  option.)
- **Make it easy to identify a modal view's task** — a title naming the task, plus
  descriptive or guiding text.
- **Let people dismiss one modal view before presenting another.** Multiple
  simultaneous modals create clutter and cognitive load, especially when one hides
  another. **An alert may appear on top of everything — but never show more than
  one alert at a time.**

## Feedback
Feedback tells people what's happening, what they can do next, results of
actions, and how to avoid mistakes. **Match the significance of the information
to the way it's delivered** — status passively; possible data loss interrupts.
- **Make all feedback accessible.** Use **color, text, sound, and haptics
  together** so people receive it whether they silence the device, look away, or
  use VoiceOver.
- **Integrate status feedback into your interface** near the items it describes,
  so people get it without acting or leaving context. (Mail shows last update and
  unread count in the mailbox toolbar.)
- **Use alerts for critical — ideally actionable — information.** Alerts disrupt by
  design; **overuse costs them their impact.**
- **Warn when a task can cause unexpected and irreversible data loss.**
  **Don't warn when data loss is the expected result** (the Finder doesn't warn on
  every file you throw away).
- **Confirm significant completed actions** (an Apple Pay transaction). Reserve
  this for important activities — people **expect success, so they mainly need to
  know when it fails.**
- **Show when a command can't be carried out, and why.**
- **watchOS: avoid indeterminate progress indicators.** An animated indicator makes
  people think they must keep watching. Instead **reassure them they'll get a
  notification when it completes.**

## Undo and redo
People will try undo **repeatedly** until something changes, often without
remembering which action they're targeting — so **help them predict the outcome
and highlight the result**.
- **Help people predict the results.** Describe the result in the shake-to-undo
  alert; label menu items specifically — "Undo Typing", "Redo Bold".
- **Show the results of an undo or redo.** If the affected content is offscreen,
  **scroll to reveal it** — otherwise people think nothing happened and repeat it.
- **Let people undo multiple times.** People expect to undo **every action since a
  logical step** like opening a document or saving.
- **Consider reverting multiple changes at once** — a batch of related incremental
  adjustments, or everything since opening/saving.
- **Provide undo/redo buttons only when necessary.** People expect system paths:
  macOS Edit menu, keyboard shortcuts on Mac/iPad, **shake on iPhone**. If you
  must, use **standard system symbols in a toolbar**.
- **iOS/iPadOS: never redefine standard gestures** — three-finger swipe, shake.
- **Briefly and precisely describe the operation to be undone or redone.** The
  alert title automatically prefixes `"Undo "` / `"Redo "` (**including the
  trailing space**); you supply an additional word or two that names what's being
  reversed — "Undo Name", "Redo Address Change".
- **macOS: Edit menu + Command-Z / Shift-Command-Z.**
- *Not supported in tvOS or watchOS.*

## Entering data
Improve it by **pre-gathering as much as possible** and **supporting all input
methods**.
- **Get information from the system whenever possible** — don't ask for what you
  can gather from settings or (with permission) location/calendar.
- **Be clear about the data you need** — a field prompt (`username@company.com`)
  or an introductory label ("Email"). **Prefill reasonable defaults.**
- **Use a secure text-entry field for sensitive data** (`SecureField`). tvOS has
  `isSecureDigitEntry`. In visionOS the system field shows data to the wearer only
  — a secure field **automatically blurs during AirPlay**.
- **Never prepopulate a password field.** Always ask, or use biometric/keychain.
- **Offer choices instead of text entry when possible** — pickers, menus.
- **Let people drag and drop or paste data in.**
- **Dynamically validate field values** as people enter them, with immediate
  feedback. Use a **number formatter** for numeric fields (also formats decimals,
  percentage, currency).
- **Make required data obvious** — e.g. enable Next/Continue **only after** the
  required fields are filled.
- **macOS: use an expansion tooltip** to reveal clipped or truncated field text.

## Searching
- **If search is important, give it a primary position** — the bottom toolbar
  (Notes) or a **dedicated tab** (Photos, Apple TV).
- **Aim to make content searchable through a single location.** One clearly
  identified place. Distinct sections may still warrant local search (Music's
  search filters the current view).
- **Clearly display the current scope** — descriptive placeholder, scope bar, or
  title. (Mail always references the mailbox being searched.)
- **Provide suggestions** — recent searches before typing, predictive suggestions
  while typing (`searchSuggestions(_:)`).
- **Take privacy into account before displaying search history**, and **provide a
  way to clear it**.
- **Make content searchable in Spotlight** by indexing it with descriptive
  **metadata**. **Define metadata for custom file types** (Spotlight File Importer,
  `CSImportExtension`). **Implement a Quick Look generator** for custom file types.
- **Prefer system-provided open and save views** — they include a built-in search
  field covering the whole system.

## Drag and drop
Source → destination. **Same container = move; different container = copy;
between apps = always a copy.**
- **Support drag and drop throughout your app** — people try it everywhere.
  System components (text fields, text views) get it free.
- **Offer alternative ways to accomplish drag-and-drop actions** — menu commands;
  in iOS/iPadOS use `accessibilityDragSourceDescriptors` /
  `accessibilityDropPointDescriptors`.
- **Decide move vs. copy deliberately.** Before changing the defaults, prefer the
  behavior **least likely to cause frustration or data loss**.
- **Support multi-item drag** where it makes sense. iPadOS lets people **add items
  to a group mid-drag**; macOS allows selecting items **from several apps**.
- **Prefer letting people undo a drop.** Ask for confirmation when it can't be
  undone (Finder confirms dragging into a write-only folder). Where undo is
  impossible, offer a way to reverse the result (Photos lets people cancel sharing
  after dropping into a shared stream).
- **Offer multiple versions of dragged content, highest to lowest fidelity**, so
  the destination takes the best it can accept — e.g. PDF vector → lossless PNG
  with transparency → lossy JPEG; or a native chart object → an image of it.
- **Consider spring loading** — dragging content over a button/segmented control
  activates it (Calendar's day/week/month/year segments). Force-click on a Magic
  Trackpad; hover on iPad.
- **Display a drag image as soon as people drag ~3 points.** Make it a
  **translucent** representation — distinguishes it from the original and lets
  people see destinations underneath. Show it until they drop.
- **Modify the drag image to help people predict the result** (a photo expanding
  to its in-document size); use **flocking** to visually group multiple items,
  ungrouping on drop. **Avoid constant, radical changes to the drag image.**
- **Show whether a destination can accept the content** — insertion point or
  highlight when it can; nothing, or an explicit `circle.slash`, when it can't.
  Show cues **only while content is over the destination**, and **identify one
  destination at a time.**
- **Consider displaying a badge during multi-item drags** — a small filled oval
  with the item count. **If a destination accepts only a subset, update the badge
  to the new number.**
- **Extract only the relevant portion of dropped content.** Dragging a contact to
  an email recipient field yields **only the name and email address**, not the
  contact's mailing address.
- **Apply appropriate styling to dropped text.** If source and destination support
  the same text styles, **preserve the original font, typeface, size, and other
  attributes**; otherwise **apply the destination's style**.
- **Provide feedback when dropped content needs time to transfer** — a progress
  indicator, plus a **placeholder at the drop location** in collections, lists,
  and tables so people know where the content will land.
- **Provide feedback when a drop initiates a task or action** (dropping onto a
  print control) — show that it began and keep people informed of progress.
- **When a drop lands on an invalid destination or fails, provide visual feedback** —
  the item can **move back to its source** (if still visible) or **scale up and fade
  out**, giving the impression of evaporating rather than landing.
- **Scroll the contents of a destination when necessary.** Dragging within a
  scrolling container should **auto-scroll** the content so people can find the right
  drop location.
- **As much as possible, let people select and drag with a single motion** — no pause
  between selecting and starting the drag (unless selecting multiple items).
- **After a drop, maintain the content's selection state in the destination**,
  updating the source as needed — **people expect dropped content to stay selected**
  so they can act on it immediately.
- **When there's a choice, pick the richest version of dropped content your app can
  accept.** A dragged chart may offer both the native chart object and a plain image
  — take the native object if you support charts.
- **iPadOS: let people perform multiple simultaneous drag activities.** People can
  **sequentially add items to an in-progress drag session** — starting a drag on one
  app icon, then selecting more before dropping them all together.
- **When possible, launch your app to handle content dropped into empty space.**
  Associating a user activity with draggable content lets your app open a window or
  scene for it (dropping a URL into empty space launches Safari).
- **macOS specifics:**
  - **When a physical keyboard is attached, check for the Option key AT DROP TIME.**
    Holding Option forces a same-container drag to behave like a **copy**; releasing
    Option before dropping makes it a **move**.
  - **Let people drag selected content from an inactive window without first
    activating it.** Selected content in an inactive window is a **background
    selection** and looks different from the active window's selection.
  - **Let people drag individual items from an inactive window without affecting an
    existing background selection** — dragging an unselected file out of an inactive
    Finder window shouldn't deselect that window's selected files.
  - **Consider changing the pointer appearance to indicate the drop result** — the
    *copy*, *drag link*, *disappearing item*, and *operation not allowed* pointers.
  - **Consider letting people drag content into the Finder**, in a format your app
    can reopen later (Calendar exports an event as a `.ics` file people can share or
    drag back in).

## Settings
- **Provide default settings that give the best experience to the largest number
  of people** — auto-detect rather than ask.
- **Minimize the number of settings.** Too many make the experience less
  approachable and any single setting harder to find.
- **Make settings available in expected ways** — **Command-Comma** with a keyboard;
  **Esc** in a game.
- **Don't use settings to ask for setup information you can get another way.**
- **Respect systemwide settings; never duplicate them.** A custom copy of a global
  option implies system settings might not apply to you and that changing yours
  affects other apps.
- **Put general, infrequently changed settings in your settings area** — people
  must suspend their work to get there.
- **Prefer letting people modify task-specific options in place**, in the screens
  they affect — a separate settings area disconnects the option from its context
  and hides the result.
- **Add only the most rarely changed options to the system Settings app**, and
  consider a button that opens it directly.
- **macOS:** settings live in the **App menu** (document-level options → File
  menu); **don't put a settings button in the toolbar**. **Dim minimize and
  maximize.** Use a **noncustomizable toolbar that always shows the active pane**.
  **Update the window title to the current pane** (single pane → "*App* Settings").
  **Restore the most recently viewed pane.**
- **watchOS:** no custom settings in the system Settings app — put a few essential
  options at the bottom of the main view or in a **More** menu.

## Offering help
- **Let your app's tasks inform the type of help.** Simple 1–2 step task → inline
  view. Complex multistep → tutorial. **Relate help to the action happening right
  now**, and make it easy to dismiss or avoid.
- **Use relevant and consistent language and images** — don't show a game
  controller to someone using a Siri Remote; don't say "click" on iPhone or "tap a
  menu item" on Mac.
- **Make all help content inclusive.**
- **Don't explain how standard components work.** Describe what the element does
  **in your app**. For a unique control or nonstandard input use, **prefer
  animation or graphics** over lengthy description.
- **Tips (TipKit):** popover tip preserves content flow; inline tip keeps
  surrounding information visible; annotation-style points at a UI element;
  hint-style isn't tied to specific UI.
  - **Use tips for simple features** — **more than three actions is too
    complicated for a tip.**
  - **Short, actionable, engaging** — **one or two sentences**, direct
    action-oriented language, **no promotional content**.
  - **Define eligibility rules** (parameter- or event-based) so tips reach only
    people who benefit; set frequency to a reasonable cadence, e.g. **once every
    24 hours**.
  - **Include an associated symbol, preferring the filled variant** — but don't
    repeat an image that already appears in the UI the tip points to.
  - **Use buttons** to send people to settings or additional resources.
- **Tooltips (macOS, visionOS — "help tags"):** appear on pointer hover, or on
  **look** in visionOS (`help(_:)`).
  - **Describe only the control people indicated interest in.**
  - **Explain the action the control initiates — begin with a verb**
    ("Restore default settings").
  - **Avoid repeating the control's name.**
  - **Be brief: 60–75 characters max.** Use sentence fragments, omit articles.
    *If you need a lot of text to describe a control, simplify the interface.*
  - **Use sentence case**; omit ending punctuation unless your style requires it.
  - **Consider context-sensitive tooltips** — different text per control state.

## Managing notifications
**You need permission before sending any notification.** People can silence all
notifications (except government alerts in some locales).

**Interruption levels (noncommunication notifications):**
| Level | Meaning | Overrides scheduled delivery | Breaks through Focus | Overrides Ring/Silent |
|---|---|---|---|---|
| **Passive** | View at leisure (restaurant recommendation) | No | No | No |
| **Active** (default) | Might appreciate on arrival (sports score) | No | No | No |
| **Time Sensitive** | Directly impacts, needs immediate attention (security issue, package delivery) | **Yes** | **Yes** | No |
| **Critical** | Urgent health/safety. Extremely rare — government/public agencies, health or home apps | **Yes** | **Yes** | **Yes** |

> **Critical notifications require an entitlement.**

- Direct communications (calls, messages) use **communication** notifications via
  SiriKit intents — the system uses **the sender** to decide delivery.
- **Build trust by accurately representing urgency.** People can turn everything
  off; never use a high level to deliver low-priority information.
- **Time Sensitive only for things relevant in the moment** — happening now or
  **within an hour**. The system explains the level on first use and **periodically
  re-offers people the chance to turn it off.**
- **Never use Time Sensitive for marketing.**
- **Get explicit permission for promotional/marketing notifications** via an alert
  or modal that describes what you'll send with a clear opt in/out.
- **Provide an in-app settings screen** so people can change that choice.
- A Focus may delay the *alert*, **but the notification itself is available as
  soon as it arrives.**
- **watchOS:** iPhone notification settings apply by default; per-notification
  options (Mute 1 Hour, Turn off Time Sensitive) come from swiping left.

## Managing accounts
**Ask for an account only if core functionality requires it.** Prefer
**Sign in with Apple**.
- **Explain the benefits of creating an account and how to sign up**, in the
  sign-in view.
- **Delay sign-in as long as possible.** People abandon apps forced to sign in
  before doing anything useful — a shopping app should let people browse and
  require sign-in only at purchase.
- **Without Sign in with Apple, prefer a passkey** (no password to create or
  enter). If you keep passwords, **add two-factor authentication**.
- **Always identify the authentication method** — "Sign In with Face ID", not
  "Sign In".
- **Refer only to methods available in the current context** — don't mention
  Face ID on a device without it (`LABiometryType`).
- **Avoid an app-specific opt-in for biometric authentication** — it's a
  system-level choice; an in-app setting is redundant and confusing.
- **Avoid the term *passcode*** for account authentication — people will think you
  want their device passcode.
- **Account deletion: if you let people create an account, you must let them
  delete it — not just deactivate.** Comply with regional right-to-be-forgotten
  law. If law compels you to retain data, **describe the situation clearly.**
  - **Provide a clear in-app way to initiate deletion**, or a **direct link** to
    the page that does — **not buried in Privacy Policy or Terms.**
  - **Keep the in-app and web deletion experiences consistent** in length and
    complexity.
  - **Consider letting people schedule deletion** for later (to use remaining
    services), **but also offer immediate deletion.**
  - **Tell people when deletion will complete and notify them when it's done.**
  - **Explain how billing and cancellation work on deletion** — auto-renewable
    subscriptions **continue to bill through Apple until cancelled**, regardless
    of account deletion. Account deletion must be supported **even if the
    subscription wasn't purchased in your app.**
  - Sign in with Apple accounts: **revoke the associated tokens** on deletion.
- **TV provider accounts:** use TV Provider Authentication for system-level
  sign-in. **Don't show a sign-out option when signed in at system level** — if
  you must, direct people to Settings > TV Provider. **Never tell people to sign
  out by adjusting privacy controls** — Settings > Privacy is not a sign-out
  mechanism.
- **tvOS:** ask for the minimum information — most people use a remote, not a
  keyboard. **Prefer letting people use another device to sign up or
  authenticate** (associated domains). **Don't ask people to pick their profile
  every time** on a shared account (tvOS 16+ shares credentials while storing
  profiles separately). **Minimize data entry** — send people to a website on
  another device for anything more than a small amount.

## Charting data
Not every dataset needs a chart — if you only need to *provide* data rather than
convey or analyze it, use a **list or table** people can scroll, search, and sort.
- **Use a chart to highlight important information about a dataset.** Charts are
  visually prominent and draw attention — pay that off by clearly communicating
  what people can learn.
- **Keep a chart simple; let people choose additional details.** Too much data is
  visually overwhelming and **obscures the very relationships you're conveying.**
  Reveal gradually — different levels of detail or subsets. You can offer several
  versions of a chart, each with more functionality than the last.
- **Make every chart accessible.** Beyond visual descriptions, provide
  **accessibility labels describing chart values and components** and
  **accessibility elements for interacting with the chart.** A descriptive
  headline **does not replace accessibility labels.**
- **Prefer common chart types** (bar, line) — people already know how to read them.
- **If a chart presents data in a novel way, teach people to interpret it.**
  (Activity animates each ring individually on first pairing.)
- **Examine data from multiple levels** — macro (totals, averages), mid-level
  (useful subsets), individual points (specific values worth attention).
- **Add descriptive text** — titles, subtitles, annotations; a brief headline or
  summary for at-a-glance grasp (Weather's "Chance of light rain in the next
  hour").
- **Match chart size to functionality, topic, and detail level.** Large enough to
  read details and support the interactivity you want; small charts work for
  glanceable info or a preview of a larger version.
- **Prefer consistency across multiple charts**, deviating only to highlight
  meaningful differences — otherwise you imply the charts are unrelated.
- **Maintain continuity among charts using the same data** — same type, colors,
  annotations, layouts, and descriptive text. (Health Trends: the expanded chart
  reuses the small chart's style, colors, marks, and annotations.)

## Playing haptics
- **Use system-provided haptic patterns according to their documented meanings.**
  If a pattern's documented use case doesn't fit, **don't repurpose it.**
- **Use haptics consistently** — build a clear causal relationship between each
  haptic and the action that causes it.
- **Prefer haptics that complement other feedback.** Match the **intensity and
  sharpness** of a haptic to its visual and auditory partners — coherence feels
  natural, as in the physical world.
- **Avoid overusing haptics.** "Often, the best haptic experience is one that
  people may not be conscious of, but miss when it's turned off."
- **Prefer short haptics complementing discrete events** in apps. Long-running
  haptics suit gameplay flow but **dilute meaning and distract** in an app.
- **Make haptics optional** — the app must still be enjoyable without them.
- **Playing haptics can impact other experiences** — enough physical force to
  disrupt the **camera, gyroscope, or microphone**.

**Standard haptic meanings:** *Notification* (something significant/out of the
ordinary needs attention — same haptic the system plays for arriving
notifications) · *Up* / *Down* (an important value crossed a significant
threshold) · *Success* / *Failure* / *Retry* (action completed / failed / failed
but retryable) · *Start* / *Stop* (an activity people explicitly start and stop,
like a timer) · *Click* (a dial clicking — communicates progress at predefined
increments; **overuse diminishes its utility and overlapping clicks confuse**).

## Multitasking
- **Pause activities requiring attention or active participation when people
  switch away.**
- **Respond smoothly to audio interruptions**, and **be prepared for your audio to
  duck**.
- **Finish user-initiated tasks in the background.**
- **Use notifications sparingly.**
- **Avoid interfering with system-provided multitasking behavior.**
- **Don't pause a window's video playback when people look away from it**
  (visionOS).

## Going full screen
- **Always let people choose when to enter full-screen mode**, and **when to
  exit**.
- **Use the system-provided full-screen experience.**
- **Adjust your layout in full-screen mode, but don't programmatically resize the
  window.**
- **Keep essential features and controls accessible** so people can finish the
  task without exiting.
- **Prioritize content by temporarily hiding toolbars and navigation controls.**
- **Except in games, let people reveal the Dock** in iPadOS/macOS full screen.
- **Help people resume where they left off** when they return.
- **Consider deferring system gestures** to prevent accidental exits.
- **In a game, don't change the display mode when players go full screen.**

## Collaboration and sharing
- **Put the Share button somewhere convenient, like a toolbar.**
- **Customize the share sheet / sharing popover** to the file-sharing types you
  support, if needed.
- **Write succinct phrases summarizing the sharing permissions you support.**
- **Provide a set of simple sharing options that streamline collaboration setup.**
- **Prominently display the Collaboration button as soon as collaboration starts.**
- **Add custom actions to the collaboration popover only if needed.**
- **Consider posting collaboration event notifications in Messages.**

## File management
- **Use app menus and keyboard shortcuts for creating and opening documents.**
- **If you need a custom file browser, support people's understanding of the
  platform's file system.**
- **Help people be confident their work is always preserved** unless they cancel
  or delete it.
- **Hide file extensions by default, but let people view them.**
- **Use a Quick Look viewer so people can preview a file your app can't open**;
  **implement a Quick Look generator for custom file types you produce.**
- **When opening/importing via a file provider extension, show only documents
  appropriate to the current context.**
- **Let people select a destination when exporting and moving documents.**
- **Provide a save interface** for changing a file's name, format, or location;
  consider extending the Save dialog's functionality.
- **Avoid a custom top toolbar** in file interfaces.
- **Help people avoid losing work if they turn off autosaving**, and **make it
  clear when a document has unsaved changes.**

**Document launcher title card (iPadOS/iOS document-based apps):**
- **Assign the title card's buttons to your most important functions.** Primary
  typically creates a new document; secondary offers additional options.
  (Numbers: primary "Start Writing", secondary "Choose a Template".)
- **Provide a background clearly distinct from the accessories and title card** —
  solid color, gradient, or pattern. **Avoid complex images or patterns that
  distract from foreground elements.**
- **Be mindful of accessory placement.** Accessories can sit in front of *and*
  behind the title card to create depth — but the **app name and both buttons
  must remain clearly visible.** Don't clutter with too many accessories.
- **Use animation sparingly.** Too much motion confuses or disorients. Prefer
  **gentle, repeating** animations — an accessory that appears to breathe or sway.

## Printing
- **Make printing discoverable**, and **present the option only when printing is
  actually possible**.
- **Present relevant printing options**; **make interdependencies between options
  clear**; **separate advanced from frequently used features**.
- **Consider letting people preview the effect of a setting**, and **storing
  modified settings with the document**.
- **macOS:** a custom print-panel category for app-specific options; a page setup
  dialog for document-specific page settings.

## Playing audio (selected)
- **Adjust levels automatically when necessary — never adjust the overall
  volume.** Use the **system-provided volume view**.
- **Permit rerouting of audio when possible.**
- **Choose an audio category that fits how your app uses sound.**
- **Respond to audio controls only when it makes sense**, and **never repurpose
  audio controls.** Custom player controls only for commands the system lacks.
- **Let other apps know when you finish playing temporary audio.**
- **Decide how to respond to audio-session interruptions**, and whether to
  **resume automatically** when the interruption ends.
- **Use the system's sound services for short sounds and vibrations.**
- **Design custom sounds for custom UI elements**; **vary sounds people could
  perceive as repetitive.**
- **visionOS: use Spatial Audio**; consider **a range of places sounds originate
  from**; decide whether sound is **fixed to the wearer or tracked by the wearer**.

## Playing video (selected)
- **Use the system video player** for a familiar experience.
- **Always display video at its original aspect ratio.**
- **Support the interactions people expect regardless of input device**;
  **play/pause on Space** from a connected Bluetooth keyboard.
- **Show the expected content immediately; start playback immediately;
  avoid loading screens; minimize loading screen content.**
- **Avoid asking people if they want to resume playback** — and **use the previous
  end time when resuming a long clip**.
- **Avoid letting audio from different sources mix** as viewers switch modes.
- **Defer to content when displaying logos or noninteractive overlays**; **show
  interactive overlays gracefully.**
- **Be prepared for an immediate exit.**
- **visionOS: help people stay comfortable.** In a fully immersive experience,
  **don't let virtual content obscure playback or transport controls**, and
  **don't automatically start a fully immersive playback experience.**
  **Avoid expanding an inline video player to fill a window.**
- **Create a thumbnail track to support scrubbing.**
- **Poster images:** represent the clip's contents; **avoid one that looks like a
  system control.**
- **tvOS:** **ensure a smooth transition to your app** — the TV app **fades to black
  and does not show your launch screen**, so present your own black screen
  immediately before playback to maintain continuity. **Make sure content plays for
  the correct viewer** — with multiple user profiles, the TV app can specify one, and
  your app must switch to it before playback. **Show a contextually relevant screen on
  exit** — a detail view for what they were watching, with an option to resume; if
  there's no detail view, a menu listing that content.
- **watchOS:** **use a RealityKit video player for views like a splash screen or a
  transitional view** — people expect the video to lead into the next experience and
  **don't need playback controls**. **Keep video clips short — no longer than 30
  seconds.** Long clips consume disk space and **make people hold their wrists raised,
  causing fatigue.**
- **Use the recommended sizes and encoding values for media assets.** **Avoid scaling
  video** — it hurts performance and looks suboptimal. **Audio: 64 kbps HE-AAC** gives
  good quality at lower data requirements.

## Ratings and reviews
- **Ask only after people have demonstrated engagement** — after completing a level
  or a significant task. **Never on first launch or during onboarding**; people
  may leave *negative* feedback if asked before they've used the app.
- **Avoid interrupting people mid-task or mid-game.** Find natural breaks.
- **Avoid pestering.** Allow **at least a week or two between requests**, and only
  after additional demonstrated engagement.
- **Prefer the system-provided prompt** (`RequestReviewAction`) — it checks for
  previous feedback, allows an optional written review, lets people opt out
  globally, and **automatically limits display to three times per app per 365
  days.**
- **Weigh resetting your summary rating** on a new release: it reflects the
  current version but **results in fewer total ratings**, which can discourage
  downloads.

## Live-viewing apps (tvOS)
- **Feature live content prominently and make it easy to access** — minimize the
  interval between app start and playing content; **live content in the first
  tab** avoids extra taps.
- **Let people tap once — or not at all — to start playback.** A "Watch Now"
  button over featured/recently-viewed content that **disappears on tap** as
  playback begins.
- **Make sure live content looks live.** People must distinguish live from VOD.
  Actually playing it is the best signal; also mark it visibly.
- **Consider indicating the progress of currently playing live content** — a
  progress bar tells people where they'll land when they jump into something
  already in progress.
- **Give people additional actions and viewing alternatives** — record, restart,
  download — while **playback always remains the primary action.**
- **Consider a content footer for browsing channels during playback**, so people
  browse without leaving live playback.
- **Provide instant visual feedback when people change channels** — confirms
  arrival at the right channel *and* covers streaming load time.
- **Match audio to the current context** — audio should follow live content even
  while people browse with it playing in the background.
- **EPG (electronic program guide):** prominently display current program,
  channel, and time so people can **instantly return to the current channel**.
  **Make browsing effortless** — easy paging, scrolling, jumping, plus a
  **My Channels / Favorites** group. **Group content into familiar categories**
  (Movies, TV Shows, Kids, Sports, Popular) and reuse those categories in the
  content footer. **Let people browse the EPG without leaving current content** —
  keep playing in PiP or the background.
- **Recording:** start/stop from the **info panel** during live streaming; record a
  future program from a **details view**, with the option to record **that program
  or all future episodes**; let people specify **current episode only / new
  episodes only / only games with specific teams**.
- **Cloud DVR:** allow playback, deletion, and recording-setting adjustments in
  content-detail views; **consider a control for managing DVR settings** — e.g.
  auto-deleting watched recordings or content older than N days to avoid running
  out of space.

## Workouts (watchOS)
- **Use workout sessions to provide useful data and relevant controls.** During an
  active session watchOS **keeps displaying your app between wrist raises.**
- **Avoid distracting people with information that's not relevant** — people don't
  need your workout list or other app areas mid-workout.
- **Use a distinct visual appearance to indicate an active workout** — a metrics
  page with real-time updating values reads as "active" at a glance.
- **Provide workout controls that are easy to find and tap** — pause, resume, stop
  — with **clear feedback when a session starts or stops.**
- **Explain what you record when sensor data is unavailable.** Water may block
  heart-rate measurement, but you can still record distance swum and calories.
- **Provide a summary at the end of a session** confirming the workout finished
  and showing recorded information; **consider including Activity rings** so
  people can check current progress.
- **Discard extremely brief sessions** — if a session ends seconds after starting,
  discard automatically or ask whether to record it.
- **Make text legible for people in motion** — large font sizes, high-contrast
  colors, most important information arranged to be easy to read.
- **Use Activity rings correctly** — an Apple-designed element whose colors and
  meanings match the Activity app. **Use them only for their documented purpose.**
