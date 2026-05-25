# Phase 05: Implement DucatAnalyzer + 4 sub-components

## Owner

Forge 🔨 (Implementation Agent)

## Pre

- Phase 04 complete: Google Fonts wired
- shadcn components ready at `src/components/ui/{table,badge,skeleton,card}.tsx`
- `@tanstack/react-table` installed

## Reads

- `knowledge/design/phase-09-upload-ui-brief.md`: ENTIRE brief; ground truth for visual + behavioral spec
- `DESIGN.md`: token system + component anatomy
- `PRODUCT.md`: register=product, tone, anti-references
- `knowledge/research/warframe-1999-visual-spec.md`: visual research
- `backend/analyze.py`: `AnalyzeResult` shape + recommendation enum values
- `backend/main.py`: endpoint signature, CORS, FormData field name
- `frontend/src/components/ui/{table,badge,skeleton,card,button}.tsx`: base primitives
- `frontend/src/styles/global.css`: token vocabulary
- `frontend/.env.example` (if exists): env var conventions

## Writes

- `frontend/src/components/DucatAnalyzer.tsx`: REWRITE from stub
- `frontend/src/components/UploadZone.tsx`: NEW
- `frontend/src/components/ResultsTable.tsx`: NEW
- `frontend/src/components/RecommendationBadge.tsx`: NEW
- `frontend/src/components/AnalysisStatus.tsx`: NEW
- `frontend/.env.example`: NEW; documents `PUBLIC_API_URL=http://localhost:8000`
- `frontend/src/styles/global.css`: append `@keyframes scan-sweep` + reduced-motion fallback per brief §4.4

## Steps

1. Read brief in full first. Brief is exhaustive; do NOT improvise outside it.
2. Create `frontend/.env.example` with one line: `PUBLIC_API_URL=http://localhost:8000`
3. Append to `frontend/src/styles/global.css`; the `@keyframes scan-sweep` block + `.scan-line` class + `@media (prefers-reduced-motion: reduce)` fallback. Use EXACT CSS from brief §7 (Implementation Notes / `global.css` additions)
4. Implement `RecommendationBadge.tsx` first (smallest, no state)
   - Props: `{ verdict: "high-value sell" | "mid-value consider" | "low-value keep" }`
   - Map verdict → label (SELL/CONSIDER/KEEP) + Tailwind classes from brief §4.3
   - Use shadcn `Badge` primitive with custom `variant` via `cva` if needed
   - NO aria-label override needed; text label is inline per brief §4.3 Accessibility; badge is presentational
5. Implement `AnalysisStatus.tsx`
   - Props: `{ status: StatusState; onReset: () => void }` per brief §4.4 Status Indicators
   - 4 states: idle (returns null), loading (spinner + aria-live), error (panel with role="alert"), success (success banner above table; collapsed upload zone)
   - Spinner CSS animation gated by `prefers-reduced-motion` per brief
6. Implement `UploadZone.tsx`
   - Props: `{ onFile: (file: File) => void; isLoading: boolean; error?: string | null }`
   - Use `react-dropzone` 15.0.0 (already installed)
   - `accept: { 'image/png': ['.png'], 'image/jpeg': ['.jpg', '.jpeg'] }`, `multiple: false`
   - Deferred submit pattern: dropzone selects → filename shown → "ANALYZE" Button (shadcn) → parent submits
   - States: idle / drag-over / file-selected / uploading / error per brief §4.1
   - Corner brackets via CSS `::before`/`::after` per brief §4.1
   - Tailwind classes per brief (e.g., `bg-surface border border-accent-blue/40 focus-visible:ring-2 ring-accent-blue`)
7. Implement `ResultsTable.tsx`
   - Props: `{ items: ItemResult[]; totals: Totals }`
   - Use `useReactTable` from `@tanstack/react-table` with `getSortedRowModel`
   - Default sort: `ducats` desc
   - Sort buttons in `<th>` with keyboard support + aria-label per brief §4.4
   - Mobile breakpoint: ≤640px collapses to card layout (Tailwind `hidden md:table` + `block md:hidden` pattern)
   - Use shadcn `Table` primitive on desktop/tablet; custom card on mobile
   - High-value rows: background tint `bg-status-success/5` ONLY; NO `border-left` side stripe. Per Cipher 🔓 (Dev-Team Orchestrator) decision 2026-05-25 (Sentinel 🛡️ (Quality Guardian) audit resolution): impeccable absolute ban on `border-left` > 1px holds; SELL badge in ACTION column carries verdict signal alongside background tint. Apply EXACT class from brief §4.2 SELL row override.
   - Summary row: `ITEMS DETECTED / MATCHED / TOTAL DUCATS` per brief §4.2
   - Scan-sweep animation overlay on mount per brief §4.4 Status Indicators
8. Implement `DucatAnalyzer.tsx` (root island)
   - REWRITE the existing stub
   - State: `useState<File | null>`, `useState<StatusState>`, `useState<AnalyzeResult | null>`
   - On file selection: store file, await user clicking "ANALYZE"
   - On analyze: build FormData with field `image`, POST to `${import.meta.env.PUBLIC_API_URL}/analyze`, parse response
   - Error handling per plan §Backend contract: 422 = no Prime parts panel; 4xx/5xx = generic error panel; network error = same
   - Render `UploadZone` OR `AnalysisStatus(loading)` OR `<AnalysisStatus(success)> + <ResultsTable>` OR `AnalysisStatus(error)`
9. Verify all components use design tokens via Tailwind utility classes; NO inline `style`, NO hex literals
10. Verify NO em dashes (use commas/colons/semicolons per impeccable copy law)
11. Verify NO gradient text, NO glassmorphism, NO modal-first, NO identical card grids per impeccable absolute bans
12. Smoke test: `pnpm build` from `frontend/`; must exit 0
13. Smoke test dev server: `pnpm dev` from `frontend/`; open `http://localhost:4321`; verify upload zone renders with 1999 styling. KILL dev server after smoke check (no lingering processes).

## Output

- 5 new/rewritten components in `frontend/src/components/`
- `frontend/.env.example` with `PUBLIC_API_URL`
- Updated `frontend/src/styles/global.css` with scan-sweep keyframes
- `pnpm build` passing

## Gate

- All 5 components present + typed (TypeScript strict)
- DucatAnalyzer POSTs to `PUBLIC_API_URL/analyze` with FormData field `image`
- Sort works (click ducats column → desc/asc toggle)
- Mobile breakpoint renders cards not table
- `prefers-reduced-motion: reduce` disables scan sweep + spinner animation
- WCAG markup: `role="button"` on dropzone, `role="alert"` on error, `aria-live="polite"` on status, `<th scope="col">` on headers
- No em dashes anywhere in new code
- No `border-left` > 1px as accent stripe
- No `style={{...}}` attributes (Tailwind only)
- `pnpm build` exit 0

## Abort conditions

- Build fails → halt; report TypeScript or bundle errors
- Component count mismatch (any of 5 missing) → halt
- API call shape doesn't match backend (FormData field name wrong, etc.) → halt
- Impeccable absolute ban detected post-implementation (gradient text, side-stripe, modal) → halt; refactor before continuing

## MCP whitelist/blacklist

- Allowed: Bash for `pnpm build`, `pnpm dev` (must kill after smoke check)
- Allowed: context7 for React 19 / Astro 6 / tanstack-table API verification
- Forbidden: git; any backend file edits
