# Design Brief: Phase 09: Upload UI + Results Table + Sell/Keep Recommendations

---

## 1. Compliance Preamble

### PRODUCT.md Compliance

- Register: `product`. This brief produces no marketing register, hero sections, or social proof.
- Tone: "terminal, gritty, trustworthy." Copy strings throughout use clipped, data-forward language. No friendly onboarding softness.
- Anti-references respected:
  - No generic SaaS minimalism (rounded corners, pastel accents, cream backgrounds).
  - No classic Orokin aesthetic (gold filigree, white voids, energy-field borders).
  - No marketing-page structure.
  - No mobile-first card grids; desktop-first layout with explicit mobile fallback.
  - No cute or playful copy.
  - No glassmorphism.
  - No gradient text.
- Design principles applied:
  - Speed-to-answer: upload zone is the primary element; results appear immediately inline, no modal gate.
  - Trust through precision: ducat values shown exact, recommendation thresholds visible on the table surface.
  - Visual coherence earns its reference: every 1999 element (brackets, scanlines, flicker) must aid clarity, not decorate.
  - Interface disappears into the task: navigation chrome is minimal; the table is the product.

### DESIGN.md Compliance

All color references in this brief use tokens as defined in DESIGN.md frontmatter. Specific named rules invoked:
- The One-Voice Rule: `#3fc8e0` is the sole interactive UI accent throughout.
- The Gold Containment Rule: `#c8a84b` appears only in the Ducats column and SELL verdict tint.
- The Mono-for-Numbers Rule: all numeric data in IBM Plex Mono.
- The Flat-By-Default Rule: no permanent `box-shadow`; glow responds to state only.

### ui-ux-pro-max Patterns Cited

Per `knowledge/research/ui-patterns-phase-09.md`:
- Upload zone: dashed-border interactive dropzone (ux-guidelines) + scan-sweep feedback (ux-guidelines loading states, severity High)
- Results table: TanStack Table + shadcn DataTable pattern (stacks/shadcn.csv, severity Medium); semantic table structure (severity High); mobile overflow via card collapse (ux-guidelines, severity Medium)
- Verdict badge: color + text + border combined; never color alone (ux-guidelines, severity High); muted-fill label from data-dense dashboard pattern (styles.csv)
- Async status: skeleton screens + aria-live + error recovery (ux-guidelines, severity High for each)
- Dark-mode-only: OLED Dark + Cyberpunk UI structural vocabulary, deviated to 1999 Höllvania palette (styles.csv)

---

## 2. Color Strategy and Theme Decision

**Color strategy: Committed.**

Justification: this is a data-heavy, single-surface tool. "Restrained" (one accent at 10% of screen) leaves the table feeling flat; the SELL/KEEP/CONSIDER verdicts need enough chromatic weight to communicate at a glance across 10-30 rows. "Committed" means one saturated color (cold blue `#3fc8e0`) carries 20-30% of interactive surface area (borders, headers, focus states, scan animation), while gold and green operate as purposeful data annotations. Full palette or Drenched would overwhelm the data readout.

**Theme decision sentence:** The player sits at their desktop post-farming-run, Kiosk screen open in Warframe on one monitor and ducat-lens on the other, under the glow of their PC setup in a dark room. The dark theme is not a choice; it is the operating environment.

The site is permanently dark. No light-mode toggle. No `.dark` class switching. `:root` IS the Höllvania theme. `color-scheme: dark` declared on `:root`.

---

## 3. AI Slop Test

### First-order check: category-reflex test

**Question:** Is this design "Warframe game tool, therefore: dark background, neon accents, scanlines, some kind of HUD overlay"?

