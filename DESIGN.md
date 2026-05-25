---
name: ducat-lens
description: "Warframe Ducat Kiosk analyzer — terminal-accurate, data-forward, permanently dark."
colors:
  bg: "#0d0f14"
  surface: "#1a1d26"
  surface-alt: "#14172a"
  text-primary: "#e8eaf0"
  text-secondary: "#8a9ab0"
  text-muted: "#6e7e9c"
  accent-blue: "#3fc8e0"
  token-gold: "#c8a84b"
  status-success: "#4cde5a"
  status-warning: "#d4b820"
  status-error: "#e03030"
  border-default: "rgba(63,200,224,0.25)"
typography:
  display:
    fontFamily: "Rajdhani, Barlow Condensed, sans-serif"
    fontSize: "clamp(1.5rem, 3vw, 2.25rem)"
    fontWeight: 700
    lineHeight: 1.1
    letterSpacing: "0.05em"
  headline:
    fontFamily: "Rajdhani, Barlow Condensed, sans-serif"
    fontSize: "1.25rem"
    fontWeight: 700
    lineHeight: 1.2
    letterSpacing: "0.04em"
  title:
    fontFamily: "Rajdhani, Barlow Condensed, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 700
    lineHeight: 1.3
    letterSpacing: "0.08em"
  body:
    fontFamily: "Roboto, sans-serif"
    fontSize: "0.875rem"
    fontWeight: 400
    lineHeight: 1.6
    letterSpacing: "normal"
  label:
    fontFamily: "IBM Plex Mono, Share Tech Mono, monospace"
    fontSize: "0.75rem"
    fontWeight: 400
    lineHeight: 1.4
    letterSpacing: "0.04em"
rounded:
  none: "0px"
  xs: "1px"
  sm: "2px"
  md: "2px"
  lg: "4px"
spacing:
  xs: "4px"
  sm: "8px"
  md: "16px"
  lg: "24px"
  xl: "40px"
  "2xl": "64px"
components:
  button-primary:
    backgroundColor: "{colors.accent-blue}"
    textColor: "{colors.bg}"
    rounded: "{rounded.sm}"
    padding: "8px 20px"
    typography: "{typography.title}"
  button-primary-hover:
    backgroundColor: "#5cd5ea"
    textColor: "{colors.bg}"
  button-outline:
    backgroundColor: "transparent"
    textColor: "{colors.accent-blue}"
    rounded: "{rounded.sm}"
    padding: "8px 20px"
  button-ghost:
    backgroundColor: "transparent"
    textColor: "{colors.text-secondary}"
    rounded: "{rounded.sm}"
    padding: "8px 20px"
  upload-zone:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text-primary}"
    rounded: "{rounded.sm}"
    padding: "32px 24px"
  upload-zone-hover:
    backgroundColor: "#1f2333"
    textColor: "{colors.accent-blue}"
  verdict-sell:
    backgroundColor: "rgba(76,222,90,0.12)"
    textColor: "{colors.status-success}"
    rounded: "{rounded.xs}"
    padding: "2px 8px"
  verdict-keep:
    backgroundColor: "rgba(138,154,176,0.12)"
    textColor: "{colors.text-secondary}"
    rounded: "{rounded.xs}"
    padding: "2px 8px"
  verdict-consider:
    backgroundColor: "rgba(212,184,32,0.12)"
    textColor: "{colors.status-warning}"
    rounded: "{rounded.xs}"
    padding: "2px 8px"
---

# Design System: ducat-lens

## 1. Overview

**Creative North Star: "The Techrot Diagnostic Terminal"**

ducat-lens renders as a Höllvania field-kit readout: dark, precise, and stripped to function. Every design decision defers to the data. The upload zone is a hardware slot; the results table is the primary output — chrome around it earns no attention. The palette is desaturated near-black with cold-blue UI chrome, Orokin gold reserved exclusively for ducat values (those are literally the currency the tool is analyzing), and phosphor greens for sell signals. Neon is earned, not ambient.

