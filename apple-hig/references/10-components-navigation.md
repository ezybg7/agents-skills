# Components: navigation & structure (HIG "Navigation and search",
# "Layout and organization")

## Tab bars
"Lets people navigate between **top-level sections** of your app."
- **Use a tab bar for navigation, not actions.** Controls that act on the current
  view belong in a **toolbar**.
- **Keep the tab bar visible as people navigate sections.** Hiding it makes people
  forget where they are. **Exception:** a modal view may cover it (temporary and
  self-contained).
- **Use the appropriate number of tabs.** Weigh the complexity of more tabs against
  how often people need each section.
- **Avoid overflow tabs.** When horizontal space limits visible tabs, the trailing
  tab becomes a **More** tab in iOS/iPadOS, hiding the rest in a separate list.
- **Never disable or hide tab bar buttons, even when content is unavailable.**
  It makes the interface look unstable and unpredictable. **If a section is empty,
  explain why.**
- **Include tab labels** — beneath or beside the icon, **single words whenever
  possible**.
- **Consider SF Symbols for tab icons** — they adapt to regular vs. compact tab
  bars automatically.
- **Use a badge (red oval, white text, number or "!") for critical information**
  only — new or updated content that warrants attention.
- **Avoid similar colors on tab labels and content-layer backgrounds** — prefer
  monochromatic, or an accent with clear differentiation.
- **Prefer a tab bar over a sidebar for navigation.** For complex apps, offer the
  option to **convert the tab bar to a sidebar** for a wider set of options.
- **Let people customize the tab bar** in apps with many sections (Music).
- **Be aware of scrolling behavior:** by default the tab bar can scroll offscreen
  when the current tab holds a single main view.
- **visionOS:** supply **a symbol and a text label** per tab — the symbol is always
  visible and **looking at the tab bar reveals labels**. Keep labels short.
- **Consider a sidebar within a tab for deep hierarchies** — but **prevent sidebar
  selections from changing which tab is open.**
- **tvOS live-viewing apps: organize tabs in a consistent order.**

## Sidebars
Appears on the **leading** side; navigates between app areas or top-level content
collections (folders, playlists).
- **Consider using a tab bar first** — more space for content, flexible enough for
  most apps' main areas; the tab bar's convertible sidebar appearance covers the
  case of more areas than fit.
- **Extend visually rich content beneath the sidebar.** Sidebars float above
  content in the Liquid Glass layer — reinforce separation by letting content
  extend under it.
- **Let people customize sidebar contents** where possible.
- **Group hierarchy with disclosure controls** if you have a lot of content, to
  keep vertical space manageable.
- **Consider familiar symbols** for items — prefer a **custom SF Symbol over a
  bitmap image** if you need something custom.
- **Consider letting people hide the sidebar** — for more content room or less
  distraction — using platform-standard interactions.
- **Consider auto-hiding/revealing the sidebar as the window resizes** (Mail
  collapses its sidebar as the viewer window shrinks).
- **Show no more than two levels of hierarchy.** Deeper → use a **split view with a
  content list between the sidebar and the detail view.**
- **With two levels, title each group with succinct, descriptive labels.**
- **Make sure sidebar icon colors serve a clear purpose.** They default to the app
  accent color; **in macOS people can change the system accent and expect all
  sidebar icons to follow** — so only fix a color when it carries meaning.
- **Avoid critical information or actions at the bottom of a sidebar** — people
  often position windows so the bottom edge is hidden.

## Search fields
- **Use placeholder text to convey what people can search for** — reinforces scope
  and teaches what search covers.
- **If possible, start search immediately as people type** — continuously refined
  results feel more responsive.
- **Consider showing suggested search terms** — recent searches before typing,
  predictive suggestions during.
- **Simplify search results.** Most relevant first; **consider categorizing them**.
- **Consider letting people filter results** — e.g. a scope bar in the results area.
- **Use a scope bar to filter among clearly defined categories** — moving from a
  broader scope to a narrower one (Mail: whole mailbox → current mailbox).
- **Default to a broader scope and let people refine.** The broad scope provides
  context for the full result set.
- **Use tokens to filter by common search terms or items** — a token gets a visual
  treatment marking it selectable and editable as a single unit.
- **Consider pairing tokens with search suggestions** — people don't know which
  tokens exist otherwise.

