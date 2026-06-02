---
Status: active
Started: 2026-05-27 13:00
Subject: Add hero showcase image + how-it-works example screenshot to landing page, filtered to match Warframe 1999 retro CRT aesthetic
Layout: subfolder pattern
---

# Plan — Add website images (CRT-filtered)

## Context

> Why is this being done? What prompted it? What is the intended outcome?

- Prompted by: User request 2026-05-27 — "can u add some images to the website please". Style constraint: "still following the warframe 1999 style".
- Goal: Two decorative images on landing page that reinforce the Warframe 1999 CRT terminal aesthetic, not break it.
- Outcome: Hero image above H1 + Ducat Kiosk example inside how-it-works step 1. Both rendered with heavy duotone CSS filter (grayscale + sepia + hue-rotate to `--color-accent-blue`) + scanline overlay + sharp 1px border. SEO preserved (alt text, lazy loading except hero LCP). Zero new deps. Zero backend changes.

## Body

### Surfaces

| # | Surface | File | Image source | Output path |
|---|---|---|---|---|
| 1 | Hero above H1 | `frontend/src/pages/index.astro` | WFCD CDN — Prime warframe full-body PNG with alpha (e.g. `LokiPrime.png`, 512×512, 97 KB verified) downloaded at phase-01 dispatch time, committed to `public/` | `frontend/public/images/hero-prime.png` |
| 2 | How-it-works step 1 | `frontend/src/pages/index.astro` | Repo-root `image.png` (existing Ducat Kiosk test fixture, 756×607, 692 KB) — re-encoded to JPEG q82 via backend Pillow to fit ≤ 500 KB cap | `frontend/public/images/example-kiosk.jpg` |

### CSS treatment (shared utility)

Single `.crt-duotone` utility class added to `frontend/src/styles/global.css`. Applies:

- `filter: grayscale(1) sepia(1) hue-rotate(160deg) saturate(2.5) contrast(1.1) brightness(0.85);` → image becomes 2-tone accent-blue CRT readout
- `::after` pseudo-element with repeating-linear-gradient scanlines @ 2px stripes, ~12% opacity, `mix-blend-mode: overlay`
- `border: 1px solid var(--border)` + `border-radius: var(--radius-sm)` to match existing card style
- `prefers-reduced-motion`: no animation; static filter only (no shimmer)

### Hero loading strategy

- Hero is LCP candidate → `loading="eager"` + `fetchpriority="high"` + explicit `width`/`height` attrs to reserve layout
- How-it-works example → `loading="lazy"` + `decoding="async"`

### Image licensing

- WFCD warframe-items: MIT — attribution not required for image redistribution, but `data/ducats.json` build script already cites repo; same source covers hero. Confirm in phase 01 step 1.
- `image.png` at repo root: user-owned screenshot (already test fixture).

## Phase index — dispatch table

| # | Phase | Owner | Runbook | Output |
|---|---|---|---|---|
| 01 | Source images + write CSS filter + edit page | Forge 🔨 (Implementation Agent) → Atrium 🏛️ (Frontend Architect) auto-gate | `phase-01-forge.md` | `frontend/public/images/hero-prime.png`, `frontend/public/images/example-kiosk.jpg`, updated `frontend/src/styles/global.css`, updated `frontend/src/pages/index.astro` |
| 02 | Visual audit (CRT cohesion + a11y + LCP) | Atrium 🏛️ (Frontend Architect) launches dev server → Lumen ✨ (Visual Director) audits via `chrome-devtools` MCP → Atrium stops server | `phase-02-lumen.md` | `knowledge/audits/lumen-images-20260527.md` with PASS / Critical / High list |
| 03 | Commit + branch + PR | Herald 📯 (Release Manager) | `phase-03-herald.md` | PR URL |
| 03-gate | Post-Herald PR-boundary review + test-plan verification | Cipher 🔓 (Dev-Team Orchestrator) dispatches Inquisitor 🔎 (PR Reviewer) | — (no runbook; orchestration only per CLAUDE.md test-plan gate) | Inquisitor verdict (PASS / ADVISORY / BLOCK) + `knowledge/audits/inquisitor-pr-XX-20260527.md` |

## Critical files / tools

