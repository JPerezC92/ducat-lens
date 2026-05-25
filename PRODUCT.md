# Product

## Register

product

## Users

Intermediate-to-veteran Warframe players who understand what Prime parts and Ducat Kiosks are. They arrive mid-session — fresh from a farming run, inventory screen still open in-game, 10-30 Prime parts to evaluate. Their job is fast triage: which parts are worth selling at the Kiosk for ducats vs. keeping for trading or building. They do not want to open a wiki tab for each part. Tech-comfortable; familiar with companion tools like Warframe Market and the Warframe Wiki.

## Product Purpose

ducat-lens accepts a screenshot of the Warframe Ducat Kiosk inventory screen, OCRs the visible Prime parts using RapidOCR, looks up each part's ducat value from a bundled WFCD/warframe-items dataset (with api.warframe.market REST fallback), and returns a ranked result table with a SELL / KEEP / CONSIDER verdict for each item. No signup, no install, stateless — results in under five seconds.

Success looks like: player uploads screenshot, gets an actionable table in one interaction, makes their Kiosk decision immediately without opening another tab.

## Brand Personality

Cold, precise, functional. Three words: terminal, gritty, trustworthy.

Voice: Warframe 1999 / Höllvania register — the in-world tone of a Techrot diagnostic terminal. Clipped, data-forward, no marketing softness. Errors read like system alerts, not apology messages. Labels read like field headings on a field kit, not friendly helper copy.

Emotional goal: the player should feel equipped and confident. Not delighted — equipped. The tool should feel like it knows more than they do and is giving them a precise readout.

Reference aesthetic: Warframe's own Pom-2 OS (DE-OS desktop, CRT monitor UI) and KIM messenger interface. Ghost in the Shell, Blade Runner 2049 UI language. Late-90s terminal and field-kit readout aesthetics. NOT Mass Effect-adjacent space opera. NOT Orokin gold-and-white classic Warframe.

## Anti-references

- Generic SaaS "modern minimalism": rounded corners, pastel accents, cream backgrounds, friendly sans-serif headlines. This is not a productivity app for knowledge workers.
- Classic Warframe Orokin aesthetic: gold filigree, white voids, energy-field borders. That era is pre-1999 in-world.
- Marketing landing pages with hero sections, big scroll-driven reveal animations, social proof blocks. This is a tool; register is product.
- Mobile-first card grids everywhere. ducat-lens is desktop-first; the Kiosk screenshot workflow is a desktop action.
- Cute or playful copy. The in-world atmosphere is decay, punk resistance, industrial grit.
- Glassmorphism or frosted-panel aesthetics.
- Gradient text as a default treatment.

## Design Principles

1. Speed-to-answer: every interaction decision optimizes for time-to-verdict. The upload zone is primary, results are immediate, no modal gates before the answer.
2. Trust through precision: ducat values are numbers — show exact figures, not rounded or implied. Recommendation thresholds are visible and explained on the surface, not hidden in a tooltip.
3. Visual coherence earns its reference: every UI element that invokes Warframe 1999 aesthetics (CRT scanlines, bracket corners, phosphor glows) must serve clarity, not obstruct it. If a period detail conflicts with readability, clarity wins.
4. The interface disappears into the task: chrome is minimal; the results table is the product. Navigation, branding, and decoration take a back seat to the data readout.
5. Accessibility is non-negotiable: WCAG 2.2 AA minimum throughout. The 1999 palette (dark backgrounds, neon accents) is high-contrast by nature — verify each token pair, especially mid-value text on surface colors.

## Accessibility & Inclusion

WCAG 2.2 AA required on all interactive and text surfaces. The site is permanently dark (Höllvania theme, no light-mode toggle). Color is never the sole conveyor of meaning — every status (SELL / KEEP / CONSIDER) carries a text label alongside any color indicator. Focus indicators use the cold-blue accent (`#3fc8e0`) at sufficient contrast against dark backgrounds. Reduced-motion: all scan-sweep and flicker animations respect `prefers-reduced-motion: reduce`. Touch targets minimum 44px even though desktop-first — mobile users exist. No time-limited interactions.
