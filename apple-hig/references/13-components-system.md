# Components: system experiences (HIG "System experiences")

Widgets, Live Activities, notifications, controls, complications, watch faces,
Top Shelf, App Shortcuts, snippets, status bars — your app **outside** your app.

## Widgets
- **Choose simple ideas that relate to your app's main purpose** — timely content
  and relevant functionality.
- **Give quick access to the content people want** — meaningful content, useful
  actions, deep links to key areas.
- **Prefer dynamic information that changes throughout the day.** *If content never
  appears to change, people won't keep the widget in a prominent position.*
- **Look for opportunities to surprise and delight** — a unique treatment on
  birthdays or holidays.
- **Offer multiple sizes when it adds value.** Small = typically one piece of
  information; larger = additional layers.
- **Balance information density.** *Sparse layouts make the widget seem
  unnecessary; overly dense layouts are less glanceable.*
- **Display only information directly related to the widget's main purpose.**
- **Use brand elements thoughtfully** — colors, typefaces, stylized glyphs for
  recognizability, **without overpowering useful information.**
- **Choose between automatic content and letting people customize it.**
- **Avoid mirroring your widget's appearance within your app.** An element that
  looks like your widget but doesn't behave like it confuses people.
- **Let people know when authentication adds value** — when signing in unlocks more.
- **Keep your widget up to date** — match update frequency to how often the data
  changes and when people need to see it.
- **Use system functionality to refresh dates and times** — update opportunities are
  limited, so let the system handle it and preserve your budget.
- **Use animated transitions to bring attention to data updates** — standard and
  custom animations **up to two seconds**.
- **Offer simple, relevant functionality; reserve complexity for your app.**
- **Ensure an interaction opens your app at the right location** — deep link to the
  details and actions related to the widget's content.
- **Offer interactivity while remaining glanceable and uncluttered** — avoid
  app-like density of interaction targets.
- **Use standard margins — 16 pt for most widgets** — to avoid crowding the edges.
- **Coordinate your content's corner radius with the widget's corner radius** — use
  a SwiftUI container to apply it.
- **Prefer the system font, text styles, and SF Symbols.**
- **Avoid very small font sizes — 11 pt or larger** in general.
- **Display content so it remains legible from a range of distances** — a widget is
  read at arm's length on a phone and across a room on a Mac or a Smart Stack.
- **Test your widgets across the full range of system color palettes and in
  different lighting conditions.**
- **Never rasterize text** — text elements scale well and let VoiceOver speak them.
- **Use color to enhance without competing with content.**
- **Convey meaning without relying on specific colors** — widgets can appear
  **monochromatic** (with or without a custom tint), and **watchOS may invert
  colors**.
- **Use full-color images judiciously.** With a tinted or clear appearance the
  system **desaturates full-color images by default**.
- **Support light and dark appearances** — light backgrounds for light, dark for
  dark; consider semantic system colors.
- **Group components into an accented and a primary group** for accented rendering
  mode.
- **Offer enough contrast for vibrant rendering mode** — pixel opacity determines
  the strength of the blurred background material effect.
- **Create optimized assets for the vibrant effect** — render images, numbers, and
  text at **full opacity**; **white or light gray for the most prominent content,
  darker grayscale for less prominent.**
- **Design a realistic preview for the widget gallery** highlighting the widget's
  capabilities per type and size.
- **Design placeholder content that helps people recognize your widget** while data
  loads.
- **Write a succinct widget description** for the gallery — **begin with an action
  verb** ("See the current…").
- **Group your widget's sizes together and provide a SINGLE description** — so people
  don't think each size is a different widget, and to avoid repetition.
- **Consider coloring the Add button** that appears below your widget group in the
  gallery, to reinforce your brand.
- **Offer Live Activities for real-time updates.** **Widgets don't show real-time
  information** — if people track a task or event with frequent updates over a
  limited time, that's a Live Activity. They share frameworks and design language, so
  developing them together is sensible.

### Widgets in specific placements
- **Lock Screen / Always-On (iPhone):** devices with the Always-On display render
  widgets **with reduced luminance** — **use levels of gray with enough contrast**
  and keep content legible.
- **StandBy:** **limit rich images and color for conveying meaning.** Use the extra
  space to **scale up and rearrange text** so people can read it from a greater
  distance. **Don't use a background color in StandBy** — it must blend with the
  black background.
- **watchOS Smart Stack:** **provide a colorful background that conveys meaning** —
  the default is black; Stocks uses **red for falling values, green for rising**.
  **Encourage the system to display or elevate your widget** by supplying relevance
  information (location-based, or tied to ongoing actions like a workout) —
  `RelevanceKit`.

