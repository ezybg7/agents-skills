# Components: buttons, menus, toolbars (HIG "Menus and actions")

## Buttons
A button **initiates an instantaneous action**, and combines three attributes:
**Style** (size, color, shape) · **Content** (symbol, text label, or both) ·
**Role** (system-defined semantic meaning that can affect appearance).

- **Make buttons easy to use.** Enough space around a button to distinguish it
  from surrounding components *and* to select it with any input.
  **Hit region ≥ 44×44 pt — in visionOS, 60×60 pt** — for fingertip, pointer,
  eyes, or remote.
- **Always include a press state for a custom button.** Without it a button feels
  unresponsive and people wonder whether their input registered.

### Style
- **Use a prominent visual style for the most likely action in a view** — the
  system applies an accent color to the background. **Keep prominent buttons to
  one or two per view**; too many increase cognitive load and slow the choice.
- **Use style — not size — to distinguish the preferred choice.** Same-size
  buttons signal a coherent set of choices; **different sizes near each other look
  confusing and inconsistent.** Highlight the preferred option with a more
  prominent *style*, and use a less prominent style for the rest.
- **Avoid similar colors on button labels and content-layer backgrounds.** With
  bright, colorful content, **prefer the default monochromatic label appearance.**

### Content
- **Ensure each button clearly communicates its purpose.**
- **Associate familiar actions with familiar icons** — people predict
  `square.and.arrow.up` means share. Prefer SF Symbols / Standard icons.
- **Use text when a short label communicates more clearly than an icon.** A few
  words, **title-style capitalization**, and **start with a verb** — "Add to Cart".
- macOS and visionOS show a **tooltip** after a moment of hover (visionOS: after
  a look).

### Role
| Role | Meaning | Appearance |
|---|---|---|
| **Normal** | No specific meaning | — |
| **Primary** | The default button; most likely choice | App accent color |
| **Cancel** | Cancels the current action | — |
| **Destructive** | Can destroy data | **System red** |

- **Assign the primary role to the most likely choice.** A primary button responds
  to **Return**, and in a temporary view (sheet, editable view, alert) that role
  lets **the view close automatically when people press Return.**
- **Never assign the primary role to a destructive action, even if it's the most
  likely choice.** Visual prominence makes people **choose primary buttons without
  reading them.**

### Platform
- **iOS/iPadOS:** **configure a button to show an activity indicator** for actions
  that don't complete instantly; you can also swap the label
  ("Checkout" → "Checking out…"). The system hides the button image while showing
  the indicator.
- **macOS button types:**
  - **Push button** — the standard type. **Use flexible-height push buttons only
    for tall or variable-height content** (two lines of text, a tall icon);
    otherwise standard. **Append a trailing ellipsis when the button opens another
    window, view, or app** — throughout the system an ellipsis signals additional
    input is needed. **Consider supporting spring loading** (force-click while
    dragging, without dropping).
  - **Square (gradient) button** — initiates an action related to a view, like
    adding/removing table rows. **Symbols or icons, not text. Use in a view, not
    the window frame** (never a toolbar or status bar — use a toolbar item).
    **Avoid introducing labels** — proximity makes the purpose clear.
  - **Help button** — circular, question mark, opens app help. **Use the
    system-provided one. Open the topic related to the current context**, falling
    back to the top level. **No more than one per window.** **In a view, not the
    window frame. Avoid introductory text.** Placement: dialog *with* dismissal
    buttons → lower corner **opposite** the dismissal buttons, vertically aligned
    with them; dialog *without* → lower-left or lower-right; settings window/pane →
    lower-left or lower-right.
  - **Image button** — in a view, not the window frame. **~10 px of padding between
    image edges and button edges** (the edges define the clickable area even when
    invisible). Generally **avoid a system-provided border**. **A label goes below
    the button.**