**Result: No.** The surface is not generically "gamer dark." The specific references are Warframe 1999's documented visual language:
- Background is `#0d0f14` (raised black with cool blue-grey cast), not pure OLED black or standard dark-mode grey.
- Accent is `#3fc8e0` (Höllvania mall/street cold blue-teal), not a generic neon cyan.
- Gold (`#c8a84b`) is used for ducats because ducats are literally Orokin currency; the use is semantic, not decorative.
- Green (`#4cde5a`) derives from Efervon chemical hazard color (in-world signal color for Scaldra faction). Not "matrix green."
- Scanlines are panel-scoped at 5-8% opacity, not a full-viewport parallax CRT overlay.
- ASCII corner brackets (`⌐ ¬ └ ┘`) reference the warframe.com/1999 official site's bracket/symbol separators, not a generic sci-fi frame.
- Motion vocabulary (scan-sweep, 80ms flicker) references DE's Pom-2 boot sequence and KIM messenger notification patterns, not generic parallax or entrance animations.

**First-order test: PASSED.** The design is not a category reflex.

### Second-order check: "dark mode with neon accents" lane test

**Question:** Is this design just "dark background + neon borders + monospace font," which is the generic developer-tool aesthetic flooding the market?

**Result: No.** Three specific differentiators prevent landing in that lane:
1. Typography pairing: Rajdhani Bold (condensed broadcast-display) + IBM Plex Mono + Roboto. Generic dark dev tools use a single monospace stack. The heading font carries the 1999 industrial-broadcast personality; mono is data-only.
2. Palette restraint: the cold blue is desaturated (not full-brightness `#00FFFF`). Gold and green have specific semantic domains they cannot escape. The background has blue-grey warmth, not OLED pure black. This palette is not interchangeable with Vercel, GitHub, or any standard dev-tool dark theme.
3. Period-correct ornament: ASCII brackets, inset scanlines, and the scan-sweep animation are not generic tech UX. They come from a documented research brief (`knowledge/research/warframe-1999-visual-spec.md`) with cited sources. A designer who did not read that brief would not arrive at these specific choices.

**What would make it fail:** dropping the Rajdhani heading font for a generic Inter or system-ui; replacing the cold blue with saturated `#00d4ff`; adding ambient full-page neon glow or gradient borders; using the gold for decoration rather than currency-specific data.

**Second-order test: PASSED.**

---

## 4. Surfaces

### 4.1 Upload Zone

**Anatomy**

A full-width panel (`w-full`) on its own row above the results area. Min-height `min-h-[160px]`, no max-height. Centered flex column layout. Four elements inside: ASCII bracket pseudo-elements at corners, Lucide icon, instruction line, hint line.

```
class="relative w-full min-h-[160px] flex flex-col items-center justify-center
       gap-3 rounded-sm border border-accent-blue/40 bg-surface p-6
       cursor-pointer transition-all duration-150 ease-out"
```

ASCII brackets via CSS in a global class `.bracket-corners`:
```css
.bracket-corners::before,
.bracket-corners::after {
  content: '⌐ ¬';
  position: absolute;
  font-family: var(--font-data);
  font-size: 0.75rem;
  color: var(--color-accent-blue);
  opacity: 0.7;
  pointer-events: none;
}
.bracket-corners::before { top: 6px; left: 8px; }
.bracket-corners::after  { bottom: 6px; right: 8px;
  content: '└ ┘'; }
```

Inner content:
```
<Upload size={24} class="text-accent-blue" />
<p class="font-heading text-sm tracking-widest uppercase text-text-primary">
  DROP SCREENSHOT OR CLICK TO BROWSE
</p>
<p class="font-body text-xs text-text-secondary">
  PNG, JPG, WebP. Max 10 MB. Kiosk inventory screen only.
</p>
```

**States**

