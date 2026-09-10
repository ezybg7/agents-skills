# Technologies (HIG)

## Generative AI — responsible design
- **Design your experience responsibly.** Consider **direct and indirect impacts on
  people, systems, and society.**
- **Keep people in control.** AI can create and manipulate content, but **people
  remain in charge of decision making and the overall experience.**
- **Ensure an inclusive experience for all.** Models learn from data and **favor the
  most common information**, leading to **harmful, unintended biases and
  stereotypes.**
- **Design engaging and useful generative features.** *Generative AI is not the
  right solution for every situation.* Offer it **where it provides clear, specific
  value.**
- **Ensure a great experience even when generative features aren't available or
  people opt not to use them.**
- **Communicate where your app uses AI.** **Never trick someone into thinking
  they're interacting with a person** or that AI-generated content is human-made.
- **Set clear expectations about what the feature can and can't do** — helps people
  build a correct mental model.
- **Choose a model type that fits the feature and protects privacy.** **On-device
  models keep information on the device, respond quickly, and work offline.**
- **Ask permission before using personal information and usage data.**
- **Clearly disclose how your app and its model use and store personal
  information.**
- **Thoughtfully evaluate model capabilities** — some models carry general
  knowledge, others are task-trained.
- **Be intentional when choosing or creating a dataset** — it greatly shapes the
  model's behavior.
- **Guide people on how to use your generative feature** — e.g. **diverse,
  predefined example inputs** that hint at what's possible.
- **Raise awareness about and minimize hallucinations.** When unsure, a model may
  produce **plausible but made-up** content that misinforms.
- **Consider consequences and get permission before irreversible or potentially
  problematic tasks.**
- **Make it easy to refine or revert generated results, and acknowledge when
  corrections take effect** — surface **Edit, Undo, Retry, Adjust** near generated
  content.
- **Help people improve requests when results are blocked or undesirable** — coach
  rather than just refusing.
- **Reduce unexpected and harmful outcomes with thoughtful design and thorough
  testing** — harm arises from accidental *and* purposeful misuse.
- **Strive to avoid replicating copyrighted content.**
- **Factor processing time into your design.** *Latency* is time-to-output;
  generative models are typically much slower than non-generative ones (ARKit body
  tracking, Vision).
- **Give specific, reassuring feedback during generation.** *Instead of
  "Processing…", say "Finding substitutions for…"*
- **Consider offering alternate versions of results** so people can choose.
- **Consider ways to improve your model over time.**
- **Let people share feedback on outputs.**
- **Design flexible, adaptable features** — models and their resource needs evolve
  constantly.

## Machine learning
**Explicit feedback:**
- **Request explicit feedback only when necessary** — prefer **implicit** feedback.
- **Always make explicit feedback voluntary.**
- **Use simple, direct language for each option and its consequences.** **Avoid
  imprecise terms like *dislike*** — they don't convey consequences and are hard to
  translate.
- **Add icons to an option description if it helps** — **never an icon alone.**
- **Consider offering multiple options** for a sense of control.
- **Act immediately on explicit feedback and persist the change** — hide unwanted
  content **everywhere in the app**, not just where it was flagged.
- **Consider using explicit feedback to refine *when and where* you show results** —
  people may like a result but not at certain times or in certain contexts.

**Implicit feedback:**
- **Always secure people's information** — implicit feedback can gather sensitive
  data.
- **Help people control their information.**
- **Don't let implicit feedback decrease opportunities to explore.** It **reinforces
  existing behavior** — better short-term, potentially worse long-term.
- **Use multiple feedback signals** to improve suggestions and mitigate mistakes —
  implicit signals are indirect and intent is hard to discern.
- **Consider withholding private or sensitive suggestions** — people share accounts
  and devices, and switch between personal and communal ones.
- **Prioritize recent feedback** — tastes change (Face ID prioritizes recent facial
  input).
- **Update predictions on a cadence matching the person's mental model** — typing
  suggestions update immediately; other predictions shouldn't churn constantly.
- **Be prepared for changes in implicit feedback when you change your UI** — even
  moving a button changes the amount and type of signal.
- **Beware of confirmation bias.** Implicit feedback is bounded by what people can
  already see and do — **it rarely reveals new things they might like.**

**Calibration:**
- **Always secure people's information**, **be clear about why you need it**, and
  **collect only the most essential information.**
- **Avoid asking people to calibrate more than once**, and **do it early** in the
  experience.
- **Make calibration quick and easy.**
- **Make sure people know how to succeed** — an explicit goal and visible progress.
- **Immediately provide assistance if progress stalls** — actionable
  recommendations, or people feel powerless and lose trust.
- **Confirm success** with a clear path into the feature.
- **Let people cancel at any time**, without implying judgment.
- **Give people a way to update or remove information they provided.**

**Mistakes:**
- **Understand the significance of a mistake's consequences.** *An incorrect keyboard
  suggestion annoys; a travel route causing a missed flight is serious.*
- **Make it easy to correct frequent or predictable mistakes.**
- **Continuously update your feature to reflect evolving interests.**
- **Address mistakes without complicating the UI where possible.**
- **Be especially careful in proactive features** — they promise value without the
  person asking, so mistakes cost more trust.
- **Consider the effect of reducing mistakes in one area on other areas and overall
  accuracy** — optimizing dog recognition may degrade cat recognition.
- **Give people familiar, easy ways to make corrections** — show the steps your app
  takes so corrections aren't confusing.
- **Provide immediate value when people make a correction.** Instantly display the
  corrected content, **and persist the update** so people never make the same
  correction twice.

