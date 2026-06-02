---
Status: active
Started: 2026-06-02 04:30
Subject: Add full-page atmospheric Warframe background image to landing page, CRT duotone filtered at low brightness to fill dead whitespace at wide viewports
Layout: subfolder pattern
---

# Plan — Add landing page background image

## Context

- Prompted by: User 2026-06-02 — at 1440px viewport the content column (~500px) leaves ~470px dead on each side. User wants background imagery to fill it.
- Goal: Full-page Warframe cinematic background applied as a fixed `body::before` layer, CRT-filtered at ~15% brightness. Hero figure removed (redundant once background active). Spacing irregularities fixed.
- Outcome: At any wide viewport the background fills with a dark atmospheric cinematic scene. Hero figure gone. Content readable. No new deps. Warframe 1999 CRT aesthetic preserved.

## Body

### Image strategy (updated 2026-06-02 — swapped during live session)

| Property | Value |
|---|---|
| Source | Digital Extremes CDN — `https://www-static.warframe.com/uploads/thumbnails/c5ab95fc8bd779f8379bc5e5b02aefe1_1600x900.jpg` (The New War key art, 1600×900 JPEG) |
| Output path | `frontend/public/images/bg-warframe.jpg` |
| Application | `body::before` pseudo-element — `position: fixed; inset: 0; z-index: -1; background-size: cover; background-position: center` |
| Filter | `grayscale(0.6) sepia(0.4) hue-rotate(160deg) brightness(0.15) saturate(2.5) contrast(1.2)` — dark atmospheric tint, CRT palette, texture not wallpaper |
| Blend | None — `mix-blend-mode: normal` (default) |
| Mobile | `@media (max-width: 767px) { body::before { display: none; } }` |
| z-index stack | `body::before` z-index: -1 → content z-index: 0 |

### Scope additions (Lumen holistic audit 2026-06-02)

| Fix | File | Change |
|---|---|---|
| Remove hero figure | `frontend/src/pages/index.astro` | Delete `<figure class="crt-duotone w-full max-w-sm mx-auto">` block (hero-prime.png) |
| Brightness correction | `frontend/src/styles/global.css` | `brightness(0.28)` → `brightness(0.15)` |
| Kiosk spacing | `frontend/src/pages/index.astro` | Remove `mt-3` from kiosk figure class |
| Upload spacing | `frontend/src/pages/index.astro` | Remove `mt-12` from upload section class |

### Branch strategy

Adds commits to existing feature branch `feat/frontend/add-crt-image-figures` (PR #12). PR auto-updates.

## Phase index — dispatch table

| # | Phase | Owner | Runbook | Output |
|---|---|---|---|---|
| 01 | Download bg image + write CSS + build | Forge 🔨 (Implementation Agent) → Atrium 🏛️ (Frontend Architect) auto-gate | `phase-01-forge.md` | `frontend/public/images/bg-warframe.jpg`, updated `global.css`, updated `index.astro` |
| 02 | Visual audit (readability + CRT fit + hero removal) | Atrium 🏛️ launches server → Lumen ✨ (Visual Director) audits → Atrium stops | `phase-02-lumen.md` | updated `knowledge/audits/lumen-images-20260527.md` |
| 03 | Commit + push (amend PR #12) | Herald 📯 (Release Manager) | `phase-03-herald.md` | new commit on `feat/frontend/add-crt-image-figures` |

## Critical files / tools

- `D:/projects/ducat-lens/frontend/src/styles/global.css` — `body::before` filter brightness fix
- `D:/projects/ducat-lens/frontend/public/images/bg-warframe.jpg` — The New War cinematic (already downloaded)
- `D:/projects/ducat-lens/frontend/src/pages/index.astro` — hero removal + spacing fixes
- Build cmd: `cd frontend && pnpm build`

## Verification

- ✅ phase-01 — `frontend/public/images/bg-warframe.jpg` exists, ≤ 500 KB (394 KB confirmed)
- ✅ phase-01 — `body::before` block in `global.css` `@layer base`: `position: fixed`, `z-index: -1`, CRT filter chain, mobile hide
- ✅ phase-01 — `pnpm build` exits 0
- ✅ phase-01 — Atrium 🏛️ (Frontend Architect) auto-gate PASS on `global.css`
- ✅ phase-02 — Lumen ✨ (Visual Director) initial audit PASS (zero Critical/High — bg renders, contrast intact, mobile hidden)
- ⬜ phase-01b — hero `<figure>` removed from `index.astro`; `brightness` corrected to `0.15`; `mt-3` + `mt-12` spacing removed
- ⬜ phase-01b — Atrium 🏛️ (Frontend Architect) auto-gate PASS on post-fix `index.astro` + `global.css`
- ⬜ phase-02b — Lumen ✨ (Visual Director) re-audit PASS (zero Critical/High; hero gone; brightness correct)
- ⬜ phase-03 — Herald 📯 (Release Manager) commits to feature branch; PR #12 updated; no AI attribution

## Out of scope

- New branch or new PR (adding to existing PR #12)
- Parallax or scroll animation on background
- Multiple background layers
- Any backend changes
- Mobile background (hidden at < 768px)

## Pending

- [waiting for] user to merge PR #12 before final merge

## Resolved decisions

- 2026-06-02 — Background image approach chosen over CSS-only
- 2026-06-02 — Background swapped from MagPrime PNG → The New War cinematic JPEG during live session. Reason: user wanted cooler image; cinematic art fills dead space better than character render
- 2026-06-02 — `body::before` pseudo-element, CSS-only, no HTML changes
- 2026-06-02 — Branch: add to existing `feat/frontend/add-crt-image-figures` (PR #12)
- 2026-06-02 — Hero figure removed (Path A per Lumen High-1). Reason: background IS the visual hero; character render in a box creates competing focal points and semantic collision with kiosk reference figure
- 2026-06-02 — `brightness(0.15)` locked (not 0.28). Reason: Lumen High-2 — 0.28 crosses wallpaper threshold; 0.15 keeps it as texture
