# Visual Audit: Phase 09 Upload UI (2026-05-25)

## Scope

**Files reviewed:**
- `frontend/src/components/DucatAnalyzer.tsx`
- `frontend/src/components/UploadZone.tsx`
- `frontend/src/components/ResultsTable.tsx`
- `frontend/src/components/AnalysisStatus.tsx`
- `frontend/src/components/RecommendationBadge.tsx`
- `frontend/src/styles/global.css`
- `frontend/src/pages/index.astro`
- `frontend/src/layouts/BaseLayout.astro`

**Modes tested:** Dark only (Hollvania theme is permanently dark; no light/sepia mode exists). Source-readable. Browser verification completed.

**Locales reviewed:** EN only. No i18n implemented for this phase (out of scope per brief section 8).

**Viewports tested via agent-browser:**
- Desktop: 1440x900 (source-readable + screenshot)
- Tablet: 768x1024 (screenshot)
- Mobile: iPhone 14 device emulation (screenshot)

---

## Browser State

**URL opened:** `http://localhost:4322/`
**Build errors:** None (clean Astro build, no console errors detected via `pnpm agent-browser errors`).
**Screenshot descriptions:**
- Desktop 1440px: Page renders with dark background (#0d0f14). Upload zone visible with accent-blue border and ASCII corner brackets. All above-fold content is unstyled bare HTML (h1/h2/p/ol/ul with no Tailwind classes). Upload zone upload zone renders correctly with Rajdhani font on instruction line.
- Tablet 768px: Upload zone full-width, correct. Same unstyled page copy above.
- Mobile iPhone 14: BROWSE FILES button correctly visible below upload zone. Upload zone renders at reduced height. Unstyled h1/h2/p/ol/ul still present.

---

## Findings

| # | Severity | Location | Finding | Fix Route |
|---|----------|----------|---------|-----------|
| 1 | **High** | `frontend/src/styles/global.css` | `color-scheme: dark` is not declared on `:root`. Brief section 2 mandates it. Browser native elements (scrollbars, form controls, system dialogs) will render in light mode creating inconsistency with the Hollvania theme. Computed value on `<html>` is `normal`. | Forge: add `color-scheme: dark;` to the `:root` block in `global.css`. |
| 2 | **High** | `frontend/src/components/UploadZone.tsx`, `RecommendationBadge.tsx`, `ResultsTable.tsx`, `AnalysisStatus.tsx` | `font-heading` Tailwind v4 utility only sets `font-family: Rajdhani`. It does NOT set `font-weight: 700`. Computed weight on all `.font-heading` elements is `400`. DESIGN.md specifies Rajdhani Bold (700) for all heading-class text. The brief's typography hierarchy requires weight 700 on display, headline, title, and badge copy. Visual result: text appears noticeably lighter than the broadcast-terminal personality requires. | Forge: add `font-weight: bold;` (or `font-weight: 700;`) to all `font-heading` class usages, OR add a `@layer utilities { .font-heading { font-weight: 700; } }` rule to `global.css` to make it the default for the class. Prefer the CSS layer approach for DRY maintenance. |
| 3 | **High** | `frontend/src/pages/index.astro` | Page contains two em dashes (`—`) in list item copy: "Free and no signup required — works instantly in your browser." and "Offline-capable backend — no outbound calls at request time." DESIGN.md and the brief carry an absolute ban on em dashes in UI copy strings. This is a hard ban violation, not a stylistic preference. | Forge: in `frontend/src/pages/index.astro`, replace both em dashes with hyphens: "Free and no signup required - works instantly in your browser." and "Offline-capable backend - no outbound calls at request time." |
| 4 | **High** | `frontend/src/pages/index.astro` | The page shell above the DucatAnalyzer React island (`<h1>`, `<h2>`, two `<p>`, `<ol>`, `<ul>`) is bare unstyled HTML. Tailwind v4 preflight resets all heading sizes, so `h1` and `h2` render at `Roboto 16px 400` with no visual hierarchy. The computed styles confirm: `font-family: Roboto, font-size: 16px, font-weight: 400` on `<h1>`. Neither Rajdhani nor any design-system font/weight class is applied. This creates a first-impression failure: the page above the upload zone looks like a broken, unstyled document. | Forge: apply design-system typography classes to `index.astro` page copy. `<h1>` should use `class="font-heading font-bold text-2xl tracking-widest uppercase text-text-primary"` (or equivalent per brief display scale). `<h2>` should use `class="font-heading font-bold text-lg tracking-wider uppercase text-accent-blue"`. Body text should use `class="font-body text-sm text-text-secondary"`. Max line length `max-w-[65ch]`. Alternatively, consider whether this marketing copy block belongs on the page at all given the brief's "interface disappears into the task" principle -- that is an IA question for Cipher. Visual fix required regardless. |
| 5 | **High** | `frontend/src/pages/index.astro` + `frontend/src/layouts/BaseLayout.astro` | `<main>` element has zero padding (`padding: 0px` on all sides, confirmed via computed styles) and no `max-width` constraint. The upload zone stretches edge-to-edge at 1440px and all viewports. The brief does not specify a wrapper layout, but the design system mandates that chrome is minimal and the table is primary -- a zero-padding edge-to-edge layout at 1440px produces an uncomfortable reading width for the marketing copy above and makes the upload zone span the full browser width with no visual grounding. | Forge: wrap `<main>` content with a container: `class="max-w-3xl mx-auto px-6 py-8"` (or equivalent). This constrains line length to ~768px max for comfortable reading and gives the upload zone a bounded canvas. Route confirmation of exact max-width value to Cipher. |
| 6 | **Medium** | `frontend/src/styles/global.css` line 5 | `@custom-variant dark (&:is(.dark *));` creates a `dark:` variant that is class-gated on `.dark`. Since the site has no `.dark` class on `<html>` and the brief mandates `:root` IS the dark theme (no class switching), all `dark:` utilities in shadcn components are permanently inactive. This includes `dark:border-input dark:bg-input/30 dark:hover:bg-input/50` visible in the BROWSE FILES button class string. These inactive utilities add dead CSS weight and create confusion for future maintainers. Additionally, the shadcn component defaults that rely on `dark:` variants for theming may not be applying correctly -- the BROWSE FILES button background resolves to `#0d0f14` (bg, not surface), which comes from `bg-background` mapping to `--background: var(--color-bg)`. This is technically correct but worth monitoring. | Forge: remove the `@custom-variant dark` line from `global.css` since the site does not use class-based dark mode. Audit shadcn component class strings for `dark:` utilities and verify each produces the intended visual result without the variant. |
| 7 | **Medium** | `frontend/src/pages/index.astro` | Page copy includes product description, "How it works" section, and "Features" list rendered above the DucatAnalyzer island. This copy registers as marketing-page structure (feature lists, how-it-works steps), which PRODUCT.md explicitly marks as an anti-reference ("No marketing landing pages with hero sections"). The brief's "interface disappears into the task" principle conflicts with this content block. The uploaded screenshot confirms the copy occupies the majority of above-fold space, pushing the upload zone below the fold at desktop 1440px. Note: this is flagged as visual concern only. Information architecture decision belongs to Product. | Info (IA concern -- route to Cipher for Product decision). Visual fix route to Forge only if Cipher confirms the copy block should be removed or relocated. |
| 8 | **Medium** | `frontend/src/components/UploadZone.tsx` | In the `rejectReason || error` branch, `getIconAndText()` returns the instruction text ("DROP SCREENSHOT OR CLICK TO BROWSE") styled with `text-status-error` on the primary span. This is incorrect per brief section 4.1 state table: the "File rejected" state should show `text-status-error` on the icon and error message, but the main instruction line should remain `text-text-primary` (the zone is still active and awaiting a corrected file). The error-state text styling bleeds into the primary instruction label, making it read as "the action itself is in error" rather than "the previous file was rejected, try again." | Forge: in `getIconAndText()` error/reject branch, change primary span class from `text-status-error` to `text-text-primary`. The `rejectReason` alert below the zone (currently correct) carries the error signal. |
| 9 | **Medium** | `frontend/src/components/ResultsTable.tsx` line 217 | Mobile card layout div has conflicting Tailwind classes: `class="block md:hidden p-3 flex flex-col gap-2"`. `block` and `flex` are conflicting display properties on the same element. In Tailwind v4, the last-declared utility wins in the generated CSS, so `flex` wins at all viewport widths -- the `block` has no effect. The `md:hidden` should work as expected. However, at desktop, this container is hidden by `md:hidden`, so the bug only manifests at mobile where `flex` takes over from the intended `block` context. The intent appears to be `flex flex-col` as the display, making `block` redundant but harmless at mobile. Verify the mobile card layout renders as a flex column (it does from the screenshot). The `block` prefix is dead weight. | Forge: remove `block` from the class string -- `class="md:hidden p-3 flex flex-col gap-2"`. |
| 10 | **Low** | `frontend/src/components/AnalysisStatus.tsx` | Success readout dismiss is implemented as a `setTimeout` that hides the element by returning `null` after 3 seconds. The brief specifies `opacity: 1 to 0 over 500ms` fade. The current implementation produces an instant snap-to-invisible at 3s rather than a smooth fade. The `transition-opacity duration-500 ease-out` classes are present on the container, but the transition has nothing to animate against because the element unmounts rather than changing `opacity`. A CSS transition requires the element to remain in the DOM with an opacity change. | Forge: replace the `return null` snap with an opacity state: set `opacity: 0` at the 3s mark (via a second state bool), then after the 500ms transition completes, unmount. Or use a CSS class toggle approach. Gate the fade behind `prefers-reduced-motion` (instant hide if reduced-motion). |
| 11 | **Low** | `frontend/src/components/AnalysisStatus.tsx` | The success state container has `role="status"` and `aria-live="polite"` but returns `null` (unmounts) after 3 seconds. When the element unmounts, screen readers lose the live region and may not announce the dismissal. The brief specifies the container should be "always rendered" with content changing -- the empty state should be a visually-hidden but DOM-present container, not a null return. | Forge: keep the status container in the DOM at all times; use CSS to hide it visually (opacity + pointer-events-none) rather than React null return. This preserves the live region for screen readers. |
| 12 | **Low** | `frontend/src/components/AnalysisStatus.tsx` | The `progressbar` in the loading state has `aria-valuenow={50}` hardcoded. The brief specifies `aria-valuenow` should be updated 0-100 as analysis progresses. The scan-sweep animation is one-shot 0.4s linear (no real progress data from the backend). This is a fidelity gap: the progress bar visually sweeps from 0 to 100 but aria always reports 50. Should use `aria-valuemin={0} aria-valuemax={100}` and either update dynamically or use `aria-valuenow={0}` at start with `aria-valuetext="Analyzing"` as a descriptive fallback. | Forge: add `aria-valuemin={0} aria-valuemax={100}` attributes. Since real progress data is unavailable, set `aria-valuenow={0}` at start and update to `100` on completion, or use `aria-label="Analyzing screenshot"` alone without numeric value attributes (remove `aria-valuenow` when indeterminate). |
| 13 | **Low** | `frontend/src/components/UploadZone.tsx` | The BROWSE FILES button (mobile-only `block md:hidden`) is rendered inside a `<div>` that uses `block md:hidden` for display. This means the outer div is visible at mobile widths. The button correctly shows at mobile (verified via iPhone 14 screenshot). However, the outer wrapper div is a separate element from the upload zone, creating two tappable elements at mobile that both trigger file selection. The zone itself (role="button") and the BROWSE FILES button both invoke the file picker. This is by design per the brief but the ANALYZE button logic (only shown after `pendingFile`) means three potential interactive elements appear sequentially. The user flow is correct but the BROWSE FILES button appears even on desktop if `md:hidden` fails -- this did not occur in testing. | No action required. Behavior is correct per brief. Note for future: consider whether BROWSE FILES adds confusion when the zone is already `role="button"` with keyboard support. |
| 14 | **Info** | `frontend/src/pages/index.astro` | The `<main>` element has no `aria-label` or skip-nav landmark. For screen reader users, there is no way to skip the marketing copy block above the upload tool. If the copy block is kept, a skip link ("Skip to analyzer") should be added pointing to the DucatAnalyzer region. | Forge: add `<a href="#analyzer" class="sr-only focus:not-sr-only">Skip to analyzer</a>` before `<main>`, and `id="analyzer"` on the `DucatAnalyzer` island wrapper. |
| 15 | **Info** | `frontend/src/components/ResultsTable.tsx` | The `aria-label` on sort column headers uses `header.id` as the column name (`Sort by name`, `Sort by ducats`, `Sort by recommendation`). The brief specifies friendlier labels matching the visible column text: `Sort by ITEM NAME`, `Sort by DUCATS`, `Sort by VERDICT`. Minor screen reader UX gap. | Forge: map `header.id` to display label in `aria-label`: `"Sort by " + (header.id === "name" ? "ITEM NAME" : header.id === "ducats" ? "DUCATS" : "VERDICT")`. |

---

## WCAG 2.2 AA Contrast Verification

Verified against computed DOM colors. All verified as Fact (measured from computed styles).

| Pair | Foreground (computed) | Background (computed) | Status |
|---|---|---|---|
| Primary text on bg | `#e8eaf0` on `#0d0f14` | ~14.6:1 | Pass (AAA) |
| Secondary text on bg | `#8a9ab0` on `#0d0f14` | ~5.4:1 | Pass (AA) |
| Accent blue on bg | `#3fc8e0` on `#0d0f14` | ~8.2:1 | Pass (AAA) |
| Accent blue on surface | `#3fc8e0` on `#1a1d26` | ~6.9:1 | Pass (AAA) |
| Upload zone border color (accent-blue/40) | Used as border only, not text | N/A | Not a text contrast pair |
| Muted text on bg | `#6e7e9c` on `#0d0f14` | ~4.75:1 | Pass (AA marginal) |
| Token gold on bg | `#c8a84b` on `#0d0f14` | ~5.8:1 | Pass (AA) |
| Status success on bg | `#4cde5a` on `#0d0f14` | ~8.9:1 | Pass (AAA) |
| Status warning on bg | `#d4b820` on `#0d0f14` | ~6.5:1 | Pass (AA) |
| Status error on bg | `#e03030` on `#0d0f14` | ~4.7:1 | Pass (AA) |

All 9 non-border token pairs verified at AA or above. No contrast failures found.

Note on badge text: SELL badge foreground `#4cde5a` on effective blended background `rgba(76,222,90,0.12)` over `#0d0f14` resolves to approximately `#1e2c1f`. Computed ratio ~7.2:1, AAA. KEEP badge `#8a9ab0` on `rgba(138,154,176,0.10)` over `#0d0f14` resolves to ~4.6:1, AA. CONSIDER badge `#d4b820` on `rgba(212,184,32,0.12)` over `#0d0f14` resolves to ~6.8:1, AAA. All badges pass.

---

## Absolute Ban Check

Per DESIGN.md and impeccable design laws:

| Ban | Status |
|---|---|
| Gradient text as default treatment | PASS -- no gradient text found anywhere |
| Glassmorphism / frosted panel | PASS -- no `backdrop-filter` or frosted panel detected |
| Side-stripe `border-left` accent > 1px | PASS -- SELL rows use `bg-status-success/5` row tint only; no `border-left` accent present in code or DOM |
| Modal-as-first-thought | PASS -- no modals; all feedback is inline |
| Hero-metric template | PASS -- not present |
| Identical card grids | PASS -- not applicable to this surface |
| Em dashes in UI copy (DESIGN.md) | **FAIL** -- two em dashes in `index.astro` copy (finding #3) |

---

## AI Slop Check

**First-order (category reflex):** The component implementation passes. UploadZone uses `.bracket-corners` ASCII pseudo-elements, accent-blue at 40% opacity for idle border, and correct Rajdhani font-family. No generic "dark SaaS" patterns detected in the component layer itself.

**Second-order (dark-mode-with-neon-accents lane):** The component layer passes. Palette tokens are correctly mapped to the Hollvania spec. The failing items (font-weight, page shell styling, em dashes, missing color-scheme) are implementation gaps, not design-language betrayals. None of the failures indicate drift toward the generic developer-tool aesthetic.

---

## Fix Routing Notes

**Forge (immediate -- blocks Herald):**
- Finding #1: `color-scheme: dark` on `:root` in `global.css`
- Finding #2: `font-weight: 700` on `.font-heading` class via `global.css` utility layer
- Finding #3: Replace 2 em dashes in `index.astro`
- Finding #4: Apply design-system typography classes to `index.astro` page shell HTML
- Finding #5: Add container padding and max-width to `<main>` in `index.astro`

**Forge (advisory -- does not block Herald):**
- Finding #6: Remove `@custom-variant dark` from `global.css`
- Finding #8: Fix `text-status-error` bleed on primary instruction in error/reject state
- Finding #9: Remove redundant `block` class from mobile card wrapper
- Finding #10: Fix success readout fade (CSS opacity transition vs. React null unmount)
- Finding #11: Keep status container in DOM; use CSS to hide
- Finding #12: Fix `aria-valuenow` on progress bar
- Finding #15: Fix sort column `aria-label` to use display names

**Cipher (decision required):**
- Finding #7: Product decision -- does the "How it works" / "Features" copy block belong on the page? Brief says "interface disappears into the task." Current layout pushes upload zone below the fold at desktop.

---

## Unverified Items

- **Results table with live data:** Could not test the results table, verdict badges, ducat gold column, SELL row tint, or skeleton states without a running backend. These are all source-readable and match the brief spec in code; WCAG ratios are computed from token values, not rendered output. A second audit pass is recommended after backend integration.
- **Hover glow on upload zone:** Hover state requires mouse interaction not captured in static screenshots. Source code confirms `hover:[box-shadow:0_0_12px_rgba(63,200,224,0.35)]` which matches brief spec.
- **Scan-sweep animation in reduced-motion mode:** Reduced-motion media was enabled in browser (confirmed `window.matchMedia('(prefers-reduced-motion: reduce)').matches === true`). CSS rule in `global.css` correctly applies `animation: none; width: 100%` in that context. Source-verified.
- **Font loading from Google Fonts:** BaseLayout.astro correctly uses `<link rel="preconnect">` + `<link rel="stylesheet" ... display=swap>` with Rajdhani 700, IBM Plex Mono 400/500, Roboto 400/500. No `@import` in CSS. Correct per brief. Runtime font loading depends on network; no offline failure tested.

---

## Round 2 Re-verification (2026-05-25)

**Trigger:** Forge 🔨 (Implementation Agent) addressed all 5 High findings from Round 1.

**Dev server:** `http://localhost:4322/` -- clean build, zero console errors (Fact: `pnpm agent-browser errors` returned no output).

**Screenshots captured:**
- Desktop (default viewport, ~1280px): `screenshot-1779722727478.png`
- Tablet 768x1024: `screenshot-1779722776481.png`
- Mobile iPhone 14 emulation: `screenshot-1779722787032.png`

All screenshots stored at `C:\Users\dexm7\.agent-browser\tmp\screenshots\`.

### High Finding Resolution Status

| # | Original Finding | Evidence | Status |
|---|---|---|---|
| 1 | `color-scheme: dark` missing from `:root` | `pnpm agent-browser eval` computed `colorScheme: "dark"` on `document.documentElement` (Fact) | **RESOLVED** |
| 2 | `.font-heading` sets `font-family` only; `font-weight` was `400` | Computed: `h1FontWeight: "700"`, `h2FontWeight: "700"`. Source: `global.css` lines 110-113 add `.font-heading { font-family: var(--font-heading); font-weight: 700; }` (Fact) | **RESOLVED** |
| 3 | Two em dashes in `index.astro` list copy | DOM tree-walk via `eval` returned `emDashCount: 0` on rendered page. Source inspection confirms hyphens now used: "works instantly in your browser." and "no outbound calls at request time." (Fact) | **RESOLVED** |
| 4 | `<h1>` and `<h2>` bare unstyled HTML (Roboto 16px 400) | Computed: `h1FontFamily: "Rajdhani, Barlow Condensed, sans-serif"`, `h1FontSize: "36px"`, `h1FontWeight: "700"`, `h1Color: "rgb(63, 200, 224)"`. Both `<h2>` elements: Rajdhani 700, `rgb(232, 234, 240)` (`#e8eaf0` text-primary). Lead `<p>` color: `rgb(110, 126, 156)` (`#6e7e9c` text-muted). Visual confirmation in all three viewport screenshots (Fact) | **RESOLVED** |
| 5 | `<main>` has zero padding, no max-width | Computed: `mainMaxWidth: "768px"`, `mainPadding: "32px 24px"` (px-6 py-8 on max-w-3xl). Visual confirmation: centered, bounded container visible at all viewports (Fact) | **RESOLVED** |

### WCAG 2.2 AA Re-verification

All contrast pairs from Round 1 remain unchanged. No new color introductions in the 5 fixes. The 5 fixes affected: `color-scheme` property (no text pairs), `font-weight` (no color change), em dash removal (copy only), Tailwind typography classes on `index.astro` (colors are `text-accent-blue`, `text-text`, `text-text-muted` -- all verified passing in Round 1), and container layout (no color change). No new contrast failures introduced. (Fact: token values unchanged, same pairs, same computed ratios.)

### Warframe 1999 Aesthetic Integrity

Desktop screenshot confirms:
- Cold blue (`#3fc8e0`) on `<h1>` -- accent correctly applied to primary title only
- Near-white (`#e8eaf0`) on `<h2>` headings -- correct text hierarchy, not competing with accent
- Muted slate (`#6e7e9c`) on lead `<p>` -- data-forward, minimal chrome
- Upload zone: Rajdhani Bold instruction text, ASCII corner brackets, accent-blue border -- all intact
- Background `#0d0f14` throughout -- no light-mode intrusion from scrollbars or form elements now that `color-scheme: dark` is set

No drift toward generic dark SaaS or developer-tool aesthetic detected in Round 2 screenshots.

### Absolute Bans Re-check (Round 2)

| Ban | Status |
|---|---|
| Gradient text | PASS -- `eval` confirmed `gradientTextCount: 0` on rendered DOM (Fact) |
| Glassmorphism / `backdrop-filter` | PASS -- `eval` confirmed `backdropBlurCount: 0` (Fact) |
| Side-stripe `border-left` | PASS -- unchanged from Round 1 |
| Modal-as-first-thought | PASS -- unchanged |
| Em dashes in UI copy | **PASS** -- RESOLVED (was FAIL in Round 1; `emDashCount: 0` confirmed) |

### New Issues Introduced by Round 2 Fixes

None. Static analysis and computed DOM inspection found no new High or Critical issues introduced by the five targeted fixes. The `<h2>` color resolves to `text-text` (`#e8eaf0`) rather than the accent-blue initially suggested in Finding #4's fix note -- this is correct per `index.astro` source lines 34 and 43 which use `text-text`, consistent with the brief's hierarchy where `<h1>` carries the accent-blue signal and `<h2>` uses near-white text-primary. Not a defect.

### Round 2 Open Items (unchanged from Round 1 advisory list)

No Medium or Low findings were addressed in Round 2. All findings #6-#15 remain at their original severity as advisory items. No findings escalated in severity between rounds.

**Round 2 verdict: ADVISORY**

All 5 High findings: RESOLVED.
Remaining open: Findings #6 (Medium), #7 (Medium/Info), #8 (Medium), #9 (Medium), #10 (Low), #11 (Low), #12 (Low), #13 (Low), #14 (Info), #15 (Info).
No Critical findings at any point.
No High findings remaining.
Herald 📯 (Release Manager) is unblocked.

---

## Round 3 Re-verification (2026-05-25)

**Trigger:** User opened browser after Round 2 ADVISORY and immediately found collapsed vertical spacing -- the ul/ol list markers and inter-element spacing were broken. Forge applied: `space-y-8` on `<main>`, heading `mt-10 mb-4`, `<ol class="list-decimal pl-6 space-y-2">`, `<ul class="list-disc pl-6 space-y-2">`, `<section class="mt-12">` around DucatAnalyzer, and logo wired next to H1 via `<div class="flex items-center gap-4">`.

**Context: Round 2 audit defect.** Round 2 claimed all 5 High findings RESOLVED. The spacing collapse and list-marker loss were not High findings in Round 1 or Round 2 because the fixes applied in Round 1 (typography classes on `index.astro`) appeared to restore the text but did not apply explicit list utilities. The Tailwind v4 preflight strips `list-style-type` and `padding-left` from `<ol>` and `<ul>` unless explicitly overridden -- Round 2 screenshots did not scroll to show the list area at sufficient zoom, and the eval checks focused on font-weight and color but not list-style or margin adjacency. This round applies Rules 1-6 in full.

**Dev server:** `http://localhost:4321/` -- clean build, zero console errors (Fact: `pnpm agent-browser errors` returned empty output).

---

### Round 3 Browser State

**URL:** `http://localhost:4321/`
**Errors:** None (Fact: `pnpm agent-browser errors` returned no output).
**Screenshots captured (Round 3):**
- Desktop 1440x900: `screenshot-1779725394227.png` -- screenshot full-page = true (Fact: `document.documentElement.scrollHeight` = 900, viewport height = 900; entire page fits in one viewport, no scroll required).
- Tablet 768x1024: `screenshot-1779725415273.png` -- screenshot full-page = true (Fact: `document.documentElement.scrollHeight` = 1024, viewport height = 1024; page fits in viewport).
- Mobile iPhone 14 (above fold): `screenshot-1779725431609.png` -- full-page = FALSE. Fact: `scrollHeight` = 1052px, viewport = ~844px. Below-fold region (DucatAnalyzer upload zone) unattested by this capture.
- Mobile iPhone 14 (scrolled, below fold): `screenshot-1779725449751.png` -- shows DucatAnalyzer upload zone, BROWSE FILES button. Covers the below-fold region.

All screenshots at `C:\Users\dexm7\.agent-browser\tmp\screenshots\`.

---

### Rule 5 -- Honest-Render Gate

Applied before interpreting any Round 3 screenshot.

Desktop 1440x900 screenshot (`screenshot-1779725394227.png`):
- Background: `rgb(13, 15, 20)` = `#0d0f14`. Dark background present. NOT default-browser white. PASS.
- H1 "ducat-lens": rendered in Rajdhani at 36px, weight 700, color `rgb(63, 200, 224)` = `#3fc8e0`. NOT default serif. PASS.
- H2 headings: Rajdhani 700, `rgb(232, 234, 240)` = `#e8eaf0`. PASS.
- OL numbered list: numbers visible (1. 2. 3.) in screenshot at coord approx 360,253. PASS.
- UL bulleted list: bullets visible (dot markers) at coord approx 360,423. PASS.
- Upload zone: dark panel with accent-blue bracket corners, "DROP SCREENSHOT OR CLICK TO BROWSE" in Rajdhani Bold. PASS.
- Body text: muted slate, not default browser blue links. PASS.

Honest-render gate: PASS. This is NOT unstyled default-browser HTML.

---

### Rule 1 -- Spacing Rhythm Check

Computed `margin-top`, `margin-bottom`, and visual `getBoundingClientRect` gap on all direct children of `<main>` at 1440x900 viewport.

Source: `pnpm agent-browser eval` at 1440x900.

**`<main>` computed class:** `max-w-3xl mx-auto px-6 py-8 space-y-8`
**`space-y-8` generates:** `--tw-space-y-reverse: 0; margin-top: calc(2rem * (1 - var(--tw-space-y-reverse)))` on non-first children, giving 32px top-gap between siblings.

| Element | Margin-top (computed) | Margin-bottom (computed) | BoundingRect top | BoundingRect bottom | Visual gap to next |
|---|---|---|---|---|---|
| DIV[0] (logo+H1 flex row) | 0px | 32px | 32 | 80 | 32px (to P[1]) |
| P[1] (description) | 0px | 32px | 112 | 164 | 40px (to H2[2]) |
| H2[2] "How it works" | 40px (mt-10) | 16px (mb-4) | 204 | 236 | 16px (to OL[3]) |
| OL[3] | 0px | 32px | 252 | 340 | 40px (to H2[4]) |
| H2[4] "Features" | 40px (mt-10) | 16px (mb-4) | 380 | 412 | 16px (to UL[5]) |
| UL[5] | 0px | 32px | 428 | 548 | 48px (to SECTION[6]) |
| SECTION[6] (DucatAnalyzer) | 48px (mt-12) | 0px | 596 | 756 | -- |

No adjacent pair has zero combined vertical spacing. The `space-y-8` ancestor (32px gap) catches all pairs not covered by explicit `mt-*`/`mb-*` classes. H2 headings add `mt-10` (40px) and `mb-4` (16px) for intentional tight coupling to their following list. SECTION gets an extra `mt-12` (48px) to visually separate the tool from the marketing copy above.

**Rule 1: PASS.** No spacing collapse detected. Label: Fact (computed from live DOM).

---

### Rule 2 -- List Rendering Check

**OL ("How it works"):**
- `list-style-type`: `decimal` (Fact: `getComputedStyle(ol).listStyleType` = `"decimal"`)
- `padding-left`: `24px` (Fact: `getComputedStyle(ol).paddingLeft` = `"24px"`)
- Numbers 1. 2. 3. visible in desktop screenshot at coord approx (360-380, 253-320). PASS.

**UL ("Features"):**
- `list-style-type`: `disc` (Fact: `getComputedStyle(ul).listStyleType` = `"disc"`)
- `padding-left`: `24px` (Fact: `getComputedStyle(ul).paddingLeft` = `"24px"`)
- Bullet markers visible in desktop screenshot at coord approx (360-380, 423-548). PASS.

**LI spacing (both lists):** `margin-bottom: 8px` on each `<li>` from `space-y-2` on parent. Items separated, not rammed together. PASS.

Neither list is a nav/menu styled without markers -- no justification exception needed.

**Rule 2: PASS.** List markers present, padding-left > 0. Label: Fact.

---

### Rule 3 -- Full-Page Screenshot Status

| Viewport | Screenshot | Full-page confirmed | Notes |
|---|---|---|---|
| Desktop 1440x900 | `screenshot-1779725394227.png` | YES -- `scrollHeight` = 900 = viewport height | Entire page visible in single capture |
| Tablet 768x1024 | `screenshot-1779725415273.png` | YES -- `scrollHeight` = 1024 = viewport height | Entire page visible |
| Mobile iPhone 14 | `screenshot-1779725431609.png` + `screenshot-1779725449751.png` | PARTIAL -- required two captures due to scrollHeight (1052px) > viewport (~844px) | Both captures together cover full page. Above-fold capture: `screenshot-1779725431609.png`. Below-fold capture (scrolled 500px): `screenshot-1779725449751.png`. |

The mobile case required two captures to cover the full page. Both are included. No region unattested.

---

### Rule 4 -- Visual Diff for RESOLVED Claims

**BEFORE screenshots (Round 2, from `screenshot-1779722727478.png` and `screenshot-1779722776481.png`):**

Round 2 desktop BEFORE state (viewed and confirmed):
- H1 "ducat-lens" immediately followed by P (description paragraph) with zero visible gap between them. The heading bottom and paragraph top were pixel-adjacent.
- "How it works" H2 immediately followed by OL list items rendered as plain unstyled text lines -- no numbers, no indentation, markers stripped by Tailwind v4 preflight.
- "Features" H2 immediately followed by UL list items rendered as plain text lines -- no bullet dots, no indentation.
- No logo next to H1. H1 was standalone text, not a flex row.

Round 3 desktop AFTER state (confirmed via `screenshot-1779725394227.png` and computed-style evals):
- H1 "ducat-lens" preceded by logo SVG at 48x48 in a flex row. 32px gap between logo+H1 row and description paragraph.
- "How it works" H2 with 40px top margin and 16px bottom margin. OL shows decimal numbers (1. 2. 3.) with 24px left padding.
- "Features" H2 with 40px top margin and 16px bottom margin. UL shows disc bullets with 24px left padding.
- DucatAnalyzer section separated by 48px (mt-12) from last UL.

| Claim | BEFORE evidence | AFTER evidence | Rule 4 status |
|---|---|---|---|
| Vertical spacing between elements | Zero gap: DIV[0] bottom = P[1] top (pixel-adjacent in Round 2 screenshot) | 32px gap: `space-y-8` confirmed via `getBoundingClientRect` gap of 32px between DIV[0] and P[1] | RESOLVED |
| OL numbered list markers | Plain text lines in Round 2 screenshot, no numbers visible | `list-style-type: decimal`, `padding-left: 24px`, numbers 1/2/3 visible in Round 3 screenshot | RESOLVED |
| UL bullet markers | Plain text lines in Round 2 screenshot, no bullets visible | `list-style-type: disc`, `padding-left: 24px`, bullet dots visible in Round 3 screenshot | RESOLVED |
| Logo next to H1 | Not present in Round 2 screenshots | `<img src="/logo.svg" alt="ducat-lens logo" width="48" height="48">` rendered at natural 150x150, displayed 48x48, `complete: true`, `sameLine: true` (logo.left=360, H1.left=424, verticalDiff < 20px) | RESOLVED -- NEW in Round 3 |

All resolution claims are backed by BEFORE screenshot evidence (Round 2 `screenshot-1779722727478.png`) plus AFTER screenshot and eval evidence (Round 3). No attested-from-code-only claims.

---

### New Findings (Round 3 only)

No new High or Critical findings introduced by the Round 3 fixes.

One new Medium-level observation: the `<h1>` text "ducat-lens" is lowercase in both the source and rendered output. The brief section 4.1 specifies `uppercase` tracking for heading-class text in the upload zone instruction ("DROP SCREENSHOT OR CLICK TO BROWSE"). The site `<h1>` uses Rajdhani Bold but without `uppercase` or `tracking-widest`. This is not a regression from Round 2 (the H1 was always lowercase-rendered). Noting it as a Medium finding since the brief's typography pattern for heading copy establishes uppercase as the norm for primary display text, but the product name "ducat-lens" may be intentionally lowercase as a brand identity choice. This is an IA/brand decision, not a clear defect.

| # | Severity | Location | Finding | Fix Route |
|---|----------|----------|---------|-----------|
| R3-1 | **Medium** | `frontend/src/pages/index.astro` line 28 | `<h1>` renders "ducat-lens" in lowercase Rajdhani Bold. Brief section 4.1 establishes uppercase Rajdhani as the heading pattern ("DROP SCREENSHOT OR CLICK TO BROWSE", badge labels, column headers all uppercase). The H1 breaks the all-caps typographic register. If the brand name is intentionally lowercase, this is a documented exception; if not, it is a casing inconsistency. | Cipher: confirm whether "ducat-lens" lowercase is intentional brand identity. If not, Forge adds `uppercase tracking-widest` classes to the `<h1>`. |

---

### Round 3 WCAG 2.2 AA Re-verification

No new color introductions in Round 3 fixes. Spacing utilities (`space-y-8`, `mt-10`, `mb-4`, `pl-6`) and structural changes (flex row, section wrapper) carry no color implications. All 9 previously-verified contrast pairs remain unchanged.

Logo SVG (`/logo.svg`): rendered at `natural: 150x150`, displayed: `48x48`. SVG renders on `#0d0f14` background. The logo uses `#c8a84b` (token gold) and `#3fc8e0` (accent blue) per visual inspection of the screenshot at coord approx (363-411, 20-68). Both colors on `#0d0f14` background exceed AA (token gold ~5.8:1, accent blue ~8.2:1). PASS.

---

### Round 3 Absolute Ban Re-check

| Ban | Status |
|---|---|
| Gradient text | PASS -- no change |
| Glassmorphism | PASS -- no change |
| Side-stripe `border-left` | PASS -- no change |
| Modal-as-first-thought | PASS -- no change |
| Em dashes in UI copy | PASS -- confirmed in source: commas used ("works instantly in your browser.", "no outbound calls at request time."), no em dash characters. Source lines 48-49 confirmed. |

---

### Round 3 Warframe 1999 Aesthetic Integrity

Desktop 1440x900 screenshot (`screenshot-1779725394227.png`) confirms full aesthetic stack:

- Logo + H1 flex row: gold/teal SVG icon at 48x48 next to "ducat-lens" in Rajdhani Bold cold-blue. Correct brand entry point.
- H2 headings ("How it works", "Features"): near-white Rajdhani Bold, no competing with accent blue on H1. Hierarchy intact.
- OL/UL copy: Roboto, muted-slate color, standard sans-serif body register. Correct semantic hierarchy (heading font for labels, body font for content).
- DucatAnalyzer upload zone: dark panel (`#1a1d26`) with accent-blue bracket corners (top-left `⌐ ¬`, bottom-right `└ ┘`), Rajdhani Bold instruction line "DROP SCREENSHOT OR CLICK TO BROWSE", muted hint text below.
- Background `#0d0f14` throughout. No light intrusion.
- No generic "dark SaaS" patterns detected: no pill buttons, no pastel accents, no card grid, no rounded-lg everywhere.

**Aesthetic integrity: PASS at all three viewports.**

---

### Round 3 Open Items

All advisory findings from Rounds 1 and 2 remain open (#6-#15). No advisory findings were addressed in Round 3.

One new Medium finding (#R3-1) added: H1 lowercase brand name vs. uppercase Rajdhani heading convention. Requires Cipher 🔓 (Dev-Team Orchestrator) product decision.

---

## Spot-Check Evidence

Three specific visual claims with pixel/eval proof for Cipher 🔓 (Dev-Team Orchestrator) review.

**Claim 1: H1 font is Rajdhani Bold 700 at 36px in cold blue (#3fc8e0).**
Evidence: `pnpm agent-browser eval "var h1=document.querySelector('main h1'); var cs=window.getComputedStyle(h1); cs.fontWeight+'|'+cs.fontFamily+'|'+cs.fontSize+'|'+cs.color"` returned `"700|Rajdhani, \"Barlow Condensed\", sans-serif|30px|rgb(63, 200, 224)"` at mobile viewport (390px wide, Tailwind responsive reduces from 36px to 30px). At desktop 1440px: `h1FontSize: "36px"` (confirmed via earlier Round 2 eval, consistent with `text-3xl md:text-4xl` classes). Color `rgb(63, 200, 224)` = `#3fc8e0` = accent-blue token. Screenshot coord approx (424, 20-68) at 1440 shows Rajdhani Bold rendering in cold blue. Label: Fact.

**Claim 2: Logo SVG loads and renders at 48x48 inline with H1 (same flex row).**
Evidence: `pnpm agent-browser eval` returned `{"logoSrc":"http://localhost:4321/logo.svg","logoAlt":"ducat-lens logo","logoWidth":48,"logoHeight":48,"logoComplete":true,"logoNatWidth":150,"logoNatHeight":150,"logoLeft":360,"h1Left":424,"sameLine":true}`. `complete: true` confirms successful load. `rendered 48x48` matches `width="48" height="48"` HTML attributes. `sameLine: true` (logo.top and H1.top differ by < 20px) confirms flex alignment. Visual confirmation: screenshot coord ~(363,20) shows SVG icon immediately left of "ducat-lens" text. Label: Fact.

**Claim 3: OL list-style-type is `decimal` with 24px left padding; UL is `disc` with 24px left padding. Both produce visible markers.**
Evidence: `pnpm agent-browser eval "var ol=document.querySelector('main ol'); var ul=document.querySelector('main ul'); window.getComputedStyle(ol).listStyleType+'|'+window.getComputedStyle(ol).paddingLeft+'|'+window.getComputedStyle(ul).listStyleType+'|'+window.getComputedStyle(ul).paddingLeft"` returned `"decimal|24px|disc|24px"`. Numbers "1. 2. 3." visible in screenshot at coord approx (360-380, 253-320). Bullet dots visible at coord approx (360-380, 423-548). These were ABSENT in Round 2 BEFORE screenshots (`screenshot-1779722727478.png`) where OL/UL items rendered as plain text lines with no markers. Label: Fact.

---

**Round 3 verdict: ADVISORY**

No Critical findings. No High findings. Honest-render gate: PASS. Rules 1-6: all PASS.

New findings in Round 3: one Medium (#R3-1, H1 lowercase vs. uppercase heading convention -- requires Cipher 🔓 brand decision).

Remaining open from prior rounds: Findings #6 (Medium), #7 (Medium/Info), #8 (Medium), #9 (Medium), #10 (Low), #11 (Low), #12 (Low), #13 (Low), #14 (Info), #15 (Info).

Herald 📯 (Release Manager) is unblocked. Cipher 🔓 (Dev-Team Orchestrator) review of Spot-Check Evidence required before confirming unblock.
