# UI Pattern Research — Phase 09 (Upload UI + Results Table + Sell/Keep Recs)

Compiled from ui-ux-pro-max CSV catalog queries. Each section: top patterns found, source domain, ducat-lens applicability.

---

## 1. File Upload / Dropzone

**Query:** "file upload dropzone drag drop preview" — domain: ux
**Query:** "file upload dropzone drag drop dark mode tool" — design-system

### Patterns found

**Pattern A — Dashed-border interactive dropzone (UX convention)**
- Source: ui-ux-pro-max ux-guidelines.csv (inferred from loading-state + form patterns; explicit file-upload pattern absent from ux CSV)
- Convention: large clickable/droppable region, dashed border signals droppability, icon + instruction copy + hint text, file-type restriction communicated upfront
- State machine: idle → hover/drag-over (border highlights) → accepted (file name shown) → error (wrong type/size)
- Key rule from catalog: "disable button and show loading state" during async operation (loading-buttons, severity High)

**Pattern B — Inline preview deferred (from cyberpunk/tool dark-mode style category)**
- Source: styles.csv — Dark Mode OLED, Cyberpunk UI
- Convention: no thumbnail preview on upload (avoids cluttering a tool with consumer-app affordances); accepted file name displayed inline as text, not as image card
- Rationale for ducat-lens: screenshots are analysis inputs, not media assets. A text confirmation of the file name is sufficient.

**Pattern C — Status-forward feedback (from UX loading states)**
- Source: ux-guidelines.csv (Loading States, severity High)
- Convention: skeleton screens or spinners for async operations over 300ms; scan-line/progress bar for single-step pipeline operations
- For ducat-lens: a single scan-sweep bar (not spinner) signals the OCR pipeline is running; feedback is linear, not indeterminate

**Ducat-lens selection:** Combine Pattern A (dashed/bordered zone with drag-and-drop) + Pattern C (scan-sweep status bar) + no preview (Pattern B rationale). Dropzone is the page's primary visual anchor at idle state.

---

## 2. Sortable Data Table

**Query:** "sortable data table action column verdict badge" — domain: ux
**Query:** "shadcn gaming tool dark upload table badge" — stack: shadcn

### Patterns found

**Pattern A — TanStack Table + shadcn DataTable (shadcn stack, severity Medium)**
- Source: stacks/shadcn.csv — DataTable guideline
- Convention: `useReactTable` hook combined with shadcn Table primitives (`Table`, `TableHeader`, `TableBody`, `TableRow`, `TableHead`, `TableCell`). Handles column sort, filter, pagination without custom implementations.
- Key rule: "Use Table for tabular data display. Don't use div grid for table-like layouts." (severity Medium)
- Requires semantic `<thead>` / `<tbody>` structure (severity High)

**Pattern B — Table horizontal scroll on mobile (UX responsive table, severity Medium)**
- Source: ux-guidelines.csv — Table Handling
- Convention: `overflow-x-auto` wrapper for mobile viewport; alternatively collapse to card layout per row
- For ducat-lens: desktop-first but mobile users exist; card-per-row collapse at `< 768px` is the correct fallback (avoids horizontal scroll on small screens where the table has 4-5 columns)

**Pattern C — Bulk/row action accessibility**
- Source: ux-guidelines.csv — Bulk Actions (severity Low)
- Convention: per-row action is sufficient for a read-only results table; bulk action only applies if users need to mark items
- For ducat-lens: results table is read-only (no per-row action needed in phase 09); verdict column is the action output

**Ducat-lens selection:** shadcn Table (semantic) with TanStack Table for sort. Single-column sort on Ducat Value and Name columns. No pagination (max ~30 rows). Mobile collapse to card layout.

---

## 3. Verdict Badge

**Query:** "status badge color indicator verdict chip label" — domain: ux

### Patterns found

**Pattern A — Color + text + shape (a11y critical)**
- Source: ux-guidelines.csv — Color Only (severity High)
- Hard rule: "Don't convey information by color alone. Use icons/text in addition to color."
- Implementation: badge must carry the text string (SELL / KEEP / CONSIDER) and a distinct border-color. Color shift alone is not sufficient.

**Pattern B — High-contrast badge on dark surfaces**
- Source: styles.csv — Dark Mode OLED, Inclusive Design
- Convention: status badges on dark backgrounds require text contrast 7:1+ for AAA; 4.5:1 minimum for AA. Neon accent colors (`#4cde5a`, `#d4b820`) on near-black (`#1a1d26`) pass AA but require verification.
- Key rule: "symbol-based indicators, not color-only" (Inclusive Design pattern)

**Pattern C — Muted fill + full text label (data-dense dashboard)**
- Source: styles.csv — Data-Dense Dashboard
- Convention: status indicators in data tables use a muted background fill (low opacity) with the full text label, not just a dot or icon. High information density without relying on decoding color.
- For ducat-lens: `bg-status-success/12` fill + `text-status-success` foreground + uppercase text is the correct implementation.

**Ducat-lens selection:** Pattern A (required) + Pattern C (recommended). Badges: muted fill, colored text, full text label, 1px border, 1px radius, uppercase Rajdhani tracking-widest.