| State | Border | Background | Icon | Text color | Shadow |
|---|---|---|---|---|---|
| Idle | `accent-blue/40` | `bg-surface` | `text-accent-blue` | `text-text-primary` | none |
| Hover | `accent-blue` | `bg-surface` | `text-accent-blue` | `text-accent-blue` | `0 0 12px rgba(63,200,224,0.35)` |
| Drag-over | `accent-blue` | `bg-surface-alt` | `text-accent-blue` | `text-accent-blue` | `0 0 12px rgba(63,200,224,0.35)` |
| File accepted | `status-success` | `bg-surface` | CheckCircle `text-status-success` | `text-status-success` | none |
| File rejected | `status-error` | `bg-surface` | XCircle `text-status-error` | `text-status-error` | `0 0 8px rgba(224,48,48,0.4)` |
| Locked (processing) | `accent-blue/20` | `bg-surface` | Loader2 spinning | `text-text-muted` | none |

Transition on all states: `transition-all duration-150 ease-out`.

Rejected file type: inline `role="alert"` text below the zone (not a modal, not a toast):
```
class="mt-2 flex items-center gap-1.5 text-xs text-status-error font-body"
```
Copy: "UNSUPPORTED FORMAT: use PNG, JPG, or WebP"

**Responsive variants**

- `>= 1024px` (desktop): full-width, `min-h-[160px]`
- `768px – 1023px` (tablet): full-width, `min-h-[140px]`, reduced padding `p-4`
- `< 768px` (mobile): full-width, `min-h-[120px]`, instruction text wraps to two lines naturally

**shadcn components used**

- No shadcn component for the zone itself; custom `<div>` with `role="button"` and drag-event handlers.
- Button (shadcn) variant=`outline` for the "Browse files" fallback CTA below the zone on mobile only.

**Motion spec**

- All state transitions: `150ms ease-out` on border-color, background-color, box-shadow.
- `prefers-reduced-motion`: remove box-shadow animation, keep color transitions.
- No entrance animation on initial page load.

---

### 4.2 Results Table

**Anatomy**

Shadcn `Table` component inside a `Card`-like container panel. Sticky `<thead>`. Five columns: `#`, `ITEM NAME`, `DUCATS`, `VERDICT`, `NOTES`.

Container:
```
class="w-full rounded-sm border border-border bg-surface overflow-hidden"
```

Table head row:
```
class="border-b border-border bg-bg"
```

Column headers:
```
class="px-3 py-2 font-heading text-xs tracking-widest uppercase text-accent-blue
       text-left select-none cursor-pointer hover:text-text-primary transition-colors duration-150"
```

Sort icon (Lucide `ArrowUpDown`, 12px): inline after header text, `text-text-muted`.

Row (even):
```
class="border-b border-border/40 bg-bg hover:bg-surface transition-colors duration-[80ms]"
```

Row (odd):
```
class="border-b border-border/40 bg-surface-alt hover:bg-surface transition-colors duration-[80ms]"
```

SELL row override (background tint only; no side stripe per impeccable absolute ban on `border-left` > 1px as accent):
```
class="border-b border-border/40 bg-status-success/5
       hover:bg-status-success/10 transition-colors duration-[80ms]"
```
The SELL badge in the ACTION column carries the verdict signal. Background tint provides the at-a-glance row distinction. Decision locked 2026-05-25 by Cipher 🔓 (Dev-Team Orchestrator) to resolve brief↔impeccable contradiction flagged by Sentinel 🛡️ (Quality Guardian) audit.

Cell: item name
```
class="px-3 py-2.5 font-data text-sm text-text-primary"
```

Cell: ducat value
```
class="px-3 py-2.5 font-data text-sm text-token-gold text-right tabular-nums"
```

Cell: verdict
```
class="px-3 py-2.5 text-center"
```

Cell: notes (optional)
```
class="px-3 py-2.5 font-body text-xs text-text-muted"
```

**Sortable columns**

- ITEM NAME: alphabetical.
- DUCATS: numeric, descending default.
- VERDICT: sort order SELL > CONSIDER > KEEP.
- Sort state: active column header `text-text-primary`; sort direction: Lucide `ArrowUp` or `ArrowDown` replacing `ArrowUpDown`.