### visionOS widgets (spatial)
- **Adapt your design and content for the spatial experience.** In visionOS widgets
  **don't float in isolation** — they're part of living rooms, kitchens, and offices.
  **Think of a widget as part of someone's surroundings**, from the start.
- **Design a responsive layout for BOTH viewing thresholds.** **At a distance:** a
  simplified version — fewer details, **larger type**, and **remove interactive
  elements like buttons and toggles**. **Nearby:** more detail, smaller type.
- **Offer widget family sizes that fit a person's surroundings.** Widgets **map to
  real-world dimensions and have a permanent presence** in the space — consider
  whether yours will be wall-mounted, on a sideboard, or beside a workspace.
- **Mounting style:** **elevated** (the default) suits content that should stand out
  and feel present — reminders, media, glanceable data. **Recessed** suits immersive
  or ambient content like weather or editorial.
- **Test elevated widget designs at every system-provided frame width.** People choose
  the frame width, **you can't change layout based on their choice** — so the layout
  must stay visually balanced at all of them.
- **Style: paper** gives a print-like look that feels like a real object in the room —
  **the entire widget responds to ambient lighting** (the Music poster widget displays
  albums like framed artwork). **Style: glass** suits **information-rich** widgets —
  it separates foreground from background so you choose what adapts to surroundings;
  **foreground elements stay in full color, unaffected by ambient lighting**, keeping
  important content sharp and legible.

## Live Activities
- **Offer them for tasks and events with a defined beginning and end** — best for
  **short to medium duration activities that don't exceed eight hours.**
- **Focus on important information people need at a glance** — you don't need to
  display everything.
- **Never display ads or promotions.**
- **Avoid sensitive information** — they're prominently visible on the Lock Screen
  and Always-On display, viewable by casual observers.
- **Match your app's visual aesthetic and personality in both dark and light.**
- **If you include a logo mark, display it without a container** — and **don't use
  the entire app icon.**
- **Don't add elements to your app drawing attention to the Dynamic Island** —
  other items appear there too.
- **Ensure text is easy to read** — large, **medium weight or heavier**; small text
  sparingly.
- **Adapt to different screen sizes and presentations.**
- **Adjust element size and placement for efficient use of space** — use only the
  space you need.
- **Use familiar layouts** — templates with default system margins and recommended
  text sizes are in Apple Design Resources.
- **Use consistent margins and concentric placement** — even, matching margins
  between rounded shapes and the edges, **including corners.**
- **When separating a block of content, use an inset container shape or a thick
  line. Don't draw content all the way to the edge of the Dynamic Island.**
- **Dynamically change the height on the Lock Screen and in the expanded
  presentation** — shrink when there's less to show.
- **Use color to express the character and identity of your app.** Live Activities in
  the Dynamic Island use a **black opaque background**, so **bold colors for text and
  objects** are how personality comes through.
- **Background color:** you **can't** customize it for compact, minimal, and
  expanded presentations — only for the Lock Screen presentation.
- **Tint the key line color to match your content.** On a dark background a key line
  appears around the Dynamic Island to distinguish it.
- **Use animations to reinforce information and highlight updates.**
- **Animate layout changes**, e.g. expanding to fill the screen in StandBy.
- **Try to avoid overlapping elements** — animate elements out and back in at a new
  position rather than colliding.
- **Make sure tapping opens your app at the right location.**
- **Focus on simple, direct actions.** Buttons and toggles **take space that could
  show useful information** — only for essential, directly related functionality.
- **Consider letting people respond to event or progress updates.**
- **Start Live Activities at appropriate times and make them easy to turn off in
  your app.**
- **Offer an App Shortcut that starts your Live Activity.**
- **Update only when new content is available** — otherwise maintain the display.
- **Alert people only for essential updates** — alerts light up the screen and play
  the notification sound by default.
- **Let people track multiple events with a single Live Activity** rather than
  several they must jump between.
- **Always end a Live Activity immediately when the task or event ends**, and
  consider setting a custom dismissal time.
- **Start with the iPhone design, then refine for other contexts.**
- **Compact presentation:** show dynamic, essential, easy-to-understand
  information. **Design leading and trailing elements to read as a single piece**
  despite the TrueDepth camera between them. **Keep content as narrow as possible,
  snug against the camera** — no padding between content and camera; **don't
  obscure key status bar information.** **Both elements link to the same screen.**
- **Minimal presentation:** must stay recognizable — **prefer updated information
  over just a logo.**