---

## 4. Async Status Indicator

**Query:** "async loading states skeleton spinner aria-live empty error" — domain: ux

### Patterns found

**Pattern A — Skeleton screens for content placeholders (severity High)**
- Source: ux-guidelines.csv — Loading States
- Convention: `animate-pulse` skeleton blocks matching the dimensions of expected content. Show one skeleton row per expected data row.
- For ducat-lens: skeleton rows in the results table while OCR/lookup is in progress. Row count can be estimated or fixed at 8-10 placeholder rows.

**Pattern B — aria-live for dynamic content (severity High)**
- Source: ux-guidelines.csv — Error Messages
- Hard rule: "Use aria-live or role=alert for errors. Don't use visual-only error indication."
- Convention: `role="alert"` for errors (assertive), `aria-live="polite"` for status updates (progress)
- For ducat-lens: status container wrapping the scan-sweep bar gets `aria-live="polite"`; error container gets `role="alert"`.

**Pattern C — Disable submit button during async operation (severity High)**
- Source: ux-guidelines.csv — Loading Buttons
- Rule: "Disable button and show loading state during async actions."
- For ducat-lens: the upload zone becomes non-interactive during OCR pipeline; spinner or scan-sweep indicates progress.

**Pattern D — Error recovery with clear next steps (severity Medium)**
- Source: ux-guidelines.csv — Error Recovery
- Convention: error state must offer a recovery action — not just a message.
- For ducat-lens: OCR error shows "ANALYSIS FAILED" + "Try a clearer screenshot" + a re-upload affordance (click zone to re-trigger).

**Pattern E — Empty state with helpful message (severity Medium)**
- Source: ux-guidelines.csv — Empty States
- Convention: "No items yet. Create one!" pattern — give context and a next action.
- For ducat-lens: "NO ITEMS IDENTIFIED" empty state includes a secondary line "Ensure the Kiosk inventory is fully visible in the screenshot."

**Ducat-lens selection:** All five patterns apply. State machine: idle → uploading (zone locked, scan-sweep) → analyzing (skeleton rows in table) → success (table reveals) → error/empty (inline alert with recovery).

---

## 5. Dark-Mode-Only Product UI

**Query:** "dark mode only single theme gaming tool dashboard" — domain: style
**Query:** "dark mode cyberpunk terminal retro sci-fi" — domain: style

### Patterns found

**Pattern A — Dark Mode OLED (style catalog)**
- Source: styles.csv
- Convention: deep near-black background (not pure `#000000`), high contrast text (7:1+), minimal glow effects (not ambient neon everywhere), `color-scheme: dark`
- Accessibility: WCAG AAA achievable. Implementation checklist: no white background, vibrant neon accents used sparingly, text contrast 7:1+.
- Note: catalog uses `#000000` as canonical OLED black — ducat-lens uses `#0d0f14` (raised black with blue cast) which is the correct period translation.

**Pattern B — Cyberpunk UI (style catalog)**
- Source: styles.csv
- Convention: `0D0D0D` dark background, neon accents (green, cyan, magenta), terminal/HUD aesthetic, scanlines via `::before repeating-linear-gradient`, monospace fonts
- Accessibility note: catalog flags "Limited (dark+neon)" — accessibility requires manual contrast verification on all neon-on-surface pairs
- For ducat-lens: adopt structure (dark bg, neon chrome, scanlines) but deviate on palette (use 1999 Höllvania colors, not generic cyberpunk neons) and on saturation (desaturated accents, not full-brightness neon)

**Pattern C — Retro-Futurism (style catalog)**
- Source: styles.csv
- Convention: CRT scanlines as `::before` overlay, neon glow via `text-shadow + box-shadow`, glitch effects (skew/offset keyframes), monospace fonts
- For ducat-lens: adopt CRT scanlines (panel-scoped only, 5-8% opacity), adopt glow on interactive elements, skip glitch effects (not documented in 1999 UI spec) unless specifically for error states

**Ducat-lens selection:** Blend of OLED Dark (contrast discipline) + Cyberpunk UI (structural vocabulary) + Retro-Futurism (panel scanlines, glow). Deviate from catalog neon palette in favor of 1999 Höllvania tokens. Single-theme, no toggle.

---

## Summary Table

| Surface | Top Pattern | Source | Key Rule |
|---|---|---|---|
| Upload dropzone | Bordered interactive zone + scan-sweep status | ux-guidelines + styles | Disable zone during async; scan-sweep, not spinner |
| Results table | TanStack Table + shadcn DataTable | stacks/shadcn.csv | Semantic table structure required |
| Verdict badge | Color + text + border (never color-alone) | ux-guidelines (severity High) | Text label mandatory; 4.5:1 contrast minimum |
| Async status | Skeleton + aria-live + error recovery | ux-guidelines (severity High) | role="alert" for errors; "polite" for progress |
| Dark-mode UI | OLED Dark + Cyberpunk structure + 1999 palette | styles.csv | Panel-scoped scanlines; no ambient full-neon |
