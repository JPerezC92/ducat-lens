---
Status: completed
Started: 2026-05-25 17:00
Completed: 2026-05-25 22:30
Subject: Phase 09; frontend upload UI + results table + sell/keep recommendations (Warframe 1999 aesthetic)
Layout: subfolder pattern
---

# Plan: Phase 09 upload UI + results table

## Context

- Prompted by: bootstrap plan phase 09 (still ⬜); stack now ready (Tailwind v4 + shadcn radix-nova installed PR #?); user-approved design brief at `knowledge/design/phase-09-upload-ui-brief.md`
- Goal: ship `DucatAnalyzer.tsx` wired to POST `/analyze` with full Warframe 1999 / Höllvania UI; upload zone, sortable results table, sell/keep verdict badges, status indicators; responsive desktop/tablet/mobile, WCAG 2.2 AA
- Outcome: PR opened with single cohesive frontend deliverable; visible at `pnpm dev` on `/`; backend `/analyze` endpoint already shipped (PR #4)

## Body

### Scope

| Surface | Components | Source |
|---|---|---|
| Upload zone | `UploadZone.tsx` (react-dropzone + deferred submit) | brief §4.1 |
| Results table | `ResultsTable.tsx` (shadcn Table + tanstack-react-table sort) | brief §4.2 |
| Verdict badge | `RecommendationBadge.tsx` (shadcn Badge custom variants) | brief §4.3 |
| Status indicators | `AnalysisStatus.tsx` (loading/error/empty + aria-live) | brief §4.4 |
| Root island | `DucatAnalyzer.tsx` (state owner, POST `/analyze`) | brief §7 |

### Stack additions (exact pins required)

| Package | Why | Source |
|---|---|---|
| `@tanstack/react-table` | sortable + accessible table primitives | brief §5 |
| shadcn Table | UI table built on tanstack | brief §5 |
| shadcn Badge | verdict pill base | brief §5 |
| shadcn Skeleton | loading row placeholder | brief §5 |
| shadcn Card | optional container element | brief §5 |
| Google Fonts (CDN) | Rajdhani + IBM Plex Mono + Roboto via `<link>` | DESIGN.md §typography |

### Backend contract (Fact: `backend/analyze.py`, `backend/main.py`)

- Endpoint: `POST /analyze`
- Body: `FormData` with field `image` (PNG or JPEG)
- Response shape:
  ```ts
  interface AnalyzeResult {
    items: { name: string; ducats: number; recommendation: "high-value sell" | "mid-value consider" | "low-value keep" }[];
    totals: { items_detected: number; items_matched: number; ducats_sum: number };
  }
  ```
- 422 = no Prime parts detected
- CORS allows `http://localhost:4321` (dev origin)

## Phase index; dispatch table

| # | Phase | Owner | Runbook | Output |
|---|---|---|---|---|
| 01 | Research `@tanstack/react-table` exact pin | Augur 🔮 | `phase-01-augur.md` | pin recommendation in plan §Resolved decisions |
| 02 | Vet `@tanstack/react-table` + shadcn component deps | Warden 🔒 | `phase-02-warden.md` | PASS / ADVISORY / BLOCK |
| 03 | Install deps + add shadcn components | Forge 🔨 | `phase-03-forge.md` | `frontend/package.json` updated; `src/components/ui/{table,badge,skeleton,card}.tsx` created |
| 04 | Wire Google Fonts in BaseLayout | Forge 🔨 | `phase-04-forge.md` | `BaseLayout.astro` `<head>` updated |
| 05 | Implement DucatAnalyzer + 4 sub-components | Forge 🔨 | `phase-05-forge.md` | 5 React components implemented + `PUBLIC_API_URL` env support |
| 06 | Build + type verify | Atrium 🏛️ | `phase-06-atrium.md` | `pnpm build` exit 0; SEO markers preserved |
| 07 | Visual audit via agent-browser | Lumen ✨ | `phase-07-lumen.md` | screenshots + WCAG 2.2 AA contrast verification + audit report at `knowledge/audits/` |
| 08 | Post-install dep audit | Warden 🔒 | `phase-08-warden.md` | `pnpm audit` 0 vulns |
| 09 | Commit + branch + PR | Herald 📯 | `phase-09-herald.md` | PR URL |
| 10 | Test-plan verification gate | Inquisitor 🔎 | `phase-10-inquisitor.md` | all PR checkboxes `[x]`; PASS gate signal |

## Critical files / tools

- `frontend/src/components/DucatAnalyzer.tsx`: root island (will be rewritten from stub)
- `frontend/src/components/UploadZone.tsx`: NEW
- `frontend/src/components/ResultsTable.tsx`: NEW
- `frontend/src/components/RecommendationBadge.tsx`: NEW
- `frontend/src/components/AnalysisStatus.tsx`: NEW
- `frontend/src/components/ui/{table,badge,skeleton,card}.tsx`: NEW via shadcn CLI
- `frontend/src/layouts/BaseLayout.astro`: `<head>` Google Fonts `<link>`
- `frontend/src/pages/index.astro`: unchanged (DucatAnalyzer already wired with `client:load`)
- `frontend/.env.example`: NEW; documents `PUBLIC_API_URL`
- `knowledge/design/phase-09-upload-ui-brief.md`: design source of truth
- `knowledge/research/warframe-1999-visual-spec.md`: visual research source
- `PRODUCT.md` + `DESIGN.md`: product + design system context
- Skills: `git-branch-name`, `git-commit`, `git-pr`, `ui-ux-pro-max`, `impeccable`

## Verification

- ✅ Phase 01: Augur 🔮 (Senior Research Analyst) returns exact `@tanstack/react-table` pin (`8.21.3`)
- ✅ Phase 02: Warden 🔒 (Dependency Warden) PASS (`@tanstack/react-table@8.21.3` MIT + clean; no new Radix packages needed; `pnpm audit` 0 vulns)
- ✅ Phase 03: `frontend/package.json` shows `@tanstack/react-table@8.21.3` exact pinned; `ui/{table,badge,skeleton,card}.tsx` created; `pnpm build` exit 0
- ✅ Phase 04: `BaseLayout.astro` `<head>` carries preconnect + Google Fonts `<link>` (Rajdhani 700 + IBM Plex Mono 400/500 + Roboto 400/500); `pnpm build` exit 0
- ✅ Phase 05: 5 React components implemented (`DucatAnalyzer`, `UploadZone`, `ResultsTable`, `RecommendationBadge`, `AnalysisStatus`); `.env.example` created; `global.css` scan-sweep keyframes appended; `pnpm build` exit 0; smoke test PASS
- ✅ Phase 06: `pnpm build` exit 0; `pnpm tsc --noEmit` exit 0; `dist/index.html` carries `application/ld+json` + `canonical` + `<h1` (round 2 after Forge fixes)
- ✅ Phase 07: Lumen ✨ (Visual Director) round 2 ADVISORY (zero Critical/High after Forge fixes; 5 prior High RESOLVED; WCAG 2.2 AA contrast PASS on 9 pairs)
- ✅ Phase 08: Warden 🔒 (Dependency Warden) PASS (`pnpm audit` 0 vulns / 785 deps; tanstack pin matches; MIT clean; no postinstall scripts)
- ✅ Phase 09: PR #9 opened (`feat/frontend/phase-09-upload-ui`); commits `b89b00e` + `9302bf6`; zero AI attribution
- ✅ Phase 10: Inquisitor 🔎 (PR Reviewer) PASS; 14/14 test-plan boxes ticked with Fact-level evidence; zero violations on cross-cutting checks

## Out of scope

- Multi-image / batch upload
- Image preview or crop before submit
- Per-row explanation of recommendation reasoning
- User accounts, history, bookmarks, CSV export
- Light mode toggle (permanently dark Höllvania)
- PWA / offline support
- Internationalization
- Backend retry logic (UI shows error, user retries manually)
- Phase 10 of bootstrap plan (audit gates); separate plan

## Pending

- None at plan start. Phase blockers added here if they emerge mid-execution.

## Resolved decisions

- 2026-05-25: Design stack: shadcn/ui (`radix-nova` style) + Tailwind v4 + lucide-react. User pick.
- 2026-05-25: Color strategy: **Committed** (cold blue carries 30-60% of surface). Lumen ✨ (Visual Director) pick.
- 2026-05-25: Gold reserved for ducat values + logo only. User confirmed via brief approval.
- 2026-05-25: Scan sweep INCLUDED, gated `prefers-reduced-motion: no-preference`. Lumen ✨ (Visual Director) pick.
- 2026-05-25: Muted text token: `#6e7e9c` (~4.75:1 on `#0d0f14`, passes AA). Cipher 🔓 (Dev-Team Orchestrator) correction of Lumen ✨ (Visual Director)'s failed hypothesis `#5a6a82`.
- 2026-05-25: Theme: permanently dark; `:root` IS the dark theme; no `.dark` class toggle.
- 2026-05-25: `@tanstack/react-table` exact pin: `8.21.3` (license MIT; React 19 peer compat via `peerDependencies.react >=16.8`; clean of CVE-2026-45321 / GHSA-g7cv-rxg3-hmpx supply-chain incident — only `@tanstack/router` + `@tanstack/start` packages compromised, `@tanstack/table*` family unaffected; `8.21.3` predates the 2026-05-11 incident). Augur 🔮 (Senior Research Analyst).
