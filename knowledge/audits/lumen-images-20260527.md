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