- **visionOS:** buttons typically have a **visible background** and **play sound**
  as feedback. Three standard shapes: **icon-only → circle; text-only → rounded
  rectangle or capsule; icon + text → capsule.** Four interaction states.
  **Custom hover effects are not supported.**

  | Shape | Mini 28 | Small 32 | Regular 44 | Large 52 | XL 64 |
  |---|---|---|---|---|---|
  | Circular | ✓ | ✓ | ✓ | ✓ | ✓ |
  | Capsule (text only) | | ✓ | ✓ | ✓ | |
  | Capsule (text + icon) | | | ✓ | ✓ | |
  | Rounded rectangle | | ✓ | ✓ | ✓ | |

  - **Prefer a discernible background shape and fill** — except inside a toolbar,
    context menu, alert, or ornament, where the container already provides
    visibility. **On glass, use the thin material as the button background;
    floating in space, use the standard material.**
  - **Never make a custom button with a white background fill and black text or
    icons** — the system reserves that style for the **toggled state**.
  - **Prefer circular or capsule shapes.** Eyes are drawn toward corners, making it
    hard to keep looking at a shape's center; **the more rounded, the easier to
    look at steadily.** A standalone button should be **capsule**.
  - **Button centers at least 60 pt apart.** Buttons **≥ 60 pt need 4 pt of
    padding** so the hover effect doesn't overlap. **Avoid small or mini buttons in
    a vertical stack or horizontal row.**
  - **Text-labeled buttons: rounded rectangle in a vertical stack; capsule in a
    horizontal row.**
  - **Use standard controls for their familiar audible feedback** — especially
    important because **visionOS doesn't play haptics.**
- **watchOS:** all inline buttons are **capsule**; inline with content they gain a
  material effect for legibility.
  - **Prefer buttons that span the full width of the screen for primary actions** —
    they look better and are easier to tap. **If two buttons share a horizontal
    space, give them the same height**, and use images or short labels.
  - **Use the same height for vertical stacks of one- and two-line text buttons.**
  - **Use toolbar buttons for navigation to related areas or contextual actions on
    the view's content** — additional information or secondary actions.

## Toolbars
A toolbar holds **the current view's title, navigation controls and search, and
actions (bar items)**, arranged horizontally along the top or bottom edge in
logical sections. (A **tab bar** is for navigating *between areas* — a toolbar
acts on content, aids navigation, and orients people.)

- **Choose items deliberately to avoid overcrowding.** Define which items move to
  the overflow menu as the toolbar narrows.
  > **The system adds the overflow menu automatically in macOS and iPadOS. Don't
  > add one manually, and avoid layouts that overflow by default.**
- **Add a More menu for additional actions** — prioritize *less* important actions
  for it, try to fit everything in the toolbar first, and only add it if needed.
- **In iPadOS and macOS, consider letting people customize the toolbar** —
  especially valuable in apps with many items, advanced functionality not everyone
  needs, or long usage sessions.
- **Reduce toolbar backgrounds and tinted controls.** Custom backgrounds
  **interfere with the system's background effects.** Let the content layer inform
  the toolbar's color, and use a `ScrollEdgeEffectStyle` to distinguish the toolbar
  from the content area.
- **Avoid similar colors on toolbar item labels and content-layer backgrounds** —
  prefer monochromatic toolbars over colorful content.
- **Prefer standard components.** Standard buttons, fields, headers, and footers
  have corner radii **concentric with the bar's corners** — custom components must
  match that concentricity.
- **Consider temporarily hiding toolbars for a distraction-free experience** —
  contextually, and **always offer a reliable way to restore them.**

### Titles
- **Provide a useful title for each window** — confirms location and
  differentiates multiple open windows. **If a title would be redundant, leave the
  area empty** (Notes doesn't title a single note; multi-window Notes titles each
  with its first line so people can tell them apart).
- **Never title windows with your app name** — it says nothing about the hierarchy.
- **Write a concise title: a word or short phrase, under 15 characters**, leaving
  room for other controls.

### Navigation
- **Use the standard Back and Close buttons and their standard symbols.**
  **Don't use a text label reading "Back" or "Close".** A custom version must look
  the same, behave as expected, and be used consistently throughout.

