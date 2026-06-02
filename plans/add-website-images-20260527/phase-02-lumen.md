# Phase 02 — Visual audit (CRT cohesion + a11y + LCP)

## Owner

Lumen ✨ (Visual Director)

## Pre

- Phase 01 Gate PASS (build green, Atrium 🏛️ (Frontend Architect) PASS, both `<img>` tags in place)
- Dev server running at `http://localhost:4321/`. Atrium 🏛️ (Frontend Architect) launches it via `cd frontend && pnpm dev` (Atrium owns the `pnpm dev` Bash grant per CLAUDE.md). Lumen ✨ (Visual Director) only attaches via `chrome-devtools` MCP — never starts/stops the server itself.

## Reads

- `frontend/src/pages/index.astro` — verify markup, alt text, dimension attrs
- `frontend/src/styles/global.css` — verify `.crt-duotone` filter values + scanline overlay + `prefers-reduced-motion` branch
- `knowledge/design/warframe-1999-visual-spec.md` (if present — design system source)
- `frontend/public/images/hero-prime.png` + `example-kiosk.jpg` — verify exist + dimensions match HTML attrs

## Writes

- `knowledge/audits/lumen-images-20260527.md` — visual audit report with severity-tagged findings (Critical / High / Medium / Low) + screenshots inline

## Steps

1. Load `http://localhost:4321/` via `mcp__chrome-devtools__navigate_page` — this both probes Atrium-launched server liveness AND opens the audit target page. If page does not load, halt and request Atrium 🏛️ (Frontend Architect) relaunch per Pre. (Lumen Bash grant scopes to `pnpm dlx impeccable *` + `pnpm agent-browser *` only — curl is not granted; use MCP for liveness check.)
2. Capture full-page screenshot via `mcp__chrome-devtools__take_screenshot`; embed in audit report.
3. CRT cohesion checks:
   - Verify hero image renders in accent-blue duotone (not full color) — sample pixel via DevTools or visual inspection
   - Verify scanlines visible at 1px stride
   - Verify 1px accent-blue border + sharp corners (border-radius matches existing cards = `--radius-sm`)
   - Verify NO drop shadows, NO rounded corners > radius-sm, NO color leak outside duotone palette
4. A11y checks:
   - Both `<img>` have non-empty `alt` (run `mcp__chrome-devtools__evaluate_script` to query)
   - Contrast: image surroundings preserve WCAG 2.2 AA for adjacent text
   - `prefers-reduced-motion` branch: emulate via `mcp__chrome-devtools__emulate` → verify scanline opacity adjusts, no animation kicks in
5. LCP / CLS check:
   - Run `mcp__chrome-devtools__performance_start_trace` → reload → `performance_stop_trace`
   - Read `mcp__chrome-devtools__performance_analyze_insight` for LCP element, LCP time, CLS score
   - Baseline (without new images): compare against previous `knowledge/audits/` if exists, else record this as baseline
   - Hero MUST be LCP candidate (eager + high priority); LCP regression ≤ 200 ms acceptable
   - CLS MUST be 0.00 (width/height attrs reserve layout)
6. Mobile viewport check: `mcp__chrome-devtools__resize_page` to 375×812; re-screenshot; verify images scale, don't break grid.
7. Write `knowledge/audits/lumen-images-20260527.md` with sections: Summary verdict, CRT cohesion findings, A11y findings, Performance findings, Screenshots (desktop + mobile + reduced-motion), Severity table, Recommendations. Re-check via `mcp__chrome-devtools__*` if any finding needs second look (server still up).
8. Notify Cipher 🔓 (Dev-Team Orchestrator) audit done; Cipher dispatches Atrium 🏛️ (Frontend Architect) to stop dev server (Atrium grant per CLAUDE.md).

## Output

- `knowledge/audits/lumen-images-20260527.md` — full audit report
- Verdict line at top: `PASS` | `PASS with Medium findings` | `BLOCK — Critical/High present`

## Gate

- Zero Critical findings
- Zero High findings
- LCP regression ≤ 200 ms vs prior baseline (or hero IS LCP and total LCP < 2.5 s)
- CLS == 0
- All `<img>` alt non-empty + descriptive (not "image" or filename)

## Abort conditions

- `mcp__chrome-devtools` server unavailable → halt, return to Cipher 🔓 (Dev-Team Orchestrator); fall back to manual screenshot via `pnpm agent-browser` per Bash registry
- Critical CRT cohesion break (e.g. duotone filter not applied, image renders full-color) → halt, route fix to Forge 🔨 (Implementation Agent) via Cipher 🔓 (Dev-Team Orchestrator)
- LCP regression > 200 ms → halt, route to Forge 🔨 (Implementation Agent) to add `<link rel="preload">` for hero in `BaseLayout.astro`

## MCP whitelist/blacklist

- Allowed: `chrome-devtools` (all sub-tools), `context7` (for design-system / a11y doc lookup if needed)
- Forbidden: any tool that edits `frontend/src/` (Lumen ✨ never edits app code — reports only)