The aesthetic is Warframe 1999 / Höllvania — Pom-2 OS meets KIM messenger — translated to the web through ASCII corner brackets, 1px panel borders, inset scanlines on card surfaces (never full-viewport), and snappy 150ms state transitions. The motion vocabulary is boot-sequence and scan-sweep, not smooth holographic glides.

This system explicitly rejects the Orokin aesthetic (gold filigree, white voids, energy-field glow borders) that characterizes classic Warframe. It also rejects generic SaaS minimalism (rounded corners, pastel accents, cream backgrounds, friendly onboarding copy) and marketing-page register (hero sections, scroll reveals, social proof). The register is product. The density is a feature.

**Key Characteristics:**
- Permanently dark. No light-mode variant. Background is `#0d0f14` — raised black with cool blue-grey cast.
- Accent blue (`#3fc8e0`) is the single UI chrome color. It appears on borders, focus rings, scan animations, and interactive states. Rarity is the point.
- Orokin gold (`#c8a84b`) is reserved: ducat value column only, logo, and KIM-approval-style positive verdict tints. One use earns its heritage.
- Typography is heading-to-mono: Rajdhani Bold for panel titles and labels, IBM Plex Mono for data values and table cells, Roboto for body copy.
- Borders are 1px. Panel radius is 2px or 0. No decorative curves.
- Motion is period-accurate: 150ms snappy transitions, a 400ms scan-sweep on results reveal, 80ms flicker on hover for neon elements.

## 2. Colors: The Höllvania Palette

The palette derives from Warframe 1999's two confirmed zone color families (mall/street: cold blue-teal; underground/Techrot: desaturated green) plus the KIM golden approval gradient for favorable outcomes.

### Primary
- **Cold Phosphor Blue** (`#3fc8e0`): UI chrome, interactive borders, focus rings, scan-sweep animation, hover states on accent elements, column headers in the results table. Single accent color. Appears on at most 15% of any given screen surface.

### Secondary
- **Orokin Ducat Gold** (`#c8a84b`): Ducat value column in the results table, logo inner star, SELL verdict background tint. Intentionally sparse — it only appears where literal Orokin currency is the subject.

### Tertiary
- **Techrot Signal Green** (`#4cde5a`): SELL verdict badge foreground, high-value row left-border accent, positive status icons. Derived from Efervon chemical green (in-world hazard/signal color). Not used for decorative purposes.

### Neutral
- **Höllvania Near-Black** (`#0d0f14`): Page background. Cool blue cast, not pure black. Alternating table row (primary stripe).
- **Desaturated Charcoal** (`#1a1d26`): Card and panel background. Upload zone, results container, header bar.
- **Surface Alternate** (`#14172a`): Alternating table row (secondary stripe), secondary panel variants.
- **Near-White** (`#e8eaf0`): Primary text. High contrast against all surface tokens.
- **Cool Grey** (`#8a9ab0`): Secondary text, icon fills, sort/filter controls, KEEP verdict label.
- **Muted Slate** (`#6e7e9c`): Metadata, placeholder text, disabled states. Verified ~4.75:1 on `#0d0f14` — clears WCAG AA.
- **Translucent Blue Border** (`rgba(63,200,224,0.25)`): Default panel border and input border. At rest — blue but quiet.

### Status
- **Efervon Green** (`#4cde5a`): SELL — success / positive.
- **Techrot Yellow** (`#d4b820`): CONSIDER — uncertain / infected.
- **Devil's Triad Red** (`#e03030`): ERROR — failed OCR, network failure.

**The One-Voice Rule.** `#3fc8e0` is the only interactive UI accent. It must not share the screen with a second accent color at equal weight. Status colors (green, yellow, red) are data annotations, not UI chrome — they appear only on verdict badges and status indicators.

**The Gold Containment Rule.** `#c8a84b` appears in exactly two contexts: the Ducats column and the SELL verdict background tint. Using it elsewhere dilutes the earned reference and looks like Orokin aesthetic regression.

## 3. Typography

**Display Font:** Rajdhani Bold (Google Fonts, `weights: 700`) with `Barlow Condensed, sans-serif` fallback
**Body Font:** Roboto (Google Fonts, `weights: 400, 500`) with `sans-serif` fallback
**Data/Mono Font:** IBM Plex Mono (Google Fonts, `weights: 400, 500`) with `Share Tech Mono, monospace` fallback