### Actions
- **Provide actions supporting the main tasks** — usually most-frequent commands,
  sometimes those mapping to the highest-level or most important objects.
- **Make the meaning of each control clear** — don't make people guess or
  experiment. **Prefer simple recognizable symbols over text**, except for actions
  like *edit* that symbols represent poorly.
- **Prefer system-provided symbols without borders.** Borders (outlined circles)
  aren't needed — the section provides a visible container, and the system defines
  hover and selection appearances.
- **Use the `.prominent` style for key actions like Done or Submit** — it separates
  and tints the action as a focal point. **Only one primary action, on the trailing
  side.**

### Item groupings — three locations
- **Leading edge:** return-to-previous-document and show/hide sidebar at the far
  leading edge, then the view title, then optionally a **document menu**
  (Duplicate, Rename, Move, Export). **Leading-edge items are not customizable**,
  so they're always available.
- **Center area:** common useful controls, and the view title if not leading.
  In macOS/iPadOS people can add, remove, and rearrange these when customization is
  enabled, and **these items collapse into the system overflow menu as the window
  shrinks.**
- **Trailing edge:** important always-available items, inspector buttons, an
  optional search field, the More menu, and the primary action (Done).
  **Trailing-edge items stay visible at all window sizes.**

Rules for grouping:
- **Group logically by function and frequency of use.**
- **Group navigation controls and critical actions (Done, Close, Save) in
  dedicated, familiar, visually distinct sections.**
- **Keep groupings and placement consistent across platforms.**
- **Minimize the number of groups — aim for a maximum of three.**
- **Keep actions with text labels separate.** A text action beside a symbol action
  can look like **one combined action**; multiple text buttons can **run
  together**. Insert **fixed space** between them
  (`UIBarButtonItem.SystemItem.fixedSpace`).

### Toolbar platform notes
- **iOS:** space is very limited — **prioritize only the most important items**,
  put the rest in a More menu. **Use a large title** to help people stay oriented:
  it transitions to a standard title on scroll and back at the top
  (`prefersLargeTitles`).
- **iPadOS:** **a toolbar and a tab bar can coexist in the same horizontal space**
  at the top — useful when you want to navigate a few main areas while keeping the
  full window width for content.
- **macOS:** the toolbar sits in the window frame, below or integrated with the
  title bar; **toolbar items don't include a bezel**. **Make every toolbar item
  available as a menu bar command** — the toolbar can be customized or hidden, so
  it can never be the only path to a command. (The reverse isn't true: not every
  menu command deserves toolbar space.)
- **visionOS:** the toolbar sits **along the bottom edge, above window-management
  controls, in a parallel plane slightly in front of the window (z-axis)**. A
  **variable blur** anchors the bar above scrolling content while keeping the
  glass uniform. Supply a symbol **or** a text label per item — **looking at a
  symbol reveals its text label.** **Prefer the system-provided toolbar** (placed
  correctly, optimized for eye and hand input). **Never create a vertical
  toolbar** — tab bars are vertical in visionOS and it would confuse people.
  **Try to prevent windows resizing below the toolbar's width** — visionOS has no
  menu bar, so the toolbar is the reliable path to essential controls.

## Menus
- **Write a label that clearly and succinctly describes each menu item** — a verb
  or verb phrase for actions (View, Close, Select).
- **Use title-style capitalization** — capitalize every word except articles,
  coordinating conjunctions, and short prepositions.
- **Remove articles (*a*, *an*, *the*) to save space** — they lengthen labels and
  rarely add understanding.
- **Show people when a menu item is unavailable** — dimmed and unresponsive.
  **If every item is unavailable, the menu itself must stay available** so people
  can open it and learn what it contains.
- **Append an ellipsis when the action requires more information before it can
  complete** — signals input or additional choices, usually in another view.
- **Represent common actions consistently** with the system's standard icons
  (Share, Print, Search).
- **Use menu item icons sparingly and with purpose** — highlight the most common
  actions, key features, file system locations, connected devices, visual concepts.