- `D:/projects/ducat-lens/frontend/src/pages/index.astro` — landing page edit target
- `D:/projects/ducat-lens/frontend/src/styles/global.css` — add `.crt-duotone` utility
- `D:/projects/ducat-lens/frontend/public/images/` — new dir for static assets
- `D:/projects/ducat-lens/image.png` — repo-root Ducat Kiosk fixture, source for how-it-works (re-encoded)
- `D:/projects/ducat-lens/backend/` — uv env w/ Pillow used for re-encode (no new deps)
- `D:/projects/ducat-lens/plans/add-website-images-20260527/_crt-snippets.md` — verbatim CSS + Astro + Pillow blocks
- WFCD CDN: `https://cdn.warframestat.us/img/<imageName>.png` — hero source (redirects to `raw.githubusercontent.com/WFCD/warframe-items/master/data/img/<file>`)
- Build cmd: `cd frontend && pnpm build` (frontend is standalone — NO pnpm workspace filter)
- Skills: `plan-enforce` (this), `git-branch-name`, `git-commit`, `git-pr` (Herald)
- MCP: `chrome-devtools` (Lumen visual audit only — screenshot + lighthouse on LCP/CLS)

## Verification

- ✅ phase-01 — `frontend/public/images/hero-prime.png` exists, ≤ 300 KB, dimensions documented in runbook
- ✅ phase-01 — `frontend/public/images/example-kiosk.jpg` exists, ≤ 500 KB (JPEG q82 re-encode of `image.png`)
- ✅ phase-01 — `.crt-duotone` utility added to `global.css` with filter + scanline `::after` + border; works under `prefers-reduced-motion`
- ✅ phase-01 — `index.astro` renders hero `<img>` above H1 (eager+high-priority) + how-it-works `<img>` inside step 1 `<li>` (lazy). Both have descriptive `alt` text. Both wrapped to receive `.crt-duotone`.
- ✅ phase-01 — Atrium 🏛️ (Frontend Architect) auto-gate PASS on `index.astro` + `global.css` edits
- ✅ phase-02 — Lumen ✨ (Visual Director) audit returns PASS or zero Critical/High findings (Medium acceptable, logged for follow-up)
- ✅ phase-02 — Lighthouse LCP regression ≤ 200 ms vs baseline; CLS = 0 (explicit width/height verified)
- ⬜ phase-03 — Herald 📯 (Release Manager) opens PR via `gh pr create`; PR title + body free of AI attribution
- ⬜ phase-03-gate — Inquisitor 🔎 (PR Reviewer) returns PASS or ADVISORY; all test-plan checkboxes ticked via `gh pr edit --body-file`
- ⬜ phase-03-gate — User confirms PR ready before merge

## Out of scope

- Item-row thumbnails in results table (deferred — user picked only hero + how-it-works)
- OG / social-share image (deferred — user picked only hero + how-it-works)
- Backend changes (no `imageName` field added to `/analyze` response)
- New CSS/JS dependencies (filter is pure CSS)
- Image CDN proxy / runtime fetching (images committed to repo)
- Pixel-art / pixelated treatment (heavy duotone picked instead)
- Animation on images (static; no hover / no shimmer)

## Pending

- [decision needed at phase 01 step 1] Which WFCD Prime warframe `imageName` for hero — Forge 🔨 picks one of: `LokiPrime.png`, `MagPrime.png`, `RhinoPrime.png`, `NyxPrime.png`. Default: `LokiPrime.png` (already verified live in conversation). User may override.

## Resolved decisions

- 2026-05-27 — Scope locked to 2 surfaces: hero + how-it-works example (user picked via AskUserQuestion; rejected item thumbnails + OG image).
- 2026-05-27 — Treatment locked: heavy duotone (user picked over light tint + pixelated).
- 2026-05-27 — How-it-works source: reuse repo-root `image.png` (existing Ducat Kiosk test fixture) instead of sourcing new screenshot. Avoids licensing question + extra download.
- 2026-05-27 — Hero source: WFCD CDN `https://cdn.warframestat.us/img/<imageName>.png` (MIT license; verified live in conversation, e.g. `LokiPrime.png` HTTP 200).
- 2026-05-27 — Static commit to repo (no runtime CDN fetch). Reasons: deterministic LCP, no third-party request at page load, no SRI/CSP exposure.
- 2026-05-27 — Example image format: JPEG q82 (not PNG). Reason: source `image.png` = 692 KB PNG-optimized still exceeds 500 KB cap. JPEG q82 lands ~150-250 KB, lossless-enough for a CRT-filtered decorative image.
- 2026-05-27 — Re-encode tool: backend Pillow via `uv run`. Reason: Pillow already in backend deps; avoids `pnpm dlx sharp-cli` native-binary download risk.
- 2026-05-27 — Build cmd: `cd frontend && pnpm build` (NOT `pnpm --filter frontend build`). Reason: verified no `pnpm-workspace.yaml` exists; frontend is standalone package.
- 2026-05-27 — Hero visual fit confirmed: rendered duotone preview during plan verification. Loki Prime full-body render on transparent bg renders as accent-blue silhouette over `--color-bg`. Strong CRT-terminal feel. Earlier "tiny icon" concern (MED-4) cleared.