### Search placement (decision guide)
| Placement | When |
|---|---|
| **Bottom** (own toolbar or added to an existing one) | Search is a priority — keeps it easy to reach |
| **Top** | You must defer to content at the bottom, or there's no bottom toolbar (Wallet keeps event passes reachable) |
| **Inline, next to content** | Filtering or searching within a single view — proximity shows the search applies to *this* content |
| **Trailing side of the toolbar** | Common pattern for split views searching across multiple columns (Mail, Notes, Voice Memos) |
| **Top of the sidebar** | Filtering sidebar content or navigation (Settings — exposes sections several levels deep) |
| **Item in the sidebar or tab bar** | You want a dedicated discovery area with rich suggestions, categories, or content needing space |

- **An inline field at the top goes above the list it searches**; consider
  **pinning it to the top toolbar when scrolling** to distinguish it from search
  elsewhere.
- **Search tab styles:** the **standard** style creates a dedicated landing page —
  suggestions, discovery, exploration. The **button** appearance immediately raises
  the keyboard with the field above it — a transient, get-in-get-out experience.
- **In a dedicated search area, consider focusing the field immediately** on
  navigation. **Exception: on iPad with only a virtual keyboard**, leave it
  unfocused.
- **Account for window resizing.** On iPad the field resizes fluidly like on Mac;
  **in compact views, make sure search stays where it's most contextually useful.**
- **tvOS: provide suggestions** — people don't want to type. Popular,
  context-specific, and recent searches.

## Split views
Manages multiple **adjacent panes**, each of which may hold tables, collections,
images, or custom views.
- **Persistently highlight the current selection in each pane that leads to the
  detail view** — clarifies the relationship between panes.
- **Prefer a split view in a regular — not compact — environment.** It needs
  horizontal space; iPhone portrait doesn't have it.
- **Account for narrow, compact, and intermediate window widths** — iPad windows
  resize fluidly.
- **Set reasonable minimum and maximum pane sizes** so the **divider stays
  visible** — too small and the divider can become unusable.
- **Consider letting people hide a pane** — e.g. hiding other panes around an
  editing area for focus and room.
- **Provide multiple ways to reveal hidden panes** — a toolbar button, a menu
  command, a keyboard shortcut.
- **Prefer the thin divider style** (**1 pt**) — maximum content space, still easy
  to grab. Thicker styles need a specific reason.
- **Choose a layout that keeps panes balanced.** Default: **one-third primary,
  two-thirds secondary.**
- **Display a single title above the split view**, describing the content as a
  whole — people already know how to navigate a split view.
- **Choose title alignment by secondary-pane content:** a **content collection** →
  consider **centering** the title; otherwise align to the content.
- **Prefer a split view over a new window for supplementary information** — keeps
  people in context.
- **Consider letting people drag and drop between panes.**
- **Automatically display the most relevant detail view on launch** — relevant to
  location, time, or recent activity.
- **watchOS: place multiple detail pages in a vertical tab view** so people scroll
  between them with the Digital Crown (with a page indicator).

## Lists and tables
- **Prefer displaying text in a list or table** — the row format makes text easy to
  scan and read.
- **Let people edit a table when it makes sense** — people appreciate reordering
  even when they can't add or remove. iOS/iPadOS require an **edit mode** first.
- **Provide appropriate feedback on selection**, varying by whether selection
  reveals a new view or toggles state.
- **Keep item text succinct** to minimize truncation and wrapping.
- **Preserve readability of text that might be clipped or truncated**, especially
  when people can vary the table's width.
- **Use descriptive column headings in multicolumn tables** — nouns or short noun
  phrases, **title-style capitalization, no ending punctuation.**
- **Choose a table/list style that coordinates with your data and platform.**
- **Choose a row style that fits the information.**
- **Use an info button only to reveal more information about a row's content** —
  it does **not** support hierarchical navigation.
- **Avoid an index on a table with trailing-edge controls** (like disclosure
  indicators) — they collide.
- **macOS: let people click a column heading to sort**; clicking an already-sorted
  column **re-sorts in the opposite direction**. **Let people resize columns.**
  **Consider alternating row colors** in multicolumn tables to track values across
  a wide row.
- **Use an outline view, not a table, for hierarchical data.**
- **tvOS: confirm images near a table still look good as rows highlight, grow
  slightly, and round their corners on focus.**
- **watchOS: limit the number of rows where possible**; **constrain detail view
  length if you support vertical page-based navigation.**

## Collections
Manages an **ordered set of content** in a customizable, highly visual layout.
- **Use the standard row or grid layout whenever possible.** Avoid custom layouts
  without reason.
- **Consider a table instead of a collection for text** — simpler and more
  efficient to digest in a scrollable list.
- **Make it easy to choose an item** — adequate padding around images.
- **Add custom interactions only when necessary.** Defaults: tap to select, touch
  and hold to edit, swipe to scroll.