**Character:** Rajdhani's condensed geometry carries the industrial-broadcast personality of the 1999 Techrot terminal. IBM Plex Mono grounds data values in precision. Roboto (exact Warframe in-game match) handles body copy without stylistic noise. The pairing reads simultaneously as late-90s OS and contemporary data tool — the intended ambiguity.

### Hierarchy
- **Display** (Rajdhani Bold 700, `clamp(1.5rem, 3vw, 2.25rem)`, line-height 1.1, tracking 0.05em): Panel section titles, the main "DUCAT ANALYSIS" heading. Uppercase.
- **Headline** (Rajdhani Bold 700, `1.25rem`, line-height 1.2, tracking 0.04em): Table column headers, card titles, status readout labels.
- **Title** (Rajdhani Bold 700, `0.875rem`, line-height 1.3, tracking 0.08em): Button labels, verdict badge text, upload zone instruction line.
- **Body** (Roboto 400, `0.875rem`, line-height 1.6, normal tracking): Upload hint copy, error messages, empty states. Max line length 65ch.
- **Label** (IBM Plex Mono 400, `0.75rem`, line-height 1.4, tracking 0.04em): Item names in the results table, ducat values, row metadata, all numeric data output.

**The Mono-for-Numbers Rule.** Every ducat value, part count, and numeric data field renders in IBM Plex Mono. This is non-negotiable. Proportional fonts on tabular numbers break column alignment and erode the field-kit readout feel.

**Load Strategy.** All three families load via `<link rel="preconnect">` in BaseLayout plus `<link rel="stylesheet">` with `display=swap`. Subset to Latin. Do not use `@import` inside CSS — it blocks rendering.

## 4. Elevation

This system uses tonal layering, not shadows. Depth is conveyed through background lightness steps: `#0d0f14` (page) → `#1a1d26` (panel) → `#14172a` (inset/alternate). Three levels. No `box-shadow` for structural hierarchy.

Glow is reserved for interactive state feedback only, not for permanent elevation. A focused input or hovered neon element receives a directional `box-shadow` in `rgba(63,200,224,0.4)`. This is a response to state, not a structural signal.

### Shadow Vocabulary
- **Focus glow** (`box-shadow: 0 0 0 2px rgba(63,200,224,0.5)`): Focus-visible state on interactive elements. Replaces the typical focus ring with a cold-blue phosphor halo.
- **Hover glow on accent elements** (`box-shadow: 0 0 12px rgba(63,200,224,0.35)`): Upload zone active/drag-over state; neon-bordered panels on hover.
- **Error glow** (`box-shadow: 0 0 0 2px rgba(224,48,48,0.5)`): Input in invalid/error state.

**The Flat-By-Default Rule.** Panels are flat at rest. `box-shadow` appears only in response to interaction state (hover, focus, drag-over, error). A card does not have a permanent shadow.

## 5. Components

### Buttons
- **Shape:** Nearly square corners (2px radius, `--radius: 0.125rem`). Matches period-UI aesthetic — Windows-era dialog buttons.
- **Primary:** `bg-primary text-primary-foreground` = cold blue background (`#3fc8e0`) on near-black text (`#0d0f14`). Padding `px-5 py-2`. Uppercase Rajdhani 700, tracking-wider.
- **Hover:** Background steps to `#5cd5ea`. Transition `150ms ease-out`. No scale transform.
- **Focus-visible:** `ring-2 ring-accent-blue/50 outline-none`.
- **Secondary/Outline:** `border border-accent-blue/40 bg-transparent text-accent-blue`. Hover: `bg-surface`.
- **Ghost:** `text-text-secondary hover:text-text-primary hover:bg-surface-alt`. For tertiary actions only.
- **Destructive:** `bg-status-error/10 text-status-error hover:bg-status-error/20`. Error/cancel paths.
- **Disabled:** `opacity-50 pointer-events-none`. No style distinction beyond opacity.