- **Expanded presentation:** an enlarged version of compact/minimal — **maintain
  relative element placement** for coherence. **Wrap content tightly around the
  TrueDepth camera.** **Never replicate notification layouts** — create a unique
  layout.
- **Lock Screen:** choose colors that work on a **personalized** Lock Screen
  (wallpapers, tints, widgets). **Check contrast in Dark Mode and Always-On.**
  **Verify the system-generated dismiss button color.** **Standard layout margin
  is 14 pt.**
- **StandBy:** update the layout — assets must look great at larger scale; consider
  a custom layout using the extra space. **Consider the default background color**
  (blends with the device bezel). **Use standard margins and don't extend graphics
  to the screen edge** — content gets cut off and feels broken. **Verify your
  design in Night Mode** (the system applies a **red tint**).
- **CarPlay:** consider a custom layout via `ActivityFamily` for larger text or more
  information. **The system deactivates interactive elements** — don't depend on
  buttons or toggles there.
- **watchOS:** consider a custom layout showing more information and interactivity
  (the same layout also applies in CarPlay, where interaction is deactivated).
  **In the Smart Stack, focus on essential information and significant updates.**

## Notifications
- **Provide concise, informative notifications.**
- **Avoid multiple notifications for the same thing**, even if someone hasn't
  responded — people attend to them at their convenience.
- **Avoid telling people to perform tasks within your app** — offer notification
  **actions** for simple tasks instead.
- **Use an alert — not a notification — for an error message.**
- **Handle notifications gracefully when your app is in the foreground.** Your
  notifications don't appear when your app is in front, but **you still receive the
  information** — surface it in the UI.
- **Avoid sensitive, personal, or confidential information** — you can't predict
  what people will be doing when it arrives.
- **Create a short title if it provides context** — brief enough to read at a
  glance, **especially on Apple Watch.**
- **Write succinct, easy-to-read content** — complete sentences, sentence case,
  proper punctuation. **Don't truncate — the system does it automatically.**
- **Provide generically descriptive text for when previews aren't available** —
  people can hide previews for all apps.
- **Avoid including your app name or icon** — the system displays a large app icon
  at the leading edge automatically.
- **Consider a supplementary sound** to distinguish your notifications.
- **Provide beneficial actions** — common, time-saving tasks that avoid opening
  the app.
- **Never provide an action that merely opens your app** — tapping the notification
  already does that.
- **Prefer nondestructive actions.** With a destructive one, give enough context to
  avoid unintended consequences (the system styles them distinctly).
- **Provide a simple, recognizable interface icon for each action.**
- **Badges: use only to show the number of unread notifications.** Never for
  unrelated numeric information (weather data, dates, prices).
- **Never make badging the only way to communicate essential information** — people
  can turn it off.
- **Keep badges up to date** — clear as soon as people open the notifications.
- **Never create a custom image or component mimicking a badge** — people who turned
  badges off will be frustrated.
- **watchOS short look:** **never the only way to communicate important
  information** — it appears only briefly. **Keep privacy in mind** — short looks
  are meant to be discreet; **avoid sensitive information in the title.**
- **watchOS long look:** **consider a rich, custom long look** so people get what
  they need without launching the app. **At minimum provide a static interface;
  prefer a dynamic one too** (the system falls back to static, e.g. with no
  network). **Choose a sash background appearance** (the sash shows your app icon
  and name — customizable color or blurred). **Choose a content-area background
  color** — transparent by default; **white at 18% opacity** matches other system
  notifications. **Provide up to four custom actions below the content area.**
  **Keep double tap in mind when ordering actions — double tap runs the first
  nondestructive action**, so put the most likely response first.

## Controls
- **Offer controls for actions that provide the most benefit without launching your
  app** — e.g. launching a Live Activity from a control.
- **Update controls on interaction, on action completion, or remotely via push.**
- **Choose a descriptive symbol suggesting the control's behavior** — depending on
  where it's added it **may not display the title and value**, so the symbol must
  carry enough information alone.
- **Use symbol animations to highlight state changes** — animate both on and off
  transitions for toggles; **animate indefinitely for actions with a duration.**
- **Select a tint color that works with your brand** — applied to a toggle's symbol
  in its **on** state.
- **Help people provide additional information the system needs** — e.g. choosing
  which light to control.
- **Provide hint text for the Action button** — shown on press to explain what
  press-and-hold does.
- **If the title or value can vary, include a placeholder** describing what the
  control does.
- **Hide sensitive information when the device is locked** — have the system redact
  the title and value.
- **Require authentication for actions affecting security** — unlocking a house
  door, starting a car.
