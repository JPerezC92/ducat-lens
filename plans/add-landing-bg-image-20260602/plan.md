---
Status: active
Started: 2026-06-02 04:30
Subject: Add full-page atmospheric Warframe background image to landing page, CRT duotone filtered at low brightness to fill dead whitespace at wide viewports
Layout: subfolder pattern
---

# Plan — Add landing page background image

## Context

- Prompted by: User 2026-06-02 — at 1440px viewport the content column (~500px) leaves ~470px dead on each side. User wants background imagery to fill it.
- Goal: Full-page Warframe character render applied as a fixed `body::before` background layer, CRT-duotone filtered at ~12% brightness. Atmospheric, not distracting. Content stays readable.
- Outcome: At any wide viewport the background fills with a faint accent-blue tinted Warframe silhouette. Content column readability unaffected. No new deps. Fits Warframe 1999 CRT aesthetic.

## Body

### Image strategy

| Property | Value |
|---|---|
| Source | WFCD CDN — `https://cdn.warframestat.us/img/MagPrime.png` (512×512 PNG, different from existing LokiPrime hero) |
| Output path | `frontend/public/images/bg-warframe.png` |
| Application | `body::before` pseudo-element — `position: fixed; inset: 0; z-index: -1; background-size: cover; background-position: center` |
| Filter | `grayscale(1) sepia(1) hue-rotate(160deg) brightness(0.12) saturate(3) contrast(1.5)` — extremely dark accent-blue tint; silhouette only visible |
| Blend | None — filter chain handles color conversion; `mix-blend-mode: normal` (default) |
| Reduced motion | No animation → no `prefers-reduced-motion` branch needed |
| z-index stack | `body::before` z-index: -1 → scanline `::after` z-index: auto → content z-index: 0 |

### Branch strategy

Adds commits to existing feature branch `feat/frontend/add-crt-image-figures` (PR #12). PR auto-updates. No new branch needed.

## Phase index — dispatch table

| # | Phase | Owner | Runbook | Output |
|---|---|---|---|---|
| 01 | Download bg image + write CSS + build | Forge 🔨 (Implementation Agent) → Atrium 🏛️ (Frontend Architect) auto-gate | `phase-01-forge.md` | `frontend/public/images/bg-warframe.png`, updated `global.css` |
| 02 | Visual audit (readability + CRT fit + LCP) | Atrium 🏛️ launches server → Lumen ✨ (Visual Director) audits → Atrium stops | `phase-02-lumen.md` | updated `knowledge/audits/lumen-images-20260527.md` |
| 03 | Commit + push (amend PR #12) | Herald 📯 (Release Manager) | `phase-03-herald.md` | new commit on `feat/frontend/add-crt-image-figures` |

## Critical files / tools

- `D:/projects/ducat-lens/frontend/src/styles/global.css` — add `body::before` block
- `D:/projects/ducat-lens/frontend/public/images/bg-warframe.png` — new background asset
- WFCD CDN: `https://cdn.warframestat.us/img/MagPrime.png` — bg source
- Build cmd: `cd frontend && pnpm build`

## Verification

- ✅ phase-01 — `frontend/public/images/bg-warframe.png` exists, ≤ 300 KB
- ✅ phase-01 — `body::before` block in `global.css`: `position: fixed`, `inset: 0`, `z-index: -1`, `background-size: cover`, CRT filter chain, no animation
- ✅ phase-01 — `pnpm build` exits 0, no missing-asset warnings
- ✅ phase-01 — Atrium 🏛️ (Frontend Architect) auto-gate PASS on `global.css`
- ✅ phase-02 — Lumen ✨ (Visual Director) audit: background renders as faint accent-blue tint; content text contrast unaffected; zero Critical/High findings
- ⬜ phase-03 — Herald 📯 (Release Manager) commits to feature branch; PR #12 updated; no AI attribution

## Out of scope

- New branch or new PR (adding to existing PR #12)
- Background on mobile (hide bg image on viewports < 768px via media query — mobile has no dead columns)
- Parallax or scroll animation on background
- Multiple background layers
- Any backend changes

## Pending

- [waiting for] user to merge PR #12 before final merge of this bg addition

## Resolved decisions

- 2026-06-02 — Background image approach chosen over CSS-only (user explicitly requested image background over pure CSS pattern)
- 2026-06-02 — MagPrime.png chosen as default (different from LokiPrime hero; same CRT duotone treatment)
- 2026-06-02 — `body::before` pseudo-element chosen over `BaseLayout.astro` `<div>` wrapper. Reason: zero HTML changes, pure CSS, no layout shift risk
- 2026-06-02 — Branch: add to existing `feat/frontend/add-crt-image-figures` (PR #12). Reason: same visual scope, one PR to review
- 2026-06-02 — Hide on mobile (< 768px). Reason: no dead columns on mobile; background adds no value and costs bandwidth