- **Consider animations for insert, delete, reorder** — standard animations exist.
- **Use caution with dynamic layout changes.** Changes must make sense and be easy
  to track — **avoid changing the layout while people are viewing or interacting.**

## Disclosure controls
- **Use a disclosure control to hide details until they're relevant.** Put the
  controls people are most likely to use **at the top of the hierarchy, always
  visible**, with advanced functionality disclosed.
- **Provide a descriptive label with a disclosure triangle** — indicate what is
  disclosed or hidden ("Advanced Options").
- **Place a disclosure button near the content it shows and hides.**
- **Use no more than one disclosure button in a single view.**

## Labels
Static text people can read and often copy, but not edit.
- **Use a label for a small amount of non-editable text.** Editable small text →
  text field. Large amounts of text → text view.
- **Prefer system fonts** — labels support Dynamic Type by default. Custom styling
  must stay legible.
- **Use system-provided label colors to communicate relative importance** — four
  levels.
- **Make useful label text selectable** — error messages, locations, IP addresses.

## Boxes
A visually distinct group of logically related information and components.
- **Keep a box relatively small compared to its containing view.** As it approaches
  the window/screen size it stops communicating separation.
- **Use padding and alignment for subgroups inside a box — not nested boxes.**
  Nested borders make an interface busy and cluttered.
- **Provide a succinct introductory title if it clarifies the contents.**
- **Title style: a brief phrase, sentence-style capitalization, no ending
  punctuation** — **except in a settings pane, where you append a colon.**

## Lockups (tvOS)
- **Allow adequate space between lockups** — a focused lockup expands and must not
  overlap or displace others.
- **Use consistent lockup sizes within a row or group** — matching widths and
  heights look better.
- **Prefer images over initials** — an image of a person creates a more intimate
  connection than text.

## Tab views (macOS)
Multiple **mutually exclusive** panes in the same area, switched by a tabbed
control.
- **Use for closely related areas of content** — the enclosure implies similarity.
- **Controls in a pane must affect only that pane** — panes are fully
  self-contained.
- **Label each tab to describe its pane's contents** — nouns or short noun phrases.
- **Avoid a pop-up button to switch tabs** — a tabbed control takes **one** click
  vs. two, and shows all options at once.
- **Avoid more than six tabs** — overwhelming and causes layout issues.
- **Inset a tab view with a margin of window body on all sides** — leaves room for
  controls not related to the tab contents.

## Column views / browsers (macOS)
- **Show the root level in the first column** so people can scroll back and restart
  navigation from the top.
- **Consider showing information about the selected item when there are no nested
  items** (Finder shows a preview plus creation/modification dates).
- **Let people resize columns** — especially when data names exceed the default
  width.

## Outline views (macOS)
- **Use a table instead for non-hierarchical data.**
- **Expose hierarchy in the first column only** — other columns hold attributes of
  the hierarchical data.
- **Use descriptive column headings** — nouns/short noun phrases, title-style
  capitalization, no punctuation, **specifically no trailing colon**. Always
  provide headings.
- **Consider click-to-sort column headings** (ascending/descending).
- **Let people resize columns.**
- **Make expanding/collapsing nested containers easy** — clicking a disclosure
  triangle expands that folder; **Option-clicking expands all nested levels.**
- **Retain people's expansion choices** across sessions so they don't re-navigate.
- **Consider alternating row colors in multicolumn outline views.**
- **Let people edit data where it makes sense** — a **single click** starts editing
  a cell (a double click may do something different).
- **Consider a centered ellipsis to truncate cell text** — preserving the beginning
  *and* end makes content more recognizable than clipping.
- **Consider a search field for lengthy outline views**, typically in the toolbar.

## Path controls (macOS)
Shows the file system path of a selected file or folder.
- **Standard** style: linear list of root disk, parent folders, selected item, each
  with icon and name; **hides intermediate names when too long to fit**.
- **Pop up** style: shows only the selected item's icon and name; clicking opens a
  menu with root disk, parent folders, and the item.
- **Use a path control in the window body, not the window frame** — never a toolbar
  or status bar. (Finder's appears at the **bottom of the window body**.)

## Token fields (macOS)
A text field that converts text into **tokens** — selectable, manipulable units.
- **Add value with a context menu** for additional options or token information.
- **Consider additional ways to convert text into tokens.** By default a **comma**
  creates a token; you can add shortcuts like **Return**.
- **Consider customizing the delay before showing suggested tokens.** Suggestions
  appear immediately by default, which **may distract people while typing.**