- **Camera controls: use the same camera UI in your app and your camera
  experience** so the transition is seamless. **Provide instructions for adding the
  control.**

## Status bars (iOS/iPadOS)
- **Obscure content under the status bar.** It's transparent by default, which can
  make status information hard to see.
- **Consider temporarily hiding the status bar for full-screen media.**
- **Never permanently hide the status bar** — people then must leave your app to
  check the time or Wi-Fi. **Let people redisplay a hidden status bar with a simple
  gesture.**

## App Shortcuts
- **Consider adopting app schemas instead** to surface common functionality
  throughout the system, if your app is in a common domain area.
- **Offer App Shortcuts for your most common and important tasks** — ideally tasks
  people complete **without leaving their current context**.
- **Add flexibility by letting people choose from a set of options** — an App
  Shortcut can include **a single optional parameter**.
- **Ask for clarification when a request is missing optional information.**
- **Keep voice interactions simple.** *If your phrase feels too complicated said
  aloud, it's too hard to remember or say correctly.*
- **Make App Shortcuts discoverable in your app** — occasional tips.
- **Provide enough detail for audio-only devices** (AirPods, HomePod) where people
  can't see the screen.
- **Provide brief, memorable activation phrases and natural variants.**
- **Naming: "App Shortcuts" and the "Shortcuts" app take title case, and *Shortcuts*
  is plural.** Individual shortcuts are **lowercase** ("Run a shortcut by asking
  Siri…").
- **Order shortcuts by importance** — the order determines their initial appearance
  in Spotlight and the Shortcuts app.

## Snippets
- **Ensure legibility** — sufficient contrast between custom content and the
  system-provided background **in both light and dark**, with consistent margins.
- **Keep content concise** — snippets facilitate lightweight, quick interactions.
- **Choose a descriptive label for a confirmation snippet's primary button**
  (`ConfirmationActionName` or a custom label).
- **Communicate a snippet's purpose visually.** **Don't rely on the spoken dialogue
  text** — it's essential when people aren't looking, but the visual must stand
  alone.

## Complications (watchOS)
- **Identify essential, dynamic content people want at a glance.** Launching the app
  is secondary — **the glanceable data is what people appreciate.**
- **Support all complication families when possible** — more families = available on
  more watch faces.
- **Consider multiple complications per family** — enables shareable watch faces
  centered on your app.
- **Define a different deep link for each complication** — each should open the most
  relevant area.
- **Keep privacy in mind** — the **Always-On Retina display** means the watch face
  may be visible to people other than the wearer.
- **Carefully consider when to update data** — data is a **timeline** where each
  entry specifies the time to display it.
- **Choose a ring or gauge style based on the data.**
- **Make sure images look good in tinted mode** — the system applies a solid color
  to text, gauges, and images and **desaturates full-color images** unless you
  provide alternatives. **Recognize people may prefer tinted mode over full color.**
- **Use line widths of two points or greater** — thinner lines are hard to see at a
  glance, **especially when the wearer is in motion.**
- **Provide static placeholder images for each complication you support.**

## Watch faces (watchOS)
- **Share watch faces featuring your complications** to help people discover your
  app.
- **Display a preview of each watch face you share.**
- **Aim to offer shareable watch faces for all Apple Watch devices** — some faces
  (California, Chronograph Pro, Gradient, Infograph, Infograph Modular…) are
  **Series 4 and later only.**
- **Respond gracefully if people choose an incompatible watch face** — the system
  sends an error on Series 3 or earlier.

## Top Shelf (tvOS)
- **Help people jump right into your content.**
- **Feature new content** — new releases and episodes, upcoming movies and shows.
  **Avoid promoting content people already purchased, rented, or watched.**
- **Personalize people's favorite content** — people put their most-used apps in
  Top Shelf, so target recommendations.
- **Avoid advertisements and prices.** *People put your app in Top Shelf because
  you've already sold them on it.*
- **Showcase compelling dynamic content.** Static images are a fallback — **supply
  at least one** if you don't provide the recommended full-screen content.
- **Avoid implying interactivity in a static image** — it isn't focusable.
- **Provide a title** — the show, movie, or album title; optionally a brief
  subtitle. **Identify the currently playing content** near the top of the screen.
- **Provide enough content to constitute a complete row** — enough images to span
  the full screen width, plus at least one label.
- **Be aware of additional scaling when combining image sizes** — images scale up to
  match the row height.
- **Scrolling banner: provide three to eight images.** Fewer than three feels
  ineffective; more than eight makes navigation hard.
- **If you need text, add it to the image** — this layout shows no labels under
  content. In layered images, consider elevating the text to its own layer.
