# Foundations: writing, inclusion, motion, Dark Mode, RTL, privacy,
# branding, symbols, icons, images

## Writing
"The words you choose within your app are an essential part of its user
experience." Design **through the lens of language**.

- **Determine your app's voice.** Who are you talking to? What vocabulary is
  familiar? How do you want people to feel? (A banking app conveys trust and
  stability; a game conveys excitement and fun.) **Create a list of common terms
  and reference it** to keep language consistent.
- **Match your tone to the context.** Voice is constant; **tone varies with the
  situation** — what are people doing, physically and in the app? Straightforward
  and direct for a serious situation; light and congratulatory for an achievement.
- **Be clear.** Check each word to be sure it needs to be there. **If you can use
  fewer words, do so.** *When in doubt, read your writing out loud.*
- **Write for everyone** — simple, plain language, written with accessibility and
  localization in mind, **avoiding jargon and gendered terminology.**
- **Consider each screen's purpose.** Most important information first. **If you're
  conveying more than one idea, consider multiple screens** and think about the
  flow between them.
- **Be action oriented.** Active voice and clear labels. **Label buttons and links
  with a verb.** *"Send" beats "Let's do it!"* — prioritize clarity over cute or
  clever. **Never "Click here"** — use descriptive phrases ("Learn more about UX
  Writing"), **especially important for screen reader users.**
- **Build language patterns.** Consistency builds familiarity and makes writing
  easier.
- **Adopt capitalization rules aligned with your style, applied consistently.**
  **Title case reads formal; sentence case reads casual.** Choose per UI element
  type and stick to it.
- **Give clear guidance across multi-step processes.** "Get Started" to begin;
  "Continue"/"Next" (or a hint at the next step) to advance; **"Done" to make
  completion clear.** Be consistent with whichever you choose.
- **Use possessive pronouns sparingly.** *"Favorites" conveys the same as "Your
  Favorites" and is more succinct.* Use them consistently if at all, and don't
  switch perspectives. **Avoid *we* altogether** — it's unclear who "we" is,
  especially in errors. *"Unable to load content" is much clearer than "We're
  having trouble loading this content."*
- **Write for how people use each device.** Same language across devices, adjusted
  where helpful. **Describe gestures correctly** — never "click" on iPhone or iPad
  where you mean "tap". iPhone and Apple Watch allow personalization but **small
  screens require brevity**; TVs are in shared spaces (**consider who you're
  addressing**) and **big screens also require brevity** because text must be large
  enough to read from a distance.
- **Provide clear next steps on any blank screens.** An empty state is a chance to
  welcome and educate. **Guide people to actions, with a button or link if
  possible.** Remember empty states are usually temporary — **don't put crucial
  information there that will disappear.**
- **Write clear error messages.** Best is to **help people avoid errors**. When
  needed: **display it as close to the problem as possible, avoid blame, and be
  clear about the fix.** *"Choose a password with at least 8 characters" beats
  "That password is too short."* **Skip interjections like "oops!" or "uh-oh"** —
  unnecessary and insincere. *If language alone can't address an error affecting
  many people, rethink the interaction.*
- **Choose the right delivery method** based on urgency, importance, context, and
  how much supporting information people need.
- **Keep settings labels clear and simple.** Add an explanation if the label isn't
  enough. **Describe what it does when turned ON — people infer the opposite.**
  To direct someone to a setting, **provide a direct link or button rather than
  describing its location.**
- **Show hints in text fields.** Label all fields clearly; **use hint/placeholder
  text so people know the format** ("name@example.com" or "Your name"). **Show
  errors right next to the field and instruct rather than scold** — *"Use only
  letters for your name" beats "Don't use numbers or symbols"*, and both beat
  robotic messages like "Invalid name."

## Inclusion
"Put people first by prioritizing respectful communication and presenting content
and functionality in ways that everyone can access and understand."

Perspectives arise from shared human characteristics: **age; gender and gender
identity; race and ethnicity; sexuality; physical attributes; cognitive
attributes; permanent, temporary, and situational disabilities; language and
culture; religion; education; political or philosophical opinions; social and
economic context.**

> **Don't frame the work as merely a search for content that might give offense.**
> "An inoffensive app or game isn't necessarily an inclusive one." Focusing on
> inclusion avoids offense *and* creates a welcoming experience.

- **Consider the tone of your copy from different perspectives.** *An academic tone
  can make an app seem like it welcomes only high levels of education.* Be clear,
  direct, respectful.
- **Pay attention to how you refer to people.** Use **you** and **your** — referring
  to people as *the user* or *the player* feels distant and unwelcoming. **Reserve
  *we* and *our* for your software or company**; otherwise they imply a personal
  relationship that can read as insulting or condescending.
- **Avoid specialized or technical terms without defining them.** Even when people
  know a term, **plain language is easier to read and to translate.**
- **Replace colloquial expressions with plain language.** They're culture-specific
  and hard to translate — and **some have exclusionary origins** (*peanut gallery*,
  *grandfathered in* both arose from oppressive contexts).
- **Consider carefully before including humor.** Highly subjective and hard to
  translate. It risks **confusing people who don't get it, irritating people who
  encounter it repeatedly, and insulting people** it lands badly on.
- **Avoid images and language that exclude people with disabilities.** Include
  people with disabilities when representing a variety of people, and **avoid
  language that uses a disability to express a negative quality.**
- **Take a people-first approach when writing about people with disabilities** —
  describe accomplishments and goals before mentioning a disability. **If writing
  about a specific person or community, find out how they self-identify.**
- **Prioritize simplicity and perceivability** — familiar, consistent interactions,
  and content everyone can perceive by sight, hearing, or touch.

## Motion
- **Add motion purposefully, supporting the experience without overshadowing it.**
  **Don't add motion for the sake of motion** — gratuitous animation distracts and
  can make people feel **disconnected or physically uncomfortable.**
- **Make motion optional.** Never the only way to communicate important
  information; **supplement visual feedback with other cues.**
- **Strive for realistic feedback motion that follows people's gestures and
  expectations.** Motion that doesn't make sense **disorients**.
- **Aim for brevity and precision in feedback animations** — brief and precise feels
  lightweight and often conveys information better than prominent animation.
- **In apps, generally avoid adding motion to frequent UI interactions.** The system
  already provides subtle animations for standard elements; don't make people spend
  extra time on a custom one.
- **Let people cancel motion.** Don't make people wait for an animation to finish
  before acting — **especially if they'd experience it more than once.**
- **Consider animated symbols** (SF Symbols 5+).
- **Games: maintain a consistent frame rate of 30–60 fps** for a smooth experience,
  by default on each platform you support.
- **Let people customize the visual experience to optimize performance or battery
  life** — e.g. switching power modes when external power is detected.
- **visionOS motion comfort:**
  - **Avoid motion at the edges of the field of view.** Peripheral motion is
    distracting **and can cause discomfort.**
  - **Help people stay comfortable when moving large virtual objects.** An object
    filling much of the field of view and occluding passthrough is **perceived as
    part of the surroundings**, so its motion reads as self-motion.
  - **Consider using fades to relocate an object** — fade it out, move it, fade it
    in, rather than making people track meaningless movement.
  - **In general, avoid letting people rotate a virtual world.** Rotation upsets
    people's sense of stability **even when they control it and it's subtle.**
    Prefer instantaneous direct repositioning.
  - **Consider giving people a stationary frame of reference** — movement contained
    within a non-moving area is easier to handle.
  - **Avoid sustained oscillation — especially around 0.2 Hz**, a frequency people
    are very sensitive to.

## Dark Mode
- **Avoid an app-specific appearance setting.** It creates extra work (two settings
  to change) and **people may think your app is broken** when it doesn't follow the
  system.
- **Ensure your app looks good in both appearance modes** — people can also choose
  **Auto**, which switches as conditions change through the day.
- **Test in both modes with Increase Contrast and Reduce Transparency on** —
  separately and together.
- **In rare cases, consider a permanently dark appearance** — e.g. immersive media
  viewing, where the UI recedes and people focus on the media.
- **Embrace colors that adapt** — semantic colors (`labelColor`, `controlColor`,
  `separator`) adapt automatically. **Custom colors → add a Color Set asset.**
- **Aim for sufficient contrast in all appearances — at minimum 4.5:1.**
- **Soften the color of white backgrounds.** Slightly darken a content image with a
  white background so it doesn't **glow** in the surrounding Dark Mode context.
- **Use SF Symbols wherever possible** — they work in both modes with dynamic color
  tinting or vibrancy.
- **Design separate interface icons for light and dark if necessary** — a full moon
  icon may need a subtle dark outline on light, and none on dark.
- **Make sure full-color images and icons look good in both.** Use one asset if it
  works in both; otherwise modify it or create separate light and dark assets.
- **Use the system-provided label colors** — primary, secondary, tertiary,
  quaternary all adapt.
- **Use system views to draw text fields and text views** — they adjust
  automatically for the presence or absence of vibrancy.
- **Prefer the system background colors.** Dark Mode is **dynamic**: the background
  automatically changes from **base to elevated** when an interface comes forward
  (a popover or modal sheet).
- **Include some transparency in custom component backgrounds when appropriate** —
  lets components pick up color from the window background when **desktop tinting**
  is active.

## Right to left
- **Adjust text alignment to match the interface direction** if the system doesn't
  do it automatically.
- **Align a paragraph based on its language, not the current context.** A
  *paragraph* = **three or more lines**; misaligned paragraphs are hard to read.
- **Use consistent alignment for all items in a list** — reverse them all, including
  items in a different script.
- **Never reverse the order of numerals within a number.** "541", a phone number, a
  credit card number — **digits always appear in the same order.**
- **Reverse the order of numerals that show progress or a counting direction — never
  flip the numerals themselves.**
- **Flip controls that show progress from one value to another** — sliders, progress
  indicators — because **people view forward progress as moving in the reading
  direction.**
- **Flip controls that navigate or access items in a fixed order** — in RTL, **a
  back button must point right** so screen flow matches reading order.
- **Preserve the direction of a control that refers to an actual direction or points
  at an onscreen area** — a control meaning "to the right" always points right.
- **Visually balance adjacent Latin and RTL scripts.** Arabic and Hebrew have **no
  uppercase letters**, so they can look too small beside uppercased Latin text.
- **Avoid flipping photographs, illustrations, and general artwork** — flipping
  changes meaning, and **flipping a copyrighted image could be a violation.**
- **Reverse the positions of images when their order is meaningful** —
  chronological, alphabetical, favorite.
- **Flip interface icons that represent text or reading direction** — left-aligned
  bars become right-aligned.
- **Consider a localized version of an interface icon that displays text** — e.g.
  font-size choice, a signature.
- **Flip an interface icon showing forward or backward motion** — direction of
  reading = forward.
- **Never flip logos or universal signs and marks.** Flipped logos confuse people
  and **can have legal repercussions**; universal symbols like the checkmark are
  expected as-is.
- **In general, avoid flipping interface icons depicting real-world objects** —
  *clocks work the same everywhere*, so a traditional clock icon shouldn't flip
  unless you're using it to indicate directionality.
- **Before flipping a complex custom icon, consider its individual components and
  overall visual balance** — a badge, slash, or magnifying glass may need to follow
  the visual design language regardless of locale.

## Privacy
- **Request access only to data you actually need.** Asking for more than a feature
  needs — or asking **before a person shows interest in the feature** — undermines
  trust.
- **Be transparent about how you collect and use data.** **Always respect people's
  choices to use system privacy features** (like Hide My Email).
- **Process data on the device where possible** — the Apple Neural Engine, custom
  CreateML models — avoiding "lengthy and potentially risky round trips."
- **Adopt system-defined privacy protections and follow security best practices.**
- **Request permission only when your app clearly needs the data or resource.**
  People are naturally suspicious of a request with **no obvious need**.
- **Avoid requesting permission at launch unless the data is required for the app to
  function.** People accept a launch-time request when the reason is obvious (a
  navigation app needing location).
- **Write copy that clearly describes how you use the ability, data, or resource** —
  the *purpose string* / *usage description string*, displayed after your app name
  and before the buttons.
- **If you precede the system alert with a custom screen: include only ONE button,
  and make it clear that it opens the system alert.** People feel manipulated
  otherwise.
- **Don't include additional actions in that custom screen** — no way to leave
  without viewing the system alert, no close or cancel option.
- **Never precede the system alert with a screen that could confuse or mislead.**
  People tap quickly to dismiss alerts; **a custom screen exploiting that behavior
  is not acceptable.**
- **Consider the location button** for a lightweight way to share location for a
  specific feature (attaching location to a post, finding a store, identifying a
  building or plant). **You may customize it to harmonize with your UI.**
- **Avoid relying solely on passwords — prefer passkeys.** If you keep passwords,
  **require two-factor authentication.**
- **Store sensitive information in a keychain.** **Never store passwords or secure
  content in plain-text files** — file permissions are not enough.
- **Avoid inventing custom authentication schemes** — prefer passkeys, Sign in with
  Apple, Password AutoFill.
- **macOS: sign your app with a valid Developer ID** when distributing outside the
  store. **Protect data with app sandboxing** (required for the Mac App Store).
  **Avoid assumptions about who is signed in** — fast user switching means multiple
  people may be active.

## Branding
- **Use your brand's unique voice and tone in all written communication.**
- **Apply your accent color judiciously.** Too broad a use **overwhelms the
  interface and dilutes its impact.** **Minimize it on controls**; use it
  intentionally for **primary actions or status indicators** like unread badges.
- **Consider a custom font** if your brand is strongly associated with one — but it
  **must be legible at all sizes and support Bold Text and Dynamic Type.** A common
  pattern: custom font for headlines and subheadings, system font for body.
- **Express your brand with familiar components.** Familiar components feel reliable
  and let people focus on what makes your app distinct.
- **Ensure branding always defers to content.** Screen space spent on a pure brand
  asset is space not spent on what people came for.
- **Help people feel comfortable by using standard patterns consistently.** Even a
  highly stylized interface is approachable with familiar behaviors — UI in expected
  locations, standard symbols for common actions.
- **Resist displaying your logo throughout the app** unless essential for context.
  *"People seldom need to be reminded which app they're using."*
- **Never use a launch screen as a branding opportunity.**
- **Follow Apple's trademark guidelines** — Apple trademarks must not appear in your
  app name or images.

## SF Symbols
**Rendering modes:**
- **Monochrome** — one color to all layers; paths render in your color or as a
  transparent shape within a color-filled path.
- **Hierarchical** — one color, **varying opacity by each layer's hierarchical
  level**.
- **Palette** — two or more colors, **one per layer**. Specifying only two colors for
  a three-level symbol means **secondary and tertiary share a color.**
- **Multicolor** — intrinsic colors that **enhance meaning**: `leaf` is green,
  `trash.slash` is red to signal data loss.

- **Confirm a symbol's rendering mode works in every context** — size and background
  contrast affect discernibility.
- **Use variable color to communicate CHANGE — not depth.** For depth and visual
  hierarchy use **Hierarchical**.

**Animations:** *Appear / Disappear* (gradually emerge or recede) · *Bounce* (brief
elastic scale, returns to initial state; plays once; signals an action occurred or
is needed) · *Scale* (**persists** until you set a new scale or remove it — unlike
bounce) · *Pulse* (varies opacity; **only annotated layers pulse** by default) ·
*Variable color* (incremental opacity by layer; **cumulative** = changes persist
through the cycle, **iterative** = they don't) · *Replace* (swaps arbitrary symbols
across all weights and rendering modes) · *Magic Replace* (smart transition between
**related** shapes — slashes draw on/off, badges appear/disappear) · *Wiggle*
(directional; highlights a change or an overlooked call to action) · *Breathe*
(living quality; conveys status changes or ongoing activity like a recording) ·
*Rotate* (visual indicator or real-world imitation; confirms a task is in progress)
· *Draw On / Draw Off* (SF Symbols 7+; draws along a path through guide points,
all layers at once or staggered).

- **Apply symbol animations judiciously** — no technical limit, but too many
  **overwhelm an interface and distract.**
- **Make sure animations serve a clear purpose in communicating intent** — each has
  a discrete movement communicating a certain action or eliciting a certain
  response.
- **Use them to communicate information more efficiently** — visual feedback
  reinforcing that something happened.
- **Consider your app's tone when adding animations.**

**Custom symbols:**
- **Use the template as a guide** — consistent with system symbols in level of
  detail, optical weight, alignment, position, and perspective.
- **Assign negative side margins if necessary** for optical horizontal alignment
  when a badge or other element widens the symbol.
- **Optimize layers for animation** — annotate them in the SF Symbols app;
  **Z-order determines the order colors apply** for variable color.
- **Test animations for custom symbols with all the presets** — shapes and paths may
  not behave as expected in motion.
- **Avoid custom symbols that include common variants** (enclosures, badges) — use
  the **component library** to generate those instead.
- **Provide alternative text labels** so VoiceOver can describe them.
- **Never design replicas of Apple products**, and **you can't customize a symbol
  that SF Symbols identifies as representing an Apple feature or product.**

## Icons (interface icons)
- **Create a recognizable, highly simplified design.** Too many details make an icon
  confusing or unreadable; **prefer familiar, universal shapes.**
- **Maintain visual consistency across all interface icons** — consistent size, level
  of detail, stroke thickness, and perspective, whether custom, system, or mixed.
- **In general, match the weights of icons and adjacent text** — unless you're
  deliberately emphasizing one.
- **Add padding for optical alignment if necessary** — asymmetric icons look
  unbalanced when centered **geometrically instead of optically.**
- **Provide a selected-state version only if necessary** — standard components
  (toolbars, tab bars, buttons) handle selected/unselected appearances for you.
- **Use inclusive images** — prefer **gender-neutral human figures**; avoid images
  hard to recognize across cultures or languages.
- **Include text only when essential to conveying meaning.**
- **Use a vector format (PDF or SVG) for custom icons** — the system scales them
  automatically for high-resolution displays.
- **Provide alternative text labels** for VoiceOver.
- **Avoid replicas of Apple hardware** — designs change frequently and date your
  content. If you must, use only images from Apple Design Resources.

**Document icons (macOS):**
- **Design simple images that clearly communicate the document type** — uncomplicated
  shapes, a reduced palette of distinct colors. **Can display as small as 16×16 pt.**
- **A single expressive background-fill image can work alone** (Xcode, TextEdit use
  rich background images with **no center image**).
- **Consider reducing complexity in small versions** — fine detail blurs.
- **Avoid important content in the top-right corner** — the system masks the image to
  the document shape and **draws the white folded corner on top.**
- **A center image measures half the canvas** — simple, unambiguous, recognizable at
  every size.
- **Define a ~10% margin and keep most of the image inside it** — the image should
  occupy **about 80% of the canvas**, though parts may extend into the margin for
  optical alignment.
- **Specify a succinct term if the extension is unfamiliar** — the system shows the
  extension at the bottom edge by default.

## Images
- **Provide high-resolution assets for all bitmap images, for every device** —
  append **@1x, @2x, @3x** in the asset catalog.
- **In general, design at the lowest resolution and scale up.** With resizable
  vectorized shapes, **position control points at whole values** so they align
  cleanly at 1x.
- **Include a color profile with each image.**
- **Always test images on a range of actual devices** — an image that looks great at
  design time can appear pixelated, stretched, or compressed.
- **tvOS layered images (parallax):**
  - **Use standard interface elements** — standard views plus focus APIs get parallax
    automatically.
  - **Identify logical foreground, middle, and background elements.** Foreground =
    prominent elements (a game character, text on an album cover). Middle =
    secondary content and effects.
  - **Generally keep text in the foreground** for clarity.
  - **Keep the background layer opaque** — **you'll get an error if it isn't.**
  - **Keep layering simple and subtle.** *Parallax is designed to be almost
    unnoticeable* — excessive 3D looks unrealistic and jarring.
  - **Leave a safe zone around foreground layers** — content gets cropped as the
    image scales and moves on focus.
  - **Always preview layered images** (Xcode, Parallax Previewer, or the Parallax
    Exporter Photoshop plug-in).
- **visionOS:**
  - **Create a layered app icon** — two to three layers moving at subtly different
    rates in focus.
  - **Prefer vector-based art for 2D images** — bitmap content may not look good when
    scaled up.
  - **If you use rasterized images, balance quality with performance.** A @2x image
    is fine at common viewing distances, but its **fixed resolution means the system
    doesn't scale it dynamically.**
  - **Use stereo HEIC for spatial photos** — with spatial metadata, visionOS
    recognizes it as spatial.
  - **Prefer the feathered glass background effect for text over spatial photos.**
  - **Take visual comfort into account when making spatial photos from 2D content** —
    disparity metadata affects how people view it.
  - **Display spatial photos and scenes in standalone views** — inline with other
    content **causes visual discomfort**. Use a sheet or separate view.
  - **Use spatial scenes for specific moments** — generation takes **up to several
    seconds** from an existing image, so design around that (Photos offers an
    explicit action).
  - **When displaying immersively, prefer minimal UI** — the Spatial Gallery shows a
    single piece of content, a small caption, and one Back button, navigating by
    swipe.
  - **Prefer larger spatial scenes centered in the field of view** — people move
    their head laterally to see parallax, and **smaller scenes give less of it.**
- **watchOS:**
  - **In general, avoid transparency to keep image files small** — composite the
    background into the image when it's always the same solid color. **Transparency
    is necessary in complication images.**
  - **Use autoscaling PDFs** to provide a single asset for all screen sizes — design
    for **40mm and 42mm at 2x**, and WatchKit scales by device.