- **Apply a uniform visual treatment within a group** — **icons for all items in a
  group, or none.**
- **List important or frequently used items first** — people scan from the top.
- **Group logically related items** and separate groups with a **separator**.
- **Keep all logically related commands in the same group even at different
  importance** — people expect Paste and Paste and Match Style together.
- **Be mindful of menu length.** A long menu costs time and attention and people
  miss the command they want. Divide into separate menus, or shorten with a
  submenu.
- **Use submenus sparingly** — each adds complexity and hides its items. A good
  trigger: **a term appears in more than two menu items in the same group** (Sort
  by Date / Score / Name → a Sort submenu).
- **Limit submenu depth and length** — **restrict to a single level**; **more than
  about five items → make a new menu instead.**
- **A submenu must remain available even when its nested items are unavailable.**
- **Prefer a submenu to indenting menu items** — indentation is inconsistent with
  the system and doesn't express relationships clearly.
- **Consider a changeable label describing current state** — one item toggling
  "Show Map" / "Hide Map" rather than two items.
- **Include a verb if a changeable label isn't clear enough** — "HDR On" is
  ambiguous between action and state; "Turn HDR On" isn't.
- **If it helps, display both menu items instead of one toggled item** — a game
  might list both Take Account Online and Take Account Offline.
- **Consider a checkmark to show an attribute is in effect** — easy to scan for.
- **Consider an item that removes multiple toggled attributes at once** — a "Plain"
  item that clears all formatting.
- **Games:** let players navigate in-game menus with the **platform's default
  interaction method**, and **make sure menus stay easy to open and read on every
  platform** — scaling game content to a small screen can make menus unusable.
- **iOS/visionOS layouts:** **choose a small or medium menu layout to streamline
  choices** (Notes uses medium for Scan, Lock, Pin). **Display a menu near the
  content it controls** — people look at the item before tapping and can miss the
  effect if it's far away. **Prefer the subtle breakthrough effect** for menus
  overlapping 3D content — it preserves depth and context while keeping the menu
  legible.

## Context menus
- **Prioritize relevancy.** A context menu is **not for advanced or rarely used
  items** — it's the commands people most likely need *right now*.
- **Aim for a small number of items** — too long is hard to scan and scroll.
- **Support context menus consistently throughout your app.** Inconsistency makes
  people think something is broken.
- **Always make context menu items available in the main interface too.**
- **Keep submenus to one level.**
- **Hide unavailable items — don't dim them.** (Opposite of regular menus, which
  aid discovery. macOS exceptions: Cut/Copy/Paste.)
- **Place the most frequently used items where people encounter them first** —
  people read from the part **closest to where their finger or pointer opened the
  menu**, so the ordering depends on where it appeared.
- **Show keyboard shortcuts in main menus, not context menus** — the context menu
  *is* the shortcut, so it's redundant.
- **Use separators, but no more than about three groups.**
- **iOS/iPadOS/visionOS: warn about destructive items** — list them **at the end**
  and mark them destructive.
- **Include a title only if it clarifies the menu's effect** — e.g. the number of
  selected messages.
- **Represent actions with familiar icons** — the same ones the system uses for
  Copy, Share, Delete.
- **Provide either a context menu or an edit menu for an item, but never both** —
  confusing for people and hard for the system to disambiguate intent.
- **iPadOS: consider a context menu for creating a new object** (Files creates a
  folder from a long press or secondary click).
- **Prefer a graphical preview clarifying the target of the commands** — Notes and
  Mail show a condensed version of the actual content so people confirm they're
  acting on the right item. **Ensure the preview animates well** — adjust the
  clipping path to match the shape as it emerges and the screen dims behind it.
- **Consider a context menu instead of a panel or inspector** for frequently used
  functionality — fewer separate windows keeps people's space uncluttered.
- **visionOS: avoid a context menu taller than the window** — system components sit
  above and below the window edges (window management controls, Share menu) and a
  tall menu can obscure them.

## Edit menus
- **Prefer the system-provided edit menu** — a custom menu with the same commands
  is redundant and confusing.