### Upload Zone
- **Shape:** 2px radius. 1px border `border-accent-blue/40`. Background `bg-surface`.
- **Interior:** Flat icon (Lucide `Upload`, 24px, `text-accent-blue`), one-line instruction in Rajdhani Title, one-line hint in Roboto Body.
- **ASCII corner brackets** via `::before`/`::after` pseudo-elements: `⌐ ¬ └ ┘` in `text-accent-blue`, `text-sm`, positioned at corners with absolute placement.
- **Hover:** `border-accent-blue box-shadow: 0 0 12px rgba(63,200,224,0.35)`. Transition 150ms.
- **Drag-over:** Same as hover plus `bg-surface-alt`.
- **Active (file accepted):** Icon switches to Lucide `CheckCircle`, border color `#4cde5a`, text `#4cde5a`.
- **Error (wrong file type):** Border and text `#e03030`. `role="alert"` copy below zone.

### Results Table
- **Structure:** Semantic `<table>` via shadcn Table component. `<thead>` sticky.
- **Headers:** Rajdhani Bold 700, `text-accent-blue`, `text-xs tracking-widest uppercase`. Sort icon: Lucide `ArrowUpDown`, 12px, `text-text-muted`.
- **Row background:** Even rows `bg-bg`, odd rows `bg-surface-alt`. Very subtle — not high contrast.
- **Item name cell:** IBM Plex Mono 400, `text-text-primary`.
- **Ducat value cell:** IBM Plex Mono 500, `text-token-gold`. Right-aligned.
- **Verdict cell:** Badge component (see Verdict Badges below). Centered.
- **High-value SELL rows:** `bg-status-success/5` row tint ONLY — no left-border side stripe (impeccable absolute ban on `border-left` > 1px as colored accent). Verdict badge in ACTION cell carries the verdict signal alongside the row tint.
- **Hover row:** `hover:bg-surface` transition 80ms.
- **Sort click:** Column header active state: `text-text-primary`. Sorted direction indicator: filled arrow.
- **Mobile (< 768px):** Table collapses to card layout — one card per item, vertical stacking of label/value pairs.

### Verdict Badges
- **Shape:** 1px radius. Never pill-shaped.
- **SELL:** `bg-status-success/12 text-status-success border border-status-success/30 font-heading text-xs tracking-widest uppercase`.
- **KEEP:** `bg-text-secondary/10 text-text-secondary border border-text-secondary/20 font-heading text-xs tracking-widest uppercase`.
- **CONSIDER:** `bg-status-warning/12 text-status-warning border border-status-warning/30 font-heading text-xs tracking-widest uppercase`.
- **Text label always present.** Color is never the sole indicator. All three badges carry the text string AND a distinct border-color. Screen readers announce the text directly.

### Status Indicators (Async States)
- **Analyzing (in-progress):** Scan-sweep bar — 2px height, `bg-accent-blue`, `width: 0% → 100%` animation `400ms linear` playing once. Below the upload zone. `role="progressbar" aria-live="polite"` on container.
- **Success (table ready):** Scan sweep completes → results table fades in at `opacity: 0 → 1` over 200ms. No separate success banner needed — the table IS the success state.
- **Error:** `role="alert"` `aria-live="assertive"`. Red border on the upload zone. Error text in Roboto Body, `text-status-error`, icon Lucide `AlertTriangle` 16px prepended.
- **Empty (no items recognized):** Full-width message block in the results area. IBM Plex Mono, `text-text-muted`, text "NO ITEMS IDENTIFIED: CHECK IMAGE QUALITY". Lucide `FileSearch` icon above.
- **Skeleton (pending row data):** `animate-pulse` blocks using `bg-surface-alt`, height matching actual row, one per expected row slot.

### Cards / Containers
- **Corner style:** 2px radius (matches `--radius: 0.125rem` → `radius-lg = 0.125rem`, so effectively 2px).
- **Background:** `bg-surface` (`#1a1d26`).
- **Border:** `border border-border` = `border border-[rgba(63,200,224,0.25)]`.
- **Scanline texture:** `::before` with `repeating-linear-gradient(transparent 0, transparent 1px, rgba(0,0,0,0.07) 1px, rgba(0,0,0,0.07) 2px)` at 100% width/height, `pointer-events: none`, limited to panel-scoped use (not full viewport).
- **Internal padding:** `p-4` (16px) for most panels, `p-6` (24px) for upload zone.

