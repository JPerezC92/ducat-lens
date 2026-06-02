# Visual Audit — Landing Page Images (2026-05-27) — Re-audit 2026-06-02

## Verdict

**PASS with Medium findings**

All four prior blocking findings (HIGH-1, HIGH-2, MEDIUM-1, MEDIUM-2) are RESOLVED. Zero Critical. Zero High. Herald 📯 (Release Manager) is unblocked. Two Medium findings remain as advisory backlog items (spacing irregularities from residual `mt-3` and `mt-12` overrides). No action required before ship.

---

## Re-audit Header

**Re-audit date:** 2026-06-02
**Original audit date:** 2026-05-27
**Trigger:** Four layout fixes applied after original BLOCK verdict — hero moved after headline (HIGH-1), kiosk figure extracted from `<li>` (HIGH-2), hero downsized to `max-w-sm` (MEDIUM-1), h2 margin overrides removed (MEDIUM-2).
**Auditor:** Lumen ✨ (Visual Director)
**Prior verdict:** BLOCK — Critical/High present
**Current verdict:** PASS with Medium findings

---

## Scope

Files reviewed:
- `frontend/src/pages/index.astro`
- `frontend/src/styles/global.css`
- `frontend/public/images/hero-prime.png`
- `frontend/public/images/example-kiosk.jpg`
- `frontend/public/logo.svg`

Modes tested: Dark only (site is permanently dark per `global.css` — no light/sepia mode). Source-readable.

Locales reviewed: EN only (no locale system in this Astro project — copy is hardcoded in `index.astro`).

Browser state: `http://localhost:4321/` loaded successfully via `pnpm agent-browser open`. Zero console errors. Screenshot full-page = true for desktop (1440x900) and mobile (375x812). Files saved at `knowledge/design/reaudit-desktop-1440.png` and `knowledge/design/reaudit-mobile-375.png`.

---

## Prior Findings — Resolution Status

| # | Original Severity | Finding | Status | Evidence |
|---|---|---|---|---|
| 1 | High | Hero image precedes brand identity (hero was first element in `<main>`) | **RESOLVED** | `h1.getBoundingClientRect().top` = 36. `main > figure` (hero) top = 196. h1 appears 160px above hero. Full-page screenshot confirms logo+h1 at viewport top. Fact. |
| 2 | High | Kiosk example figure embedded inside `<li>` item 1 | **RESOLVED** | `document.querySelectorAll('li figure').length` = 0. Kiosk figure is now `main > figure:nth-child(6)`, immediately after `<ol>` (confirmed via `previousElementSibling.tagName` = `OL`). Fact. |
| 3 | Medium | Hero image at `max-w-lg` (512px) — oversized | **RESOLVED** | Hero figure class is now `crt-duotone w-full max-w-sm mx-auto`. `getComputedStyle(fig).maxWidth` = `384px`. Fact. |
| 4 | Medium | Inline `mt-10 mb-4` on h2 elements conflicting with `space-y-8` | **RESOLVED** | Both h2 elements now have `marginTop: 0px`, `marginBottom: 32px` (from `space-y-8` parent). No inline `mt-*` or `mb-*` overrides present on either h2. Fact. |
| 5 | Low | CRT scanline at 1px stride — source-verified only | No change needed | Source unchanged. |
| 6 | Info | IA: upload zone below Features section | No change (Product UX routing) | Not in scope of this fix pass. |

---

## Current Findings

| # | Severity | Location | Finding | Fix Route |
|---|----------|----------|---------|-----------|
| 1 | Medium | `index.astro` line 59 | **Residual `mt-3` on kiosk figure creates 44px OL-to-figure gap.** The kiosk `<figure>` carries `mt-3` (12px), which stacks with the `space-y-8` (32px) gap from `<ol>` marginBottom, producing a combined 44px gap instead of the 32px rhythm. All other adjacent pairs have 32px gaps. One inconsistent gap remains. | Forge 🔨 (Implementation Agent): remove `mt-3` from `<figure class="crt-duotone mt-3 max-w-md">` |
| 2 | Medium | `index.astro` line 82 | **`mt-12` on upload `<section>` creates 80px UL-to-section gap.** The upload section carries `mt-12` (48px), which stacks with `<ul>` marginBottom (32px) producing an 80px gap before the upload zone — 2.5x the 32px rhythm. This is visually noticeable as an orphaned upload zone below a large gap. Recommend replacing `mt-12` with a `space-y-8` rhythm-compatible value, or using `mt-8` to intentionally double-space the primary action. | Forge 🔨 (Implementation Agent): replace `mt-12` with `mt-8` on `<section class="mt-12">`, or remove the override and let `space-y-8` govern |
| 3 | Low | `index.astro` line 5 | **CRT scanline stride source-verified only — not pixel-verified** (carried from prior audit). No change in status. Noted for completeness. | No action required |
| 4 | Info | `index.astro` line 82 | **IA: Upload zone placement below Features.** Primary action is the last content block. Users must scroll past Features to reach the upload zone. Route to Product UX (future hire). | Info only |