- **Let people reveal it with the system-defined interactions they know** — touch
  and hold on a touchscreen, **pinch and hold in visionOS**, secondary click with a
  trackpad.
- **Offer only contextually relevant commands** — remove or dim what doesn't apply
  (no Copy or Cut with nothing selected).
- **List custom commands near the relevant system-provided ones** to preserve
  expected ordering.
- **When it makes sense, let people select and copy noneditable text** — captions,
  status text — so they can paste it into a message, note, or search.
- **Support undo and redo.** An edit menu doesn't confirm before acting, so undo is
  the recovery path.
- **Avoid other controls that duplicate edit menu items.**
- **Differentiate types of deletion.** **Delete** behaves like the Delete key;
  **Cut** copies to the pasteboard *before* deleting.
- **Create short labels for custom commands** — verbs or short verb phrases.
- **Make sure your edit menu works in both styles** — the system shows the
  **compact horizontal** style for Multi-Touch reveals and the **vertical** style
  for keyboard or pointing device.
- **Adjust placement if necessary** — default is above or below the insertion
  point/selection, with a visual indicator pointing at the target.

## Pop-up buttons vs. pull-down buttons
**Pop-up button** — presents a **flat list of mutually exclusive options or
states** and reflects the current selection.
- **Provide a useful default selection.**
- **Let people predict the options without opening it** — an introductory label or
  a button label describing the effect.
- **Good when space is limited** and you don't need all options visible.
- **Consider a Custom option** for items useful only in some situations, to avoid
  cluttering the interface.
- **In a popover or modal, prefer a pop-up button over a disclosure indicator** for
  a list item's multiple options — people choose without navigating away.

**Pull-down button** — presents **commands or items directly related to the
button's action**; clarifies the target or customizes behavior without extra
buttons.
- **Never put all of a view's actions in one pull-down button** — primary actions
  must be discoverable, not hidden behind an interaction.
- **Balance menu length with ease of use** — **at least three items** makes the
  interaction feel worthwhile; for one or two, use separate buttons.
- **Display a menu title only if it adds meaning** — usually the button's content
  plus descriptive items is enough.
- **Mark destructive items (red) and ask people to confirm intent.**
- **Include an interface icon with an item when it adds value** (SF Symbols).
- **Consider a More pull-down button** for items that don't need prominent
  positions — but note it **hinders discoverability**.

## The menu bar (macOS, and iPadOS)
- **Support the default system-defined menus and their ordering.** People expect a
  familiar order, and the system implements many standard items for you.
- **Always show the same set of menu items.** Visible items teach people what your
  app supports. **Disable, don't remove**, an unavailable action.
- **Represent actions with familiar icons** — the same ones the system uses.
- **Support the standard keyboard shortcuts** for standard items (Copy, Cut,
  Paste, Save, Print), and define custom ones for custom commands.
- **Prefer short, one-word menu titles** — display sizes and menu bar extras affect
  spacing.
- **Display the About item first, followed by a separator** so it stands alone.
- **Decide whether Find items belong in the Edit menu** — if the app searches files
  or objects, File may be more appropriate.
- **Provide a View menu even for a subset of standard view functions** (e.g. an app
  with only full-screen support).
- **Each show/hide item's title must reflect the current state** — "Show Toolbar"
  when hidden, "Hide Toolbar" when visible.
- **Provide app-specific menus for custom commands** — the menu bar is where people
  look for app-specific commands, especially on first use, **even when the commands
  exist elsewhere.**
- **Reflect your app's hierarchy in app-specific menus** — Mail's Mailbox, Message,
  Format order mirrors mailboxes ⊃ messages ⊃ formatting.
- **List app-specific menus most-general to least** — people expect leading menus to
  be more specialized than trailing ones.
- **Provide a Window menu even with only one window** — include **Minimize and
  Zoom** so Full Keyboard Access users can invoke them.