TanStack Table: `useReactTable` with `getSortedRowModel()`. Column definition specifies `sortingFn: 'alphanumeric'` for name/verdict, `'basic'` for numeric value.

**Responsive variants**

- `>= 768px`: full table layout.
- `< 768px`: CSS display override, each `<tr>` becomes a flex column card. Header row hidden. Each row renders as a card with label/value pairs stacked vertically. Card class:
```
class="mb-2 rounded-sm border border-border bg-surface p-3 flex flex-col gap-1.5"
```
Label inside card: `class="font-heading text-xs tracking-widest uppercase text-accent-blue"` (the column name).
Value inside card: `class="font-data text-sm text-text-primary"`.

**shadcn components used**

- `Table`, `TableHeader`, `TableBody`, `TableRow`, `TableHead`, `TableCell` from shadcn `@radix-ui/react-slot`-backed table.
- Add: `pnpm dlx shadcn@4.8.0 add table`

**Motion spec**

Results table reveal: `opacity: 0 → 1` over `200ms ease-out`, triggered when OCR pipeline returns. Gate behind `prefers-reduced-motion`: instant `opacity: 1` with no transition.
Row hover: `80ms ease-out` on background-color. No transform.

---

### 4.3 Sell/Keep Verdict Badges

**Anatomy**

