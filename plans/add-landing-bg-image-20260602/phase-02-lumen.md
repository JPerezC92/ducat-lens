# Phase 02 — Visual audit (readability + CRT fit + bg render)

## Owner

Lumen ✨ (Visual Director)

## Pre

- Phase 01 Gate PASS (build green, Atrium 🏛️ PASS, `bg-warframe.png` in place)
- Dev server running at `http://localhost:4321/`. Atrium 🏛️ (Frontend Architect) launches via `cd frontend && pnpm dev`. Lumen attaches via `chrome-devtools` MCP only — never starts/stops server.

## Reads

- `frontend/src/styles/global.css` — verify `body::before` block
- `knowledge/audits/lumen-images-20260527.md` — prior audit to append/update

## Writes

- `knowledge/audits/lumen-images-20260527.md` — append "Re-audit 2026-06-02 background" section (do not overwrite; append only)

## Steps

1. Navigate to `http://localhost:4321/` via `mcp__chrome-devtools__navigate_page`
2. Full-page screenshot at 1440×900 via `mcp__chrome-devtools__take_screenshot`
3. Background render checks:
   - Background visible as faint accent-blue tinted silhouette in side margins
   - Content text contrast unaffected — run `getComputedStyle` spot-check on `h1`, `p`, `.text-text-muted` elements
   - No z-index conflict (content not hidden behind background layer)
   - `body::before` filter applied (verify via DevTools `getComputedStyle(document.querySelector('body::before')` indirect check or visual inspection)
4. Mobile check: resize to 375×812 → verify background is hidden (CSS `display: none` at < 768px) — no background image on mobile
5. WCAG AA contrast re-check: heading + body text contrast ratios still ≥ 4.5:1 against `--color-bg` (background must not reduce contrast)
6. Append findings to `knowledge/audits/lumen-images-20260527.md` under new `## Re-audit 2026-06-02 — Background image` section. Include: verdict, desktop screenshot, mobile screenshot, contrast spot-check results, severity table.
7. Notify Cipher 🔓 (Dev-Team Orchestrator) audit done; Cipher dispatches Atrium 🏛️ (Frontend Architect) to stop server.

## Output

- `knowledge/audits/lumen-images-20260527.md` — appended section with verdict

## Gate

- Zero Critical findings
- Zero High findings
- WCAG AA contrast ≥ 4.5:1 on all text elements (background must not reduce this below prior audit)
- Background hidden on mobile (375px) — verified via DevTools

## Abort conditions

- `mcp__chrome-devtools` unavailable → fall back to file-read checks + `pnpm agent-browser`; mark items "MANUAL VERIFY NEEDED"
- Background z-index conflict (content hidden) → halt, route fix to Forge 🔨 (Implementation Agent) via Cipher 🔓 (Dev-Team Orchestrator)
- Contrast regression below AA → halt, route fix to Forge 🔨 (Implementation Agent) (increase filter brightness reduction or add semi-opaque overlay)

## MCP whitelist/blacklist

- Allowed: `chrome-devtools` (all sub-tools)
- Forbidden: any edit to `frontend/src/` (Lumen never edits app code)