### Navigation
- **Minimal header bar.** Logo (SVG, 32px), product name "DUCAT LENS" in Rajdhani 700, `text-text-primary`, `tracking-widest`. Right-aligned: placeholder for future nav items.
- **Background:** `bg-surface border-b border-border`. Height `h-12`.
- **No tabs, no sidebar, no mega-menu.** Single-surface tool. Navigation chrome is minimal by design.

## 6. Do's and Don'ts

### Do:
- **Do** use `border-radius` of 2px or less everywhere. `--radius: 0.125rem` is the system root. Period UI was boxy.
- **Do** keep `#3fc8e0` (accent blue) as the sole interactive UI color. Use it for borders, focus rings, scan animations, and hover states. One voice.
- **Do** use `#c8a84b` (Orokin gold) exclusively for the Ducats column values and SELL verdict tints. Nowhere else.
- **Do** render all numeric data in IBM Plex Mono, right-aligned in table cells.
- **Do** place ASCII corner brackets (`⌐ ¬ └ ┘`) on the upload zone via CSS pseudo-elements. Period-correct, not Orokin filigree.
- **Do** scope scanline textures to panel `::before` pseudo-elements only, at 5-8% opacity. Never full-viewport.
- **Do** gate all animation behind `@media (prefers-reduced-motion: reduce)`. Scan sweeps and flickers become instant state changes in reduced-motion mode.
- **Do** provide text labels on every verdict badge alongside color. SELL / KEEP / CONSIDER in text, always.
- **Do** use `role="alert"` and `aria-live="polite"` on status indicator containers.
- **Do** ensure touch targets are minimum 44px height even for desktop-primary interactions.
- **Do** load Google Fonts via `<link rel="preconnect">` in BaseLayout — never `@import` inside CSS.

### Don't:
- **Don't** use generic SaaS "modern minimalism": no rounded corners (`border-radius > 4px`), no pastel accents, no cream backgrounds, no friendly sans-serif headlines. This is not a productivity app for knowledge workers. (PRODUCT.md anti-reference, verbatim.)
- **Don't** use the classic Orokin aesthetic: no gold filigree borders, no white voids, no energy-field glow borders. Orokin is pre-1999 in-world. (PRODUCT.md anti-reference, verbatim.)
- **Don't** use marketing landing page register: no hero sections, no scroll-driven reveal animations over 0.3s, no social proof blocks. This is a tool; register is product. (PRODUCT.md anti-reference, verbatim.)
- **Don't** use mobile-first card grids as a default layout. Desktop-first; the screenshot workflow is a desktop action. (PRODUCT.md anti-reference, verbatim.)
- **Don't** use cute or playful copy. Errors read as system alerts, labels read as field headings. The atmosphere is decay, punk resistance, grit. (PRODUCT.md anti-reference, verbatim.)
- **Don't** use glassmorphism or frosted-panel aesthetics. Hard prohibition per impeccable design law and PRODUCT.md. (PRODUCT.md anti-reference, verbatim.)
- **Don't** use gradient text as a default treatment. Heading text is flat `#e8eaf0`. No gradient on any text element. (PRODUCT.md anti-reference, verbatim.)
- **Don't** use `#000000` or `#ffffff`. Background is `#0d0f14`; text is `#e8eaf0`. Pure black/white are not in the palette.
- **Don't** use em dashes in any UI copy string. Use a hyphen or restructure the sentence.
- **Don't** use `border-left` color stripes thicker than 2px. The SELL row accent is 2px; that is the maximum.
- **Don't** run scan-sweep or flicker animations on page load unconditionally. They are a response to user action (file upload, results reveal), not decorative looping background effects.
- **Don't** use full-viewport CRT scanline overlays. Scanlines are panel-scoped, opacity-limited, and off on `body`.
- **Don't** reach for a modal as the first solution for any interaction. Status feedback, error states, and confirmations belong inline or in the result surface, not in an overlay.
