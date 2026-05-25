# Phase 07: Visual audit via agent-browser

## Owner

Lumen ✨ (Visual Director)

## Pre

- Phase 06 complete: build passes, types clean
- Dev server can be started for live audit

## Reads

- `frontend/src/components/*.tsx`
- `frontend/src/styles/global.css`
- `knowledge/design/phase-09-upload-ui-brief.md`
- `DESIGN.md`
- `PRODUCT.md`
- Rendered DOM via `agent-browser`

## Writes

- `knowledge/audits/phase-09-visual-audit-20260525.md`: audit report

## Steps

1. From `D:\projects\ducat-lens\frontend\`, start dev server: `pnpm dev` in background
2. Use `pnpm agent-browser` to navigate to `http://localhost:4321/`
3. Capture screenshots:
   - Desktop ≥1025px: empty state, file-selected state, mobile breakpoint
   - Tablet 641-1024px: empty state
   - Mobile ≤640px: empty state, card layout (uploaded results; use a fixture if backend not running)
4. Inspect computed styles for WCAG 2.2 AA contrast on rendered text + critical interactive elements
5. Verify motion: trigger `prefers-reduced-motion: reduce` via DevTools → confirm scan-sweep + spinner disabled
6. Verify against brief checklist:
   - Corner brackets on upload zone present
   - Cold blue accent only (no Orokin gold outside ducat values or logo)
   - Rajdhani Bold rendered on headings (font-family resolves correctly)
   - IBM Plex Mono on data cells
   - Roboto on body labels
   - No rounded corners >4px (radius-lg max)
   - No glassmorphism / gradient text / hero-metric template
   - No em dashes in copy
7. Run impeccable absolute-bans check on rendered DOM
8. Run impeccable "AI slop" first-order + second-order checks
9. Write audit report at `knowledge/audits/phase-09-visual-audit-20260525.md` with screenshots referenced + findings by severity
10. KILL dev server after audit complete (no lingering processes)

## Output

- Audit report at `knowledge/audits/phase-09-visual-audit-20260525.md`
- Gate signal: PASS / ADVISORY / BLOCK

## Gate

- 0 Critical/High visual issues
- 0 absolute-ban violations
- WCAG AA contrast verified on at least 6 critical token pairs against rendered DOM
- AI slop test passes both orders

## Abort conditions

- Critical visual issue (e.g., Orokin gold misused, accent blue wrong) → BLOCK; return to Forge 🔨 (Implementation Agent) with screenshots
- Absolute ban detected (gradient text, side-stripe accent >1px) → BLOCK
- Build doesn't render at all → halt; report to Cipher 🔓 (Dev-Team Orchestrator); reset to phase 06

## MCP whitelist/blacklist

- Allowed: Bash for `pnpm dev` (must kill after), `pnpm agent-browser *`
- Allowed: chrome-devtools MCP for visual + computed style + accessibility inspection
- Forbidden: git; editing `src/`