- **Consider items for showing and hiding panels.**
- **Dynamic menu items** (revealed by a modifier key): **never the only way to
  accomplish a task**; **use primarily in menu bar menus** (they're even harder to
  find in contextual or Dock menus); **require only a single modifier key** —
  multiple keys are physically awkward while opening a menu and reduce
  discoverability.
- **The menu bar is often hidden in full screen — ensure every function is
  reachable through your UI**, especially anything assigned to a dynamic item.
- **iPadOS:** **reserve YourAppName > Settings for opening your app's page in
  iPadOS Settings**; link an internal preferences area with a *separate* item
  beneath it in the same group. **For tab-style navigation, consider adding each
  tab as a View menu item.** **Consider grouping items into submenus to conserve
  vertical space** — iPad menu rows are taller (tappable) and some iPads are small.
- **Menu bar extras:** **consider a symbol** (interface icon or SF Symbol; both use
  black and clear). **Display a menu — not a popover — on click**, unless the
  functionality is too complex for a menu. **Let people, not your app, decide
  whether it appears** (typically a setting in your settings window). **Never rely
  on its presence** — the system hides and shows extras regularly and you can't
  predict its location. **Expose the same functionality elsewhere too**, e.g. a
  Dock menu.

## Activity views (share sheets)
- **Use the Share button to display an activity view** — don't invent an
  alternative path to the same thing.
- **Never duplicate common actions already in the activity view** (a second Print
  action is confusing — people can't tell them apart).
- **Consider a symbol to represent your custom activity.**
- **Write a succinct, descriptive title for each custom action** — a single verb or
  brief verb phrase. **Long titles wrap and may truncate.**
- **Make sure activities are appropriate to the current context** — you can't
  reorder system tasks, but you **can exclude** inapplicable ones.
- **For a share extension, prefer the system-provided composition view.**
- **Streamline and limit interaction** — ideally a task completes in a few steps,
  even a single tap.
- **Avoid placing a modal view above your extension** (an alert may be necessary;
  additional modals are not).
- **Provide an image that communicates your extension's purpose if necessary.**
  A **share** extension **automatically uses your app icon**, which gives people
  confidence your app provided it. For an **action** extension, **prefer a symbol or
  an interface icon that clearly identifies the task.**
- **Use your main app to show progress of a lengthy operation.** The activity view
  **dismisses immediately** when the task completes, so continue time-consuming
  work in the background and report progress in the app.

## Home Screen quick actions (iOS/iPadOS)
- **Create quick actions for compelling, high-value tasks** — Maps offers search
  near current location and directions home. **People expect at least one from
  every app.**
- **Avoid unpredictable changes.** Dynamic quick actions keep things relevant
  (based on location or recent activity), but shouldn't shift unpredictably.
- **Provide a succinct title that instantly communicates the result** —
  "Directions Home", "Create New Contact", "New Message".
- **Provide a familiar interface icon** — prefer SF Symbols / standard icons.
- **Never use an emoji in place of a symbol** — emoji are full color, while quick
  action symbols are **monochromatic and change appearance in Dark Mode** to keep
  contrast.

## Dock menus (macOS)
- **Make custom Dock menu items available elsewhere too** — not everyone uses them.
- **Prefer high-value custom items** — currently/recently open windows make a Dock
  menu a convenient jump target.

## Ornaments (visionOS)
- **Use an ornament for frequently needed controls or information in a consistent
  location that doesn't clutter the window.** It stays close to its window so
  people always know where to find it.
- **In general, keep an ornament visible.** Hiding makes sense when people dive
  into content (watching a video, viewing a photo) — otherwise people appreciate
  consistent access.
- **With multiple ornaments, prioritize the window's overall visual balance** —
  they elevate important actions but can distract from content.
- **Keep an ornament's width the same as or narrower than its window** — a wider
  one can interfere with a tab bar or other vertical side content.
- **Consider borderless buttons in an ornament** — the ornament's background is
  already glass, so a button on it may not need a visible border.
- **Use system-provided toolbars and tab bars unless you need custom components** —
  in visionOS they **automatically appear as ornaments**, so don't rebuild them.