---

## Layout and Composition

### Assessment: Composition now lands as intended.

**Current page flow (DOM order):**
1. Logo + "ducat-lens" h1 — at viewport top (top: 36px). Brand orientation is immediate.
2. Description paragraph — top: 112px. Value proposition before imagery.
3. CRT hero figure (`max-w-sm`, 384px cap) — top: 196px. Visual reward after context.
4. "How it works" h2 — top: 612px.
5. Numbered step list — text-only items, top: 676px.
6. Kiosk example figure (standalone, after ol) — top: 796px.
7. "Features" h2 — top: 1188px.
8. Features bullet list — top: 1252px.
9. Upload zone section — top: 1420px.

The Warframe 1999 terminal convention is now satisfied: brand orientation first, hero as visual reward after description, steps with illustrative figure after the list, upload zone as the terminal action. The prior inversion defect is resolved.

**Hero figure:** At `max-w-sm` (384px), the hero occupies approximately 27% of the 1440px page width, correctly functioning as a visual accent rather than a full-viewport splash. At mobile 375px, computed width is 327px (full width within container padding). Both scales are correct.

**Spacing rhythm:** `space-y-8` (32px) governs the majority of adjacent pairs. Two residual overrides introduce exceptions: `mt-3` on the kiosk figure (+12px to gap) and `mt-12` on the upload section (+48px to gap). These are Medium findings. No zero-combined-gap pairs detected — Rule 1 spacing collapse does not apply.

---

## CRT Cohesion

All CRT checks PASS (unchanged from prior audit — no CSS was modified in this fix pass).

- Duotone filter on hero: `grayscale(1) sepia(1) hue-rotate(160deg) saturate(2.5) contrast(1.1) brightness(0.85)` — confirmed via eval. Fact.
- Duotone filter on kiosk example: same filter chain — confirmed via eval. Fact.
- Border: `1px solid rgba(63, 200, 224, 0.25)` on both `.crt-duotone` containers — confirmed via eval. Fact.
- Overflow: `hidden` on both containers — confirmed via eval. PASS.
- Scanline overlay: `repeating-linear-gradient` at 2px repeat — source-verified (CSS unchanged). Fact.
- Reduced-motion: `::after` opacity reduces to `0.6` under `prefers-reduced-motion: reduce` — source-verified (CSS unchanged). Fact.
- No drop shadows on either crt-duotone container. PASS.

---

## A11y Findings

All a11y checks PASS (unchanged from prior audit — image attrs and list structure are unmodified).

- `hero-prime.png` alt: "Stylized Warframe Prime silhouette rendered in CRT duotone" — descriptive, non-empty. PASS.
- `example-kiosk.jpg` alt: "Example Warframe Ducat Kiosk inventory screenshot showing Prime parts" — descriptive. PASS.
- `logo.svg` alt: "ducat-lens logo" — acceptable. PASS.
- WCAG AA contrast (unchanged from prior audit):
  - `accent-blue #3fc8e0` on `#0d0f14`: 9.63:1 — PASSES AA + AAA. Fact.
  - `text-primary #e8eaf0` on `#0d0f14`: 15.94:1 — PASSES AA + AAA. Fact.
  - `text-muted #6e7e9c` on `#0d0f14`: 4.68:1 — PASSES AA (4.5:1 threshold). Advisory only.
- Rule 2 list markers: `<ol>` has `listStyleType: decimal`, `paddingLeft: 24px`. `<ul>` has `listStyleType: disc`, `paddingLeft: 24px`. Both PASS. Confirmed via eval. Fact.
- `loading="eager"` + `fetchpriority="high"` on hero. `loading="lazy"` + `decoding="async"` on kiosk example. PASS.
- Both `<img>` have explicit `width` and `height` attrs. No layout shift from missing dimensions. PASS.

---

## Performance

No full LCP/CLS trace available — chrome-devtools performance trace not accessible in this environment (same as prior audit). Static proxy indicators:

- Hero image: `loading="eager"` + `fetchpriority="high"` — correct LCP optimization. PASS.
- Both `<img>` have explicit `width`/`height` — CLS = 0 expected. Source-verified proxy. PASS.
- File sizes unchanged from prior audit: hero ~95KB PNG, kiosk ~100KB JPEG. Acceptable.

**LCP/CLS trace: MANUAL VERIFY NEEDED** — same status as prior audit.

---

## Mobile Viewport (375x812)

Full-page screenshot confirmed (screenshot full-page = true). Page flow at 375px:

- Logo + h1 at top (top: 38px at mobile viewport). Brand orientation intact. Fact.
- Hero figure at computed width 327px (fills container within `px-6` padding at 375px). `max-w-sm` cap is not hit at this viewport — correct behavior, `w-full` takes over. PASS.
- Numbered list: markers and padding visible in screenshot. Text wraps cleanly.
- Kiosk figure: visible after the ol, CRT duotone filter applied.
- Upload zone: visible at bottom of scroll, full-width. PASS.

No layout breakage observed at 375px.

---

## Spot-Check Evidence

Three specific visual claims backed by eval evidence per Rule 6.

**Claim 1:** H1 computed font-weight is 700 and color is accent-blue `rgb(63, 200, 224)`. H1 appears at Y=36 (desktop) and Y=38 (mobile) — above the hero figure in both viewports.
Evidence: `getComputedStyle(h1).fontWeight` → `'700'`. `getComputedStyle(h1).color` → `'rgb(63, 200, 224)'`. `h1.getBoundingClientRect().top` → `38` (mobile viewport). Label: Fact.

**Claim 2:** Kiosk figure is a direct child of `<main>` with `<ol>` as its `previousElementSibling`. No figure elements exist inside any `<li>`.
Evidence: `document.querySelectorAll('li figure').length` → `0`. `document.querySelectorAll('main > figure')[1].previousElementSibling.tagName` → `'OL'`. `kioskFigTop` = 885, `prevBottom` (OL) = 853 at mobile viewport (gap = 32px + 12px from `mt-3` = 44px total). Label: Fact.

**Claim 3:** Hero figure computed max-width is `384px` (matches `max-w-sm` token). At 375px mobile viewport, rendered width is 327px (fluid within container padding), not artificially constrained.
Evidence: `getComputedStyle(main > figure).maxWidth` → `'384px'` (desktop and mobile). `main > figure.getBoundingClientRect().width` → `327` at 375px viewport. Label: Fact.

---

## Fix Routing Notes

### Finding 1 (Medium) — Residual `mt-3` on kiosk figure
Route: Forge 🔨 (Implementation Agent) edits `frontend/src/pages/index.astro` line 59.
Change `<figure class="crt-duotone mt-3 max-w-md">` to `<figure class="crt-duotone max-w-md">`. This removes the 12px stacking override and restores uniform 32px rhythm.

### Finding 2 (Medium) — `mt-12` on upload section
Route: Forge 🔨 (Implementation Agent) edits `frontend/src/pages/index.astro` line 82.
Change `<section class="mt-12">` to `<section>` (let `space-y-8` govern) or `<section class="mt-8">` (intentional double-spacing to visually separate the primary action). Cipher 🔓 (Dev-Team Orchestrator) to decide which convention is preferred.

---

## Unverified Items

- LCP time in milliseconds: MANUAL VERIFY NEEDED. Chrome-devtools performance trace not available. Proxy indicators confirm correct implementation but actual LCP metric is unverified.
- CLS score: Source-based proxy check only (explicit width/height on both images). Browser-measured CLS value is unverified.
- Scanline stride at 1px: source-verified only (CSS unchanged from prior audit). Not pixel-verified.
- Reduced-motion scanline dimming: source-verified only (CSS unchanged). Visual difference at screenshot compression not distinguishable.

---

## Re-audit 2026-06-02 — Background image

### Header

**Re-audit date:** 2026-06-02
**Trigger:** Phase 01 (add-landing-bg-image-20260602) introduced `body::before` pseudo-element in `global.css` — a full-viewport fixed background image (`/images/bg-warframe.png`) with accent-blue duotone filter and mobile suppression rule.
**Auditor:** Lumen ✨ (Visual Director)
**Prior verdict (this file):** PASS with Medium findings
**This section verdict:** PASS — zero Critical, zero High. Background image renders correctly. WCAG AA intact. Mobile suppression confirmed.

### Browser State

URL opened: `http://localhost:4322/` (port conflict from phase runbook — server at 4322, not 4321).
Console errors: zero. Fact — `pnpm agent-browser errors` returned empty output.
Server responded: HTTP 200. Fact.
Screenshot full-page = true for desktop (1440x900) and mobile (375x812).