**Confidence and how to express it:**
- **In scenarios where people expect statistical or numerical information, display
  confidence values that help them interpret results** — weather predictions, sports
  statistics, and polling numbers normally carry an interval or percentage.
- **In general, avoid technical or statistical jargon.** Percentages and statistics
  usually **don't help people assess results**. *The exception is when the result
  itself is statistical or technical* — weather, sports, polling and election
  results, scientific data.
- **Consider changing how you present results at different confidence thresholds.**
  When high or low confidence meaningfully changes how people can use a result,
  adapt the presentation. (Photos' face recognition simply shows the photos when
  confidence is high, but **asks people to confirm** when it's lower.)
- **In situations where attributions aren't helpful, consider ranking or ordering
  results in a way that implies confidence levels.**
- **Always balance the benefits of a feature against the effort required to correct
  it.** People tolerate mistakes from an automating feature, but **stop using it if
  doing the task themselves seems easier.**
- **Help people establish realistic expectations.** A limitation that's **rare but
  serious** should be disclosed *before* people rely on the feature — in marketing
  materials or in the feature's context — so they can decide how much to depend on
  it.

**Presenting confidence well:**
- **Know what your confidence values mean before deciding how to present them.**
  People forgive low-quality results from complementary features **especially when
  accompanied by attribution or context.**
- **In general, translate confidence values into concepts people already
  understand.** *Simply displaying a confidence value doesn't help people relate it
  to the result.*
- **Convey confidence as actionable suggestions wherever possible** — understanding
  people's goals is the key to expressing confidence in a way that helps them decide.
- **When confidence values correspond to result quality, avoid showing results when
  confidence is low** — **especially for proactive features that make unbidden
  suggestions**, where poor results annoy people and erode trust.

**Offering options:**
- **Prefer diverse options** — balance accuracy against diversity (Maps suggests a
  no-tolls route, a scenic route, and so on).
- **Avoid providing too many options** — each one adds cognitive load. **List options
  on one screen** so people don't scroll to find the right one.
- **List the most likely option first** — rank by confidence values where they
  correlate with quality, or by context like time of day or current location.
- **Make options easy to distinguish and choose** — when options look similar, give
  each a brief description. (People choosing a route need to decide fast.)
- **Consider using attributions to help people distinguish among results** — the
  premise behind each option helps people choose.

**Corrections:**
- **Never rely on corrections to make up for low-quality results.** Depending on them
  **erodes trust and reduces the value of the feature.**
- **Prefer guided corrections over freeform ones.** Guided corrections suggest
  specific alternatives and need less effort; freeform corrections demand more input.

**Transparency — attributions and limitations:**
- **Keep attributions factual and based on objective analysis.** An attribution must
  **help people reason about a result, not provoke an emotional response.** **Never
  imply understanding or judgment of people's emotions, preferences, or beliefs.**
- **Demonstrate how to get the best results.** Without guidance, **people assume the
  feature will do everything they want** — proactively showing good technique builds
  an accurate mental model.
- **Explain how limitations can cause unsatisfactory results.** People get frustrated
  when a feature seems to work **intermittently**; ideally the feature recognizes and
  describes *why* results are poor so people can adjust expectations.
- **Consider telling people when limitations are resolved.** Frequent users **learn
  to avoid interactions that fail** — notify them when an update removes a limitation
  so they can update their mental model.

## VoiceOver
- **Provide alternative labels for all key interface elements.**
- **Describe meaningful images** — without descriptions, people can't fully
  experience them.
- **Make charts and other infographics fully accessible** — a concise description of
  what each conveys, plus interactive detail if the chart is interactive.
- **Exclude purely decorative images from VoiceOver** — it "shows respect for
  people's time."
- **Use titles and headings to help people navigate your hierarchy.** *The title is
  the first information an assistive technology gives on arriving at a screen.*
- **Specify how elements are grouped, ordered, or linked.** Proximity and alignment
  convey relationships **visually only** — make them explicit.
- **Inform VoiceOver when visible content or layout changes** — otherwise a person's
  mental map silently becomes wrong.
- **Support the VoiceOver rotor** so people can navigate by headings, links, and
  other content types.
- **visionOS: custom gestures aren't always accessible.** With VoiceOver on, apps
  defining custom gestures **don't receive hand input by default**, so people can
  explore freely.

## Siri
- **Identify your app's most popular actions, and when and where they occur.**
- **Use familiar terms for your content and actions.**
- **Offer relevant content** to Spotlight — not everything, just what's relevant to
  someone's personal context.
- **Don't advertise.** No advertisements, marketing, or in-app-purchase pitches in
  content Siri delivers.
- **Only provide a custom response if built-in responses don't meet your needs.**
- **Write response dialogue that's clear and descriptive.**
- **Keep responses as succinct as possible** — people may hear the same response
  many times.
- **Provide responses Siri can deliver audibly AND visually** so it can choose per
  situation.
- **Design inclusive interactions** — **avoid specific pronouns when unnecessary.**
- **Ask an open-ended question when the option list is too long to read.**
- **Keep responses device-independent** — a request started on one device may take
  effect on another.
- **Omit your app name from responses** — the system already attributes your app
  verbally and visually.
- **Use appropriate language and respect parental controls.**
- **Help people understand errors and failures** — enhance the default descriptions
  with context-specific ones.
- **Refer to Siri by name — never with pronouns like *she*, *him*, or *her*.**
- **Never impersonate Siri** or reproduce its functionality; the system **reserves
  important actions and phrases** for Siri.
- **In localization, translate only the word *Hey* in "Hey Siri"** — ***Siri* is an
  Apple trademark and is never translated.**

## Sign in with Apple
- **Ask people to sign in only in exchange for value** — display a brief,
  approachable description of why.
- **Delay sign-in as long as possible.**
- **If you require an account, ask people to set it up BEFORE offering sign-in
  options** — explain the reasons first.
- **Consider letting people link an existing account to Sign in with Apple.**
- **In a commerce app, wait until after a purchase to ask for an account** — support
  guest checkout.
- **Welcome people to their new account as soon as it completes** — don't delay with
  more information requests.
- **Indicate when people are currently signed in** — e.g. "Using Sign in with Apple"
  in settings.
- **Clarify whether additional data you request is required or just recommended.**
- **Never ask people to supply a password** — that's the whole point.
- **Avoid asking for a personal email address when people supply a private relay
  address.**
- **Give people a chance to engage before asking for optional data.**
- **Be transparent about the data you collect.**
- **Button:** **display it prominently — no smaller than other sign-in buttons, and
  never requiring scrolling.** **Adjust the corner radius to match your other
  buttons.** **Maintain minimum button size and margins** (title length varies by
  locale). **Choose the logo file format by button height** — SVG and PDF scale to
  any height. **Prefer the system font** for "Sign in with Apple" / "Sign up with
  Apple" / "Continue with Apple". **Preserve the title's capitalization style.**
  **Keep title and logo vertically aligned.** **Inset the logo if needed** to align
  with other authentication logos. **Maintain a margin of at least 8% of the
  button's width** between title and right edge. **Logo-only buttons: always 1:1,
  no added horizontal padding** (the artwork includes correct padding); **use a mask
  to change the default square shape**; **minimum margin of 1/10 of the button's
  height.**

## Apple Pay
- **Offer Apple Pay on all devices and browsers that support it** — and **don't
  present it where unsupported.**
- **Make Apple Pay the primary payment option when credentials are available.**
- **Use Apple Pay buttons only to initiate payment or the Apple Pay setup process.**
- **A custom button must not display "Apple Pay" or the Apple Pay logo.**
- **Use the Apple Pay mark graphic only to communicate that you accept Apple Pay** —
  **it doesn't facilitate payment; never use it as a payment button.**
- **Don't hide an Apple Pay button or make it appear unavailable** — if it can't be
  used yet (no size selected), handle it gracefully.
- **Inform search engines that you accept Apple Pay** via semantic markup.
- **Provide a cohesive checkout experience** with your branding throughout.
- **If Apple Pay is available, assume people want to use it** — first option, larger,
  or visually emphasized.
- **Accelerate single-item purchases with buttons on product detail pages**, and
  **multi-item purchases with express checkout.**
- **Support coupons and promotional codes directly in the payment sheet.**
- **Collect necessary information (color, size) BEFORE people reach the button**,
  and **collect optional information (gift messages, delivery instructions) before
  checkout** — **there's no way to input optional data on the payment sheet.**
- **Gather multiple shipping methods and destinations before showing the sheet** —
  the sheet allows **a single method and destination per order.**
- **For in-store pickup, choose the location before the sheet**, then **show its
  address on the sheet.**
- **Prefer checkout information from Apple Pay** — assume it's complete and current,
  even over your stored data.
- **Avoid requiring account creation before purchase** — ask on the **order
  confirmation page** and prepopulate what you can.
- **Report transaction results in the payment sheet**, with error messages people can
  act on.
- **Display an order confirmation or thank-you page.**
- **Only present and request essential information** — extraneous information causes
  confusion and privacy concerns.
- **Line items:** use them for **additional charges, discounts, pending costs, add-on
  donations, recurring payments, and future payments.** **Keep them short — fit on a
  single line where possible.**
- **Provide a business name after the word *Pay* on the total line** — the same name
  people will see on their bank or credit statement.
- **If you're not the end merchant, identify both businesses.**
- **Clearly disclose when people may incur additional costs after authorization.**
- **Handle data entry and payment errors gracefully.** **Defer to the payment sheet
  for progress information** — it already shows loading and progress; extra spinners
  are noise.
- **Avoid forcing compliance with your business logic** — ignore irrelevant data and
  infer missing data where possible.
- **Accurately report problems to the system** with a custom message and the correct
  status code.
- **Explain invalid or misformatted data clearly and succinctly** — reference the
  field and say exactly what's expected.
- **Handle interruptions correctly** — cancellation or timeout dismisses the sheet.
- **Subscriptions:** **clarify details before showing the sheet** (billing
  frequency); **include line items reiterating frequency, discounts, and upfront
  fees**; **clearly communicate trial terms** (trial amount **including $0**, the
  regular amount after, and when it starts); **clarify the current payment amount in
  the total line**; **only show the payment sheet when a subscription change results
  in ADDITIONAL fees** — no authorization needed when the cost decreases.
- **Donations:** **use a line item to identify a donation** ("Donation $50.00"), and
  **offer predefined amounts** ($25, $50, $100) to streamline.
- **Buttons and marks:** **always use the Apple-provided API to display Apple Pay
  buttons** — API buttons are always correct and **localized automatically.**
  **Display prominently, no smaller than other payment buttons, no scrolling.**
  **In a side-by-side layout, place the Apple Pay button to the RIGHT of Add to
  Cart.** **Adjust corner radius to match your other buttons.** **Maintain minimum
  size and margins.** **Use only Apple-provided artwork, altering nothing but
  height.** **Minimum clear space around the mark: 1/10 of its height** — never
  share a border with another graphic or button.
- **Trademark:** **capitalize as "Apple Pay"** — two words, uppercase A and P.
  **Never use the Apple logo to represent "Apple" in text.** **Use ® on first
  appearance in body text (US).** **Coordinate font face and size with your app —
  don't mimic Apple typography.** **Never translate *Apple Pay*.** **A text-only
  description is allowed only when ALL payment options are text-only.**

## In-app purchase
- **Let people experience your app before making a purchase.**
- **Design an integrated shopping experience** — people shouldn't feel they've
  entered a different app.
- **Use simple, succinct product names and descriptions** that don't truncate or
  wrap.
- **Display the total billing price for every in-app purchase, regardless of type.**
- **Display your store only when people can make payments** — hide it or explain when
  parental restrictions block purchases.
- **Use the default confirmation sheet** — **don't modify it**; it prevents
  accidental purchases.
- **Family Sharing:** **mention it prominently** where people learn about your
  content (include "Family" or "Shareable" in the name); **help people understand
  the benefits and how to participate**; **customize in-app messaging so it makes
  sense to both purchasers and family members.**
- **Refunds:** **provide help people can view before requesting a refund**;
  **use a simple title like "Refund" or "Request a Refund"**; **help people find the
  problematic purchase** with contextual information; **consider offering alternative
  solutions** (immediate fulfillment, a conciliatory item); **make it easy to request
  a refund** — help content must not create an obstacle; **never characterize or give
  guidance on Apple's refund policies** or speculate about outcomes.
- **Subscriptions:** **call attention to benefits during onboarding**; **offer a range
  of content choices, service levels, and durations**; **consider free trial access**;
  **prompt at relevant times** (nearing a free-content limit) and make subscribing
  possible anytime; **only encourage a new subscription when someone isn't already a
  subscriber** — otherwise people think theirs lapsed; **provide clear,
  distinguishable options** with short self-explanatory names, price, and duration;
  **simplify signup, asking only for necessary information**; **tvOS: let people sign
  up or authenticate on another device**; **include Terms of Service and Privacy
  Policy links on the sign-up screen**; **clearly describe how a free trial works** —
  especially that **payment starts automatically when it ends**; **include a sign-up
  opportunity in your app's settings.**
- **Offers and codes:** **clearly explain offer details**; **custom codes use only
  alphanumeric ASCII characters**; **tell people how to redeem** (custom codes
  **can't** be entered in App Store account settings); **consider supporting
  redemption within your app**; **supply an engaging promotional image**; **help
  people benefit from unlocked content immediately after redemption.**
- **Management:** **provide summaries of subscriptions** including **the upcoming
  renewal date without searching**; **consider the system-provided
  subscription-management UI** (StoreKit); **consider ways to encourage people to
  keep or resubscribe** (StoreKit notifies your app on cancellation); **always make
  it easy to cancel an auto-renewable subscription** — burying it frustrates people;
  **consider a branded, contextual experience complementing the system UI.**
- **watchOS:** **clearly describe differences between versions on different devices**;
  **consider a modal sheet for required information**; **make subscription options
  easy to compare on a small screen.**

## Augmented reality (ARKit)
- **Offer AR features only on capable devices**, and **let people use the entire
  display.**
- **Strive for convincing illusions when placing realistic objects.** **Consider how
  reflective surfaces show the environment.** **Use audio and haptics to enhance
  immersion.**
- **In a three-dimensional context, prefer 3D hints** over 2D ones — a hint that
  shares the dimensionality of the space reads correctly from any viewing angle.
- **Minimize text in the environment.** If information or controls are necessary,
  **display them in screen space**; **use indirect controls for persistent
  controls.**
- **Anticipate a wide variety of real-world environments.**
- **Be mindful of people's comfort AND safety.** **Introduce motion gradually** if
  your app encourages movement.
- **Coaching views: hide unnecessary app UI while a coaching view is active**;
  **offer a custom coaching experience if necessary**; **show people when to locate a
  surface and place an object**; **immediately integrate a placed object into the AR
  environment**; **consider guiding people toward offscreen virtual objects.**
- **Avoid trying to precisely align objects with the edges of detected surfaces**;
  **incorporate plane classification information to inform placement.**
- **Let people use direct manipulation with standard, familiar gestures.**
  **Keep interactions simple.** **Respond to gestures within reasonable proximity of
  interactive objects.** **Let people initiate object scaling when it makes sense.**
  **Be wary of potentially conflicting gestures.**
- **Strive for movement consistent with the physics of your AR environment.**
- **Consider allowing people occlusion**, and **let new participants enter a
  multiuser AR experience.**
- **When a detected image first disappears, delay removing attached virtual
  objects.** ARKit **doesn't track position/orientation changes of detected images**,
  so **wait up to one second** to prevent flickering.
- **Relocalization:** **consider hiding previously placed virtual objects during
  relocalization** to avoid flickering, redisplaying them in their new positions.
  **Allow people to cancel relocalization** — if they don't return the device near
  its previous position and orientation, **relocalization continues indefinitely
  without success**; offer a reset button when coaching fails.
- **Limit the number of reference images requiring an accurate position**, and
  **limit the number of reference images in use at one time.**
- **Consider the system-provided coaching view to help people relocalize.**
- **Let people reset the experience if it doesn't meet their expectations**, and
  **suggest possible fixes when problems occur.**
- **Minimize interruptions if your app supports both AR and non-AR experiences.**
- **If you must display instructional text, use approachable terminology.**
- **Consider indirect controls when you need persistent controls**, and **explore
  more engaging methods of interaction** beyond the standard set.
- **Prefer the AR badge to the glyph-only badge.**
- **AR glyph and badges:** **the AR glyph is strictly for initiating an ARKit-based
  experience.** Never alter it (beyond size and color), use it for other purposes, or
  use it with non-ARKit AR experiences. **AR badges (collapsed and expanded) identify
  products or objects viewable in AR using ARKit** — never alter them or change their
  color. **Use badging only when your app mixes AR-viewable and non-AR-viewable
  objects** — if everything is AR-viewable, badging is redundant.

## App Clips
- **Allow people to complete a task or a demo**, **focus on essential features**, and
  **never use App Clips solely for marketing.**
- **Avoid web views.** **Design a linear, easy-to-use, focused interface.**
- **On launch, show the most relevant part**, and **ensure people can use it
  immediately.** **Ensure your App Clip is small.** **Make it shareable.**
- **Make it easy to pay**, and **avoid requiring an account** before people benefit.
  **Consider Sign in with Apple.** **Limit the data you store and handle yourself.**
  **Offer a secure, privacy-respecting way to pay.**
- **Don't compromise the experience by asking people to install the full app.**
  **Pick the right time to recommend it**, and do so **nonintrusively and politely.**
- **Notifications: only ask for extended-period permission if really needed; keep
  them focused; use them to help people complete a task.**
- **Cards:** **use consistent branding**, **consider multiple businesses**, **prefer
  photography and graphics**, **avoid text**, **adhere to image requirements**, **use
  concise copy**, **pick the action-button verb that best fits**, **include the App
  Clip logo when space allows.**
- **App Clip Codes:** **flat or cylindrical surfaces only**, **as flat as possible**,
  **in a location ensuring reliable scanning**, **unobstructed**, **upright**, **not
  too small**, **with enough space from adjacent codes, graphics, or materials**.
  **Always use the generated code.** **Choose colors with enough contrast.** **Use
  high-quality, non-textured print materials and high-resolution images/printer
  settings.** **Use correct color settings converting the SVG to CMYK.**
  **Grayscale printers → generate grayscale codes only.** **NFC-integrated codes need
  Type 5 NFC tags.** **Test print workflows and verify printed codes for large
  batches**, using the printer calibration test sheets.

## CarPlay
- **Eliminate app interactions on iPhone when CarPlay is active.**
- **Never lock people out of CarPlay because the connected iPhone requires input**,
  and **make sure your app works without requiring people to unlock iPhone.**
- **Report errors in CarPlay, not on the connected iPhone.**
- **Audio: let people choose when to start playback**; **start as soon as audio has
  sufficiently loaded**; **display the Now Playing screen when audio is ready**;
  **resume after an interruption only when appropriate**; **adjust levels
  automatically when necessary but never change the overall volume.**
- **Provide useful, high-value information in a clean layout that's easy to scan from
  the driver's seat.** **Maintain a consistent appearance throughout.** **Ensure
  primary content stands out and feels actionable.**
- **Prefer a limited color palette coordinating with your app logo.** **Never use the
  same color for interactive and noninteractive elements.** **Test your color scheme
  under a variety of lighting conditions in an actual car.** **Ensure it looks great
  in both dark and light environments.** **Choose colors that communicate effectively
  with everyone.**
- **Supply @2x and @3x images for all CarPlay artwork.** **Mirror your iPhone app
  icon.** **Don't use black for the icon background.**

## HealthKit
- **Provide a coherent privacy policy.** **Request access to health data only when
  you need it.** **Clarify intent with descriptive messages on the standard
  permission screen.** **Manage health data sharing solely through system privacy
  settings.**
- **Activity rings** (as in Components): **Move, Exercise, Stand only**, **single
  person only**, **never for ornamentation or branding**, **maintain ring and
  background colors**, **maintain margins**, **differentiate other ring-like
  elements.**
- **Provide app-specific information only in Activity notifications.**
- **Apple Health icon:** **use only the Apple-provided icon**; **display the name
  *Apple Health* close to it**; **display it consistently with other health-related
  app icons**; **never use it as a button**; **never alter its appearance**;
  **minimum clear space 1/10 of its height**; **never use it within text or as a
  replacement for the words *Health*, *Apple Health*, or *HealthKit*.**
- **Don't display Health app images or screenshots.** **Refer to the app as *Apple
  Health* or *the Apple Health app*.** **Don't use the term *HealthKit*** in
  user-facing text. **Use correct capitalization**, and **use the system-provided
  translation of *Health*.**

## HomeKit
- **Acknowledge the hierarchical model HomeKit uses**, and **recognize people can
  have more than one home.**
- **Make it easy to find an accessory's related HomeKit details.** **Don't present
  duplicate home settings.**
- **Use the system-provided setup flow.** **Provide context explaining why you need
  Home data access.** **Never require an account or personal information.** **Honor
  people's setup choices.** **Carefully consider how and when to provide a custom
  accessory setup experience.**
- **Suggest service names that suit your accessory**, **check names follow HomeKit
  naming rules**, and **help people avoid names that include location information.**
- **Present example voice commands during setup**, and **teach more complex Siri
  commands afterward.** **Recommend zones and service groups where they make sense.**
- **Offer shortcuts only for accessory-specific functionality HomeKit doesn't
  support**, and **help people understand the difference** between the two kinds of
  voice control.
- **Be clear about what people can do in your app vs. the Home app.** **Defer to
  HomeKit if your database differs.** **Ask permission before updating the HomeKit
  database from changes in your app.**
- **Don't block camera images.** **Show a microphone button only if the camera
  supports bidirectional audio.**
- **HomeKit icon:** **Apple-provided icons only**, positioned consistently with other
  technology icons, **noninteractive**, **never within text or as a replacement for
  the word HomeKit**, **paired with the name correctly**. **Emphasize your app over
  HomeKit.** **Never suggest HomeKit is performing an action.** **Use *Apple Home*
  when referring specifically to the app.**

## iCloud
- **Make it easy to use your app with iCloud**, and **avoid asking which documents to
  keep in iCloud.**
- **Keep content up to date when possible** and **respect iCloud storage space.**
- **Behave appropriately when iCloud is unavailable.**
- **Keep app state information in iCloud.**
- **Warn about the consequences of deleting a document.**
- **Make conflict resolution prompt and easy.**
- **Include iCloud content in search results.**
- **For games, consider saving player progress in iCloud.**

## Maps
- **In general, make your map interactive**, and **pick a map emphasis style that
  suits your app.**
- **Help people find places in your map.** **Clearly identify selected elements.**
  **Cluster overlapping points of interest to improve legibility.**
- **Help people see the Apple logo and legal link.**
- **Use annotations matching your app's visual style**; **make custom information
  related to standard map features independently selectable**; **use overlays for map
  areas with a specific relationship to your content**; **ensure enough contrast
  between custom controls and the map.**
- **Place cards:** **consider your map presentation when choosing a style**; **look
  great on different devices and window sizes**; **avoid duplicating information**;
  **keep the location visible while a place card shows**; **use location-related cues
  in surrounding content** to signal a card can be opened.
- **Indoor maps:** **adjust detail by zoom level**; **use distinctive styling to
  differentiate features**; **offer a floor picker for multiple levels**; **include
  surrounding areas for context**; **consider navigation between your venue and
  nearby transit**; **limit scrolling outside your venue**; **design a map that feels
  like a natural extension of your app.**
- **Map interface elements: fit to the screen** and **show the smallest region
  encompassing the points of interest.**

## NFC
- **Don't encourage people to make contact with physical objects** — scanning works
  at a distance.
- **Use approachable terminology.**

## AirPlay
- **Prefer the system-provided media player** — standard controls plus chapter
  navigation, subtitles, and closed captioning.
- **Provide content in the highest possible resolution** — the HLS playlist must
  include the **full range of available resolutions.**
- **Stream only the content people expect.** **Don't stream background loops or short
  video experiences** that only make sense inside the app.
- **Support both AirPlay streaming and mirroring**, and **support remote control
  events** so people can play, pause, and fast forward from the Lock Screen, Siri, or
  HomePod.
- **Don't stop playback when your app enters the background or the device locks.**
- **Don't interrupt another app's playback unless you're starting immersive content.**
- **Let people use other parts of your app during playback** — the app must remain
  functional when AirPlay is active.
- **Provide a custom playback interface only if you can't use the system player.**
- **Icon and name:** **position the AirPlay icon consistently with other technology
  icons**; **never use the icon or the name in custom buttons or interactive
  elements** — noninteractive only; **pair icon and name correctly**; **emphasize
  your app over AirPlay**; **capitalize as "AirPlay"** (one word, uppercase A and P);
  **always use *AirPlay* as a noun**; use terms like ***works with*, *use*,
  *supports*, *compatible***.

## Always On (watchOS)
- **Hide sensitive information.** Redact what people wouldn't want casual observers
  to see — **bank balances, health data.**
- **Keep other personal information glanceable when it makes sense** — pace and heart
  rate during a workout.
- **Keep important content legible and dim nonessential content** — increase dimming
  on secondary text, images, and color fills.
- **Maintain a consistent layout.** Avoid distracting interface changes when Always
  On begins or ends, and throughout.
- **Gracefully transition motion to a resting state — don't stop it instantly.**
  Smoothly finishing communicates the transition instead of looking like a freeze.

## Game Center
- **Display the access point in menu screens** — main menu or settings. **Avoid
  displaying it during active gameplay.**
- **Avoid placing controls near the access point** (it sits fixed in one of the four
  screen corners).
- **Consider pausing your game while the Game Overlay or dashboard is present.**
- **Use the artwork Game Center provides in custom links**, preserving its
  appearance, and **use the correct terminology.**
- **Achievements:** **align with the four states — locked, in-progress, hidden,
  completed.** **Determine a display order** — upload order is display order. **Be
  succinct: the achievement card limits title and description to two lines each**, and
  truncates beyond. **Give players a sense of progress** with progressive
  achievements. **Design rich, high-quality images.** **Create artwork at the correct
  size and format — the system applies a circular mask, so keep content centered.**
- **Leaderboards:** **choose a type — *classic* or *recurring*.** **Take advantage of
  leaderboard sets** to organize multiple boards. **Add leaderboard images**, aiming
  for a unique one per board.
- **Challenges:** **create engaging challenges** — short, skill-based activities with
  a clear way to gauge accomplishment, taking **1–7 days**. **Avoid challenges
  tracking overall progress or personal bests** — they give regular players an unfair
  advantage; **track the most recent score after each attempt** instead. **Always
  deep-link into the challenge.** **Create high-quality challenge artwork** — it
  appears in the Game Overlay, Games app, and invitation previews.
- **Multiplayer:** **use party codes to invite players to real-time multiplayer
  sessions.** **Support multiplayer through in-game UI.** **Provide engaging activity
  artwork** — the preview image appears throughout the system.
- **tvOS: consider an optional image at the top of the dashboard** — simple and easily
  recognizable.
- **watchOS: GameKit APIs are available, but there is NO system-supported Game Center
  UI** you can present.

## SharePlay
- **Use SharePlay for real-time experiences** — activities people do together **at the
  same moment**. Asynchronous collaboration needs a different mechanism.
- **Design an experience that fits what people are doing together.** Watching or
  browsing → everyone shares one view.
- **Design activities that work across Apple platforms**, devices, settings, and
  communication methods.
- **Make it easy to start a shared activity** — a clear, recognizable control
  including the **SharePlay symbol**.
- **Let people join without friction** — get them to the shared content quickly,
  avoiding unrelated views.
- **Describe activities clearly and concisely** so an invitation explains what someone
  is joining.
- **Keep people oriented as an activity changes** — explain why one person's action
  changed things for everyone.
- **Use the term *SharePlay* correctly** — as a noun ("Join SharePlay") or as a verb
  describing an action ("SharePlay Movie").
- **Support Picture in Picture for shared video** so people keep watching while doing
  other things.
- **Resolve conflicts naturally** — when more than one person acts on the same thing,
  avoid abrupt seizing of control.
- **visionOS:** **prefer starting your experience from a window** (shareable via the
  Share button next to the window bar). **Reserve unique views for moments that call
  for them** — generally keep views and immersion levels in sync. **Let people opt in
  to immersion changes when they're mid-task.** **Let participants customize volume,
  subtitles, and other comfort/accessibility settings** independently. **Make it easy
  to leave and rejoin** with a clear rejoin control. **Support people who aren't
  represented by a spatial Persona** — people join from other devices.
- **Spatial templates:** **divide a complex activity into stages**, each with its own
  template. **Let people initiate template transitions** — unexpected role or seat
  swaps are disorienting. **Keep transitions smooth** — avoid frequent transitions or
  excessive movement; **fade out and back in** when moving someone. **Account for
  people physically together** — same-room Vision Pro users see each other through
  passthrough, not as Personas. **Provide the best seat orientation** (seats face the
  content center by default). **Support the maximum number of seats — five spatial
  Personas.** **Place seats at least a meter apart.** **Define the order in which
  people take seats** so the arrangement stays balanced as people join. **Keep roles
  independent of seats** — player, spectator, or team member must work for everyone.

## Wallet
- **Offer to add new passes to Wallet** when an action creates one (event ticket,
  rewards registration).
- **Help people add a pass created outside your app** — suggest adding it next time
  they open the app.
- **Add related passes as a group** — all boarding passes for a multi-connection
  flight at once.
- **Display an Add to Apple Wallet button** for an existing pass not in Wallet.
- **Let people jump from your app to their pass in Wallet.**
- **Tell the system when your passes expire** — Wallet hides expired passes to reduce
  crowding, with a button to revisit them.
- **Always get permission before deleting passes from Wallet.**
- **Help the system suggest a pass when relevant** so passes appear without being
  hunted for.
- **Keep passes up to date** — a boarding pass can update automatically.
- **Use change messages only for time-critical updates** — a change message
  **interrupts**.
- **Pass design:** **look great on all devices** (Apple Watch shows less information
  and fewer fields). **Keep the front uncluttered** — essential information in the
  **header**, visible while collapsed. **Make it instantly identifiable** with brand
  colors and visuals. **Ensure sufficient contrast** against solid backgrounds *and*
  background images. **Use language that works on any device** — "Slide to view" means
  nothing on some. **Reserve pass images for visual content** — **embedded text isn't
  accessible** and may not display; use text fields and semantic fields. **Keep image
  file sizes small** for fast download over email or web. **Provide a pass icon** (the
  app icon or a separate design) for the Lock Screen, Mail, and Wallet. **Avoid inner
  drop shadows on logo artwork.**
- **Orders:** **make it easy to add an order to Wallet** after an Apple Pay
  transaction. **Make order information available immediately after placement.**
  **Provide fulfillment information as soon as available and keep status current.**
  **Supply a high-resolution logo with a nontransparent background**, and **distinct,
  high-resolution product images with nontransparent backgrounds.** **Keep text
  brief** — the system truncates. **Use clear, approachable, localized language.**
  **Provide a universal link to order management** (works without your app installed).
  **Clearly describe each item.** **Supply a prioritized list of your apps** for
  in-order links. **Avoid duplicate notifications.** **Make it easy to contact the
  merchant** with multiple methods. **Help people track their order** — a multi-item
  order can have multiple fulfillments, each shipping or pickup. **Keep the
  fulfillment screen centered on order tracking** — prioritize it over app
  recommendations. **Choose shipping-fulfillment values matching what you actually
  know** (leave `carrier` empty if unknown). **Keep customers informed with
  approachable, accurate status descriptions.** **Be direct and thorough describing an
  Issue or Canceled status** — why, and what they can do.
- **Identity verification:** **present a Wallet verification option only when the
  device supports it.** **Ask for identity information only at the precise moment you
  need it.** **Clearly and succinctly describe why.** **Ask only for the data you
  actually need.** **Clearly indicate whether you'll keep the data and for how long.**
  **Choose the system-provided verification button matching your use case.**

## Tap to Pay on iPhone
- **Help merchants accept terms and conditions before they interact with customers** —
  and **present them only to an administrative user** (explain to non-admins that an
  administrator must do it).
- **Help merchants keep their device up to date** if your PSP requires specific iOS
  versions.
- **Provide a tutorial covering the supported payment types** and how to accept each.
- **Provide Tap to Pay on iPhone as a checkout option whether or not it's enabled.**
- **Avoid making merchants wait** — configuration is needed initially **and again
  periodically**. **Keep the checkout option available even while configuration
  continues in the background.**
- **Make the button easy to find** if you support multiple payment-acceptance methods
  — **don't make merchants scroll**. **Make it easy to switch between Tap to Pay and
  hardware accessories.**
- **Label the button "Tap to Pay on iPhone", or "Tap to Pay" if space is
  constrained**, and **design it to match your app's other buttons.**
- **Determine the final amount before merchants initiate the experience** (tips and
  other customer interactions come first). **Display pre-payment options before the
  Tap to Pay screen.**
- **Start processing a transaction as soon as possible** — API returns the tap result
  before the screen finishes dismissing.
- **Display a progress indicator while payment authorizes** — it can take several
  seconds.
- **Clearly display the transaction result, declined or successful.** Declines happen
  for insufficient funds, suspected fraud, and other reasons.
- **Help merchants complete checkout when a payment can't complete** (unreadable card,
  unsupported type).
- **If the system returns a merchant-addressable error, clearly describe the problem
  and recommend a resolution.** **Make it easy to get help** with unresolvable issues.
- **Use a generic label when there's no transaction amount** (reading a card) —
  **don't include "Tap to Pay on iPhone" or "Tap to Pay".**
- **Distinguish an independent loyalty-card transaction from a payment-acceptance
  flow.**

## ShazamKit
- **Stop recording as soon as possible.** People **don't expect the microphone to stay
  on** — record only for as long as recognition needs.
- **Let people opt in to storing recognized songs to their iCloud library.**

## ID Verifier
- **Ask only for the data you need** — over-asking loses trust.
- **Register for ID Verifier via Apple Business Register if you qualify**, so people
  can see essential information about your organization when you make a request.
- **Provide a button that initiates verification** — "Verify Age" for a simple age
  check, "Verify Identity" for detailed identity data.
- **In a Display Only request, help the person using your app record the visual
  confirmation they perform.**

## ResearchKit
- **Always display the onboarding screens in the correct order.**
- **Provide an introduction that informs and provides a call to action.**
- **Determine eligibility as soon as possible.**
- **Make sure participants understand your study before you get their consent** —
  **break a long consent form into easily digestible sections**, and **consider a quiz
  that tests understanding.**
- **Get the participant's consent and, if appropriate, contact information.**
- **Get permission to access the participant's device or data, and to send
  notifications.**
- **Create surveys that keep participants engaged**, and **make active tasks easy to
  understand.**
- **Use a profile to help participants manage personal data related to your study.**
- **Use a dashboard to show progress and motivate participants to continue.**

## CareKit
- **Provide a coherent privacy policy.** **Request access to health data only when
  needed.** **Clarify intent with descriptive messages on the permission screen.**
  **Manage health data sharing solely through system privacy settings.**
- **Task styles:** **simple** for a one-step task · **instructions** when a simple
  task needs informative text · **log** to help people log events · **checklist** for
  a list of actions or steps in a multistep task · **grid** for a grid of buttons in a
  multistep task.
- **Consider using color to reinforce the meaning of task items.**
- **Combine accuracy with simplicity when describing a task and its steps**, and
  **consider supplementing multistep or complex tasks with videos or images.**
- **Charts:** **consider highlighting narratives and trends to illustrate progress**;
  **label chart elements clearly and succinctly**; **use distinct colors**;
  **consider providing a legend**; **clearly denote units of time**; **consolidate
  large data sets for readability**; **if necessary, offset data to keep charts
  proportional.**
- **Consider using color to categorize care team members.**
- **Minimize notifications**, and **consider providing a detail view.**
- **Design a relevant care symbol**, and **incorporate refined, unobtrusive
  branding.**

## iMessage apps and stickers
- **Prefer providing one primary experience in your iMessage app.**
- **Consider surfacing content from your iOS or iPadOS app.**
- **Present essential features in the compact view.**
- **In general, let people edit text only in the expanded view.**
- **Create stickers that are expressive, inclusive, and versatile.**
- **Provide a localized alternative description for each sticker.**

## Live Photos
- **Apply adjustments to all frames**, and **keep Live Photo content intact.**
- **Implement a great photo sharing experience.**
- **Clearly indicate when a Live Photo is downloading and when it's playable.**
- **Display Live Photos as traditional photos in environments that don't support
  them.**
- **Make Live Photos easily distinguishable from still photos**, and **keep badge
  placement consistent.**

## Photo editing
- **Confirm cancellation of edits.**
- **Don't provide a custom top toolbar.**
- **Let people preview edits.**
- **Use your app icon for your photo editing extension icon.**

## Mac Catalyst
- **When you adopt the Mac idiom, thoroughly audit your layout and plan to change
  it.**
- **Adjust font sizes as needed**, and **make sure views and images look good in the
  Mac version.**
- **Limit appearance customizations to standard macOS ones.**
- **Make sure people retain access to important tab-bar items in the Mac version.**
- **Offer multiple ways to move between pages.**
- **Create a macOS version of your app icon.**
- **Consider moving controls from your iPad app's main UI into the Mac toolbar.**
- **As much as possible, adopt a top-down flow**, and **relocate buttons from the side
  and bottom edges of the screen.**
- Support **keyboard navigation and shortcuts** and **multiple windows.**