Inline `<span>` used inside the Verdict table cell (shadcn `Badge` can be used as the primitive, but the variant must be custom to match 1999 token system; do not use shadcn Badge's default pill radius).

**SELL:**
```
class="inline-flex items-center gap-1 rounded-[1px] border border-status-success/30
       bg-status-success/12 px-2 py-0.5 font-heading text-xs tracking-widest
       uppercase text-status-success"
```

**KEEP:**
```
class="inline-flex items-center gap-1 rounded-[1px] border border-text-secondary/20
       bg-text-secondary/10 px-2 py-0.5 font-heading text-xs tracking-widest
       uppercase text-text-secondary"
```

**CONSIDER:**
```
class="inline-flex items-center gap-1 rounded-[1px] border border-status-warning/30
       bg-status-warning/12 px-2 py-0.5 font-heading text-xs tracking-widest
       uppercase text-status-warning"
```

No icon inside the badge; text label is sufficient at table density. The row's left-border accent (SELL rows only) provides secondary color confirmation without redundancy.

**Accessibility**

Color is never the sole indicator. Text label (SELL / KEEP / CONSIDER) announced by screen reader directly. No `aria-label` override needed. Badge has no interactive role; it is a presentational label inside a `<td>`. Do not make it focusable.

**WCAG contrast verification**

| Pair | Ratio (Fact: calculated against bg) | AA pass? |
|---|---|---|
| `#4cde5a` on `rgba(76,222,90,0.12)` over `#1a1d26` = effective `#1e2c1f` | ~7.2:1 | Yes (AAA) |
| `#8a9ab0` on `rgba(138,154,176,0.10)` over `#1a1d26` = effective `#1e2022` | ~4.6:1 | Yes (AA) |
| `#d4b820` on `rgba(212,184,32,0.12)` over `#1a1d26` = effective `#1f1e1c` | ~6.8:1 | Yes (AAA) |

Note: contrast ratios above are computed against the effective blended background; browser rendering of alpha-composite values should be verified in the browser audit gate before ship. These are Hypothesis values pending actual browser measurement.

**shadcn components used**

- shadcn `Badge` as primitive (zero-radius override needed). Add: `pnpm dlx shadcn@4.8.0 add badge`

---

### 4.4 Status Indicators

**Anatomy: full state machine**

All status indicators live in a single `<div>` container between the upload zone and the results table. This container is always rendered; its content changes per state.

Container:
```
class="w-full" role="status" aria-live="polite" aria-atomic="true"
```
Upgrade to `role="alert"` when in error state (JavaScript toggle).

**State 1: Idle (no upload yet)**

Container is visually empty. No placeholder text. The upload zone is the sole prompt.

**State 2: Processing (file accepted, OCR running)**

Scan-sweep bar:
```
class="h-0.5 w-full overflow-hidden bg-surface-alt rounded-none"
```
Inner sweep element:
```
class="h-full bg-accent-blue animate-scan-sweep"
```
Keyframe (defined in `global.css`):
```css
@keyframes scan-sweep {
  from { width: 0%; }
  to   { width: 100%; }
}
.animate-scan-sweep {
  animation: scan-sweep 0.4s linear forwards;
}
@media (prefers-reduced-motion: reduce) {
  .animate-scan-sweep {
    animation: none;
    width: 100%;
  }
}
```

Below the bar, skeleton rows in the results table area (see §4.2 skeleton variant below).

Skeleton row:
```
class="h-10 w-full rounded-none bg-surface-alt animate-pulse border-b border-border/20"
```
Show 8 skeleton rows. `aria-busy="true"` on the table container.

**State 3: Success (results returned)**

Scan-sweep bar completes (or is instantly full in reduced-motion mode). Status container returns to empty. Results table transitions in. `aria-busy="false"` on the table container.

A one-line status readout above the table, then auto-dismisses after 3 seconds:
```
class="mb-2 flex items-center gap-1.5 text-xs font-data text-status-success"
```
Copy: "ANALYSIS COMPLETE: {N} ITEMS IDENTIFIED"
Icon: Lucide `ScanLine`, 12px.
Dismisses: `opacity: 1 → 0` over 500ms at 3s. Gate behind `prefers-reduced-motion`.

**State 4: Empty (OCR found no items)**

Results area shows:
```
class="w-full flex flex-col items-center justify-center gap-3 py-12
       border border-border/30 rounded-sm bg-surface"
```
```
<FileSearch size={32} class="text-text-muted" />
<p class="font-data text-sm uppercase tracking-widest text-text-muted">
  NO ITEMS IDENTIFIED
</p>
<p class="font-body text-xs text-text-muted max-w-[40ch] text-center">
  Ensure the Kiosk inventory panel is fully visible and unobscured in the screenshot.
</p>
```

**State 5: Error (OCR failure, network error, wrong file)**

Upload zone border changes to `border-status-error`. Status container:
```
role="alert" aria-live="assertive"
class="mt-2 flex items-center gap-2 rounded-sm border border-status-error/30
       bg-status-error/8 px-3 py-2.5 text-sm text-status-error font-body"
```
```
<AlertTriangle size={16} class="shrink-0" />
<span>ANALYSIS FAILED: {specific reason}</span>
```
Recovery affordance: a text button `text-accent-blue hover:underline text-xs font-data` labeled "RETRY: upload a new screenshot" which re-activates the upload zone.

Error copy variants:
- OCR pipeline failure: "ANALYSIS FAILED: OCR engine error"
- Network failure: "ANALYSIS FAILED: could not reach lookup service"
- File type rejected: "UNSUPPORTED FORMAT: use PNG, JPG, or WebP"
- File too large: "FILE TOO LARGE: maximum 10 MB"

**shadcn components used**

No shadcn component for status indicators; native HTML with Tailwind utilities and Lucide icons.

**Motion spec**

- Scan-sweep: `0.4s linear forwards`. One-shot, not looping.
- Success readout dismiss: `500ms ease-out` opacity fade at 3s delay. Gate reduced-motion.
- Error state appearance: `150ms ease-out` on border-color and background-color. No entrance animation.
- Skeleton pulse: Tailwind `animate-pulse` (default 2s ease-in-out infinite). Stops when `aria-busy="false"`.

---

## 5. shadcn Components to Add

Only Button is currently installed. Add these before implementation:

| Component | Install command | Used by |
|---|---|---|
| Table | `pnpm dlx shadcn@4.8.0 add table` | Results table |
| Badge | `pnpm dlx shadcn@4.8.0 add badge` | Verdict badges (custom variant override) |
| Skeleton | `pnpm dlx shadcn@4.8.0 add skeleton` | Processing state skeleton rows |
| Card | `pnpm dlx shadcn@4.8.0 add card` | Panel containers (optional; may use custom `div`) |

TanStack Table dependency (not a shadcn add):
```
pnpm add @tanstack/react-table@8.21.3
```
(Pin exact version per project discipline; verify latest stable at install time and pin that exact number.)

---

## 6. Accessibility

### WCAG 2.2 AA Contrast Table

| Element | Foreground | Background | Ratio (Hypothesis) | AA pass |
|---|---|---|---|---|
| Primary text | `#e8eaf0` | `#0d0f14` | ~14.6:1 | Yes (AAA) |
| Secondary text | `#8a9ab0` | `#0d0f14` | ~5.4:1 | Yes (AA) |
| Secondary text | `#8a9ab0` | `#1a1d26` | ~4.7:1 | Yes (AA marginal) |
| Muted text | `#6e7e9c` | `#0d0f14` | ~4.75:1 | Yes (AA); corrected from `#4a5568` (3.0:1 fail) per Cipher 🔓 (Dev-Team Orchestrator) decision 2026-05-25 |
| Accent blue | `#3fc8e0` | `#0d0f14` | ~8.2:1 | Yes (AAA) |
| Accent blue | `#3fc8e0` | `#1a1d26` | ~6.9:1 | Yes (AAA) |
| Token gold | `#c8a84b` | `#0d0f14` | ~5.8:1 | Yes (AA) |
| Token gold | `#c8a84b` | `#1a1d26` | ~4.9:1 | Yes (AA) |
| Status green | `#4cde5a` | `#0d0f14` | ~8.9:1 | Yes (AAA) |
| Status green | `#4cde5a` | `#1a1d26` | ~7.5:1 | Yes (AAA) |
| Status warning | `#d4b820` | `#0d0f14` | ~6.5:1 | Yes (AA) |
| Status error | `#e03030` | `#0d0f14` | ~4.7:1 | Yes (AA) |

Note: all ratios labeled Hypothesis; computed via WCAG relative luminance formula but not verified in a dedicated contrast tool against actual rendered values. Downstream audit gate must verify each pair. Muted/metadata color shifted from `#4a5568` (3.0:1 fail) to `#6e7e9c` (~4.75:1 pass) per Cipher 🔓 (Dev-Team Orchestrator) decision 2026-05-25; all tokens now clear AA on primary background.

### Focus management

- All interactive elements (upload zone, table column headers, retry button): `focus-visible:ring-2 ring-accent-blue/50 outline-none`.
- The upload zone has `role="button"` and responds to `Enter` and `Space` keyboard events.
- Tab order: header logo → upload zone → (during results) table sort headers → retry button (if error).
- `tabIndex={0}` on upload zone explicitly.

### Keyboard

- Upload zone: `Enter` / `Space` triggers file picker. `Escape` cancels drag-over state.
- Table headers: `Enter` or `Space` toggles sort on the focused column.
- No keyboard trap anywhere. No timed auto-action.

### Screen reader

- Upload zone: `aria-label="Upload Warframe Kiosk screenshot for ducat analysis"`.
- Scan-sweep bar: `role="progressbar" aria-label="Analyzing screenshot" aria-valuenow` updated 0-100.
- Results table: `aria-label="Ducat analysis results"`. `aria-sort` attribute on sorted column header (`ascending` / `descending` / `none`).
- Verdict badge: text is inline; no additional `aria-label` needed.
- Status container: `role="status" aria-live="polite"` at rest; `role="alert" aria-live="assertive"` on error.

### Motion gating

All animations declared with a companion `@media (prefers-reduced-motion: reduce)` block:
- Scan-sweep: instant fill, no animation.
- Hover flicker: disabled.
- Results table fade-in: instant opacity change.
- Skeleton pulse: replaced with static `opacity: 0.6`.
- Success readout dismiss: instant hide after 3s, no fade transition.

### Touch targets

All interactive elements: minimum `min-h-[44px]` even at desktop. Upload zone is inherently larger. Sort-header touch target: `py-3` padding to reach 44px height. Retry button: `min-h-[44px]` enforced via Tailwind class.

---

## 7. Implementation Notes

### Astro vs React island split

The page is an Astro route. React islands are opt-in per component.

| Component | Astro or React island | Reason |
|---|---|---|
| Page shell / layout | Astro | Static HTML, no JS needed |
| Header bar + logo | Astro | No interactivity |
| Upload zone | React island (`client:load`) | Drag-and-drop events, file input state |
| Status indicator | React island (`client:load`) | Dynamic state driven by upload/analysis lifecycle |
| Results table | React island (`client:load`) | TanStack Table sort state, skeleton swap |
| Verdict badges | Inside React island | Rendered by Results Table component |

The entire upload + analysis + results flow is a single React component tree hydrated on load. Split:
- `<UploadZone />`: handles file input, drag-and-drop, emits `onFileAccepted(file: File)`
- `<AnalysisStatus />`: driven by `status: 'idle' | 'processing' | 'success' | 'error' | 'empty'`
- `<ResultsTable />`: receives `items: AnalysisResult[]`, manages TanStack sort state internally

These three can be composed in a single `<DucatAnalyzer client:load />` island component.

### `PUBLIC_API_URL` env var

The frontend calls the FastAPI backend via `PUBLIC_API_URL` (Vite/Astro public env var). Format: `POST ${PUBLIC_API_URL}/analyze` with the image as `multipart/form-data`. Default value for local dev: `http://localhost:8000`. For production: injected at build time or runtime.

Do not hardcode the URL. Read from `import.meta.env.PUBLIC_API_URL`.

### Google Fonts load strategy

In `BaseLayout.astro` (or equivalent Astro base layout), add before `</head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Rajdhani:wght@700&family=IBM+Plex+Mono:wght@400;500&family=Roboto:wght@400;500&display=swap" />
```

Do not use `@import` in CSS. Do not load font weights not in this list. The `display=swap` parameter prevents FOIT.

### `global.css` additions for phase 09

Add to `frontend/src/styles/global.css` (Forge 🔨 (Implementation Agent) task, not Lumen ✨ (Visual Director)):
```css
@keyframes scan-sweep {
  from { width: 0%; }
  to   { width: 100%; }
}

@layer utilities {
  .animate-scan-sweep {
    animation: scan-sweep 0.4s linear forwards;
  }
  @media (prefers-reduced-motion: reduce) {
    .animate-scan-sweep {
      animation: none;
      width: 100%;
    }
  }
}
```

### Tailwind v4 class syntax

No `@apply` for component-specific styles. Utility classes only. No inline `style` attributes. Token references use the `var()` form only in raw CSS; in Tailwind class strings use the token shorthand: `bg-surface`, `text-accent-blue`, `border-border`, `text-token-gold`.

Custom bracket corner CSS is the one exception; it requires a CSS class in `global.css` because pseudo-elements cannot be expressed as Tailwind utilities.

---

## 8. Out of Scope

- Multi-image batch upload
- Image preview before analysis
- Analysis history or session persistence
- CSV export of results
- Light mode or theme toggle
- Retry-with-different-image auto-suggestion
- i18n / locale support
- User accounts or saved preferences
- Sorting by multiple columns simultaneously
- Filter/search within the results table
- Ducat total sum row or aggregate display (phase 10 candidate)
- Accessibility WCAG AAA target (AA is the floor; AAA is aspirational for individual elements only)