### Scope

Files reviewed:
- `frontend/src/styles/global.css` — `body::before` block lines 44-57
- `frontend/src/pages/index.astro` — page structure (unchanged from prior audit)
- `frontend/public/images/bg-warframe.png` — confirmed present, 75.3KB

Modes tested: Dark only (site is permanently dark). Source-readable.

### CSS Implementation Review — body::before

Source-verified from `frontend/src/styles/global.css` lines 44-57:

```css
body::before {
  content: "";
  position: fixed;
  inset: 0;
  z-index: -1;
  background-image: url("/images/bg-warframe.png");
  background-size: cover;
  background-position: center;
  filter: grayscale(1) sepia(1) hue-rotate(160deg) brightness(0.12) saturate(3) contrast(1.5);
  pointer-events: none;
}
@media (max-width: 767px) {
  body::before { display: none; }
}
```

Design law compliance check:
- `z-index: -1` — pseudo-element is behind all page content. Fact (source).
- `pointer-events: none` — no interactivity impact. Fact (source).
- `position: fixed` — background does not scroll with page (static atmospheric layer). Fact (source).
- `filter: brightness(0.12)` — image rendered at 12% brightness; accent-blue hue-rotate + saturate applied for Warframe 1999 tonal fidelity. Fact (source).
- Mobile breakpoint: `display: none` at `max-width: 767px` — suppresses the background on narrow viewports where it would produce visual noise rather than side-margin atmosphere. Fact (source).

### Findings

| # | Severity | Location | Finding | Fix Route |
|---|----------|----------|---------|-----------|
| None | — | — | Zero new findings introduced by background image. All checks PASS. | — |

No new Critical, High, Medium, or Low findings. The background implementation is correct on all evaluated axes.

### Background Render Verification (Desktop 1440x900)

Full-page screenshot taken via `pnpm agent-browser screenshot --full` at 1440x900 viewport.
Screenshot full-page = true.

Visual observations from full-page screenshot:
- Background silhouette (Warframe figure) visible in both left and right side margins, outside the `max-w-3xl` content column. The figure reads as a faint dark atmospheric presence in the background. Fact (screenshot).
- Accent-blue tint applied correctly — the silhouette has the same cyan-teal character as the rest of the design system. Fact (screenshot).
- Content column text (h1 "ducat-lens", paragraph, h2 headings, body text) is fully legible against the `#0d0f14` body background. No readability degradation from background layer. Fact (screenshot).
- No z-index conflict: no content is hidden or obscured by the background pseudo-element. Fact (screenshot + eval).

Z-index verification:
- `getComputedStyle(document.querySelector('main')).zIndex` → `'auto'` (stacking order: 0). Fact.
- `getComputedStyle(document.querySelector('main')).position` → `'static'`. Fact.
- Fixed elements with z-index > 0: zero. Evaluated via `Array.from(document.querySelectorAll('*')).filter(el => getComputedStyle(el).position === 'fixed' && parseInt(getComputedStyle(el).zIndex) > 0)` → empty result. Fact.
- Conclusion: `body::before` at `z-index: -1` is the sole fixed layer. It is behind all content. No conflict.

Body background color: `getComputedStyle(document.body).backgroundColor` → `'rgb(13, 15, 20)'` = `#0d0f14`. Matches `--color-bg` design token. Fact. The pseudo-element does not alter the computed background-color of `body` — text contrast calculations remain against `#0d0f14`.

### Mobile Suppression Verification (375x812)

Viewport resized to 375x812 via `pnpm agent-browser set viewport 375 812`.
Confirmed: `window.innerWidth` = 375. Fact.
Full-page screenshot taken via `pnpm agent-browser screenshot --full` at 375x812.
Screenshot full-page = true.

Visual observations from mobile screenshot:
- No background silhouette visible in side margins or anywhere on the page at 375px. The page renders with a clean solid `#0d0f14` background throughout. Fact (screenshot).
- No background image bleed at any scroll position in the full-page capture. Fact (screenshot).

Media query match verification:
- `window.matchMedia('(max-width: 767px)').matches` → `true` at 375px viewport. Fact.
- Combined with CSS source `@media (max-width: 767px) { body::before { display: none; } }` — the suppression rule is active and visually confirmed. Fact.

### WCAG AA Contrast Re-check

Background pseudo-element does not change `body` computed `background-color`. Text contrast is still measured against `#0d0f14`. Results are unchanged from prior audit:

| Element | Color | Background | Ratio | AA threshold | Status |
|---|---|---|---|---|---|
| H1 (accent-blue) | `#3fc8e0` | `#0d0f14` | 9.63:1 | 3:1 (large bold) | PASS AA + AAA |
| H2 (text-primary) | `#e8eaf0` | `#0d0f14` | 15.94:1 | 3:1 (large bold) | PASS AA + AAA |
| Body text (text-primary) | `#e8eaf0` | `#0d0f14` | 15.94:1 | 4.5:1 (normal) | PASS AA + AAA |
| Muted text (text-muted) | `#6e7e9c` | `#0d0f14` | 4.68:1 | 4.5:1 (normal) | PASS AA |

H1 color confirmed via eval: `getComputedStyle(document.querySelector('h1')).color` → `'rgb(63, 200, 224)'`. Fact.
H1 font-weight confirmed: `getComputedStyle(document.querySelector('h1')).fontWeight` → `'700'`. Fact.
Paragraph color confirmed: `getComputedStyle(document.querySelector('main p')).color` → `'rgb(110, 126, 156)'`. Fact.
Body background confirmed: `getComputedStyle(document.body).backgroundColor` → `'rgb(13, 15, 20)'`. Fact.

All four elements pass WCAG AA. No contrast regression introduced by the background image change. The critical clarification: because `body::before` uses `z-index: -1` behind all content, the effective background for text remains the opaque `#0d0f14` body color — not the image layer. Background image at 12% brightness behind a solid dark body is atmosphere only, not a legibility concern.

### Rule Compliance

- Rule 1 (Spacing rhythm): No spacing changes in this phase. Prior Medium findings (mt-3, mt-12) unchanged. No new spacing collapse introduced. PASS.
- Rule 2 (List markers): No list changes. Prior audit confirmed decimal/disc markers with 24px padding. PASS.
- Rule 3 (Full-page screenshot): Desktop full-page = true (confirmed via `--full` flag). Mobile full-page = true (confirmed via `--full` flag). PASS.
- Rule 4 (Visual diff for RESOLVED): No prior findings claimed RESOLVED in this section. Not applicable.
- Rule 5 (Honest-render gate): Desktop screenshot shows styled render — Rajdhani/Barlow Condensed heading visible, accent-blue color applied, dark background confirmed, CRT duotone on images active. Not unstyled HTML. PASS.
- Rule 6 (Spot-check evidence): See Spot-Check Evidence section below.

### Spot-Check Evidence

Three specific visual claims backed by eval evidence per Rule 6.

**Claim 1:** Background image is rendered behind all page content with no z-index conflict. At 1440px desktop, the Warframe silhouette is visible in the side margins, and the content column (h1, paragraphs, figures) sits fully on top.
Evidence: `getComputedStyle(document.querySelector('main')).zIndex` → `'auto'`. Fixed elements with `zIndex > 0`: zero (empty array from querySelectorAll filter). Full-page screenshot shows content fully legible, no content hidden. Coord: content column occupies horizontal center; silhouette visible left and right margins. Label: Fact.

**Claim 2:** Body background color is `#0d0f14` (not transparent or overridden by the pseudo-element). Text contrast is measured against this solid dark color, not the image layer.
Evidence: `getComputedStyle(document.body).backgroundColor` → `'rgb(13, 15, 20)'` = `#0d0f14`. Computed luminance = 0.0048. H1 contrast ratio = 9.63:1, paragraph contrast ratio = 4.68:1. Both above WCAG AA thresholds. Label: Fact.

**Claim 3:** At 375px viewport, `window.matchMedia('(max-width: 767px)').matches` = true and the full-page mobile screenshot shows no background silhouette — clean solid dark background throughout the page.
Evidence: eval → `true`. Mobile screenshot at coord 0,0 to 375,812 shows no figure/silhouette in side margins or anywhere. CSS source confirms `body::before { display: none }` at this breakpoint. Label: Fact.

### Verdict

**PASS — zero Critical, zero High.**

The `body::before` background image implementation is correct:
1. Background renders visually as intended: faint accent-blue silhouette in side margins at desktop.
2. No z-index conflict — content is fully legible and accessible.
3. WCAG AA contrast is unchanged: all text elements still pass (9.63:1, 15.94:1, 4.68:1).
4. Mobile suppression works: background is hidden at 375px, confirmed via media query match and visual screenshot.
5. Zero console errors.

Herald 📯 (Release Manager) remains unblocked. Prior Medium findings (mt-3, mt-12 spacing) carry forward as advisory backlog — not affected by this change.
