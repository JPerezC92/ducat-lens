---
Status: completed
Started: 2026-05-25 14:00
Completed: 2026-05-25 14:30
Subject: Bump react 18→19, @types/react, @types/react-dom, typescript 5→6 to latest stable exact pins
Layout: subfolder pattern
---

# Plan — bump react 19 + typescript 6 frontend deps

## Context

- Prompted by: user request to address Astro deprecation backlog (pnpm outdated reported stale deps after PR #7 astro 6.3.7 merge)
- Goal: all 5 target packages at latest stable exact pins; pnpm build passes; 0 audit vulns
- Outcome: PR merged with react 19.2.6 + TS 6.0.3 + matching @types; no regressions on SEO artifacts

## Body

**Packages changing:**

| Package | From | To | Location |
|---|---|---|---|
| react | 18.3.1 | 19.2.6 | dependencies |
| react-dom | 18.3.1 | 19.2.6 | dependencies |
| @types/react | 18.3.29 | 19.2.15 | devDependencies |
| @types/react-dom | 18.3.7 | 19.2.3 | devDependencies |
| typescript | 5.9.3 | 6.0.3 | devDependencies |

**Packages unchanged (confirmed compatible):**

| Package | Version | Reason |
|---|---|---|
| astro | 6.3.7 | patched PR #7 |
| @astrojs/react | 5.0.5 | declares `react: "^17 || ^18 || ^19"` — already React 19 compatible |
| react-dropzone | 15.0.0 | latest; peerDep `>= 16.8` covers React 19 |
| @astrojs/sitemap | 3.7.2 | no React dep |
| agent-browser | 0.27.0 | dev tool, no React dep |

**Risk assessment:** MINIMAL. DucatAnalyzer.tsx has zero React hooks or API calls — no migration surface.

**TS 6 safety:** `astro/tsconfigs/base.json` already sets `moduleResolution: "Bundler"`, `strict: true`, `esModuleInterop: true` — all TS 6 defaults. No tsconfig changes needed.

## Phase index — dispatch table

| # | Phase | Owner | Runbook | Output |
|---|---|---|---|---|
| 01 | Edit package.json pins | Forge 🔨 | `phase-01-forge.md` | `frontend/package.json` updated |
| 02 | Install + build verify | Atrium 🏛️ | `phase-02-atrium.md` | `frontend/pnpm-lock.yaml` updated; `dist/` rebuilt |
| 03 | Dep audit | Warden 🔒 | `phase-03-warden.md` | 0 vulnerabilities confirmed |
| 04 | Commit + PR | Herald 📯 | `phase-04-herald.md` | PR URL |
| 05 | Test-plan verification | Inquisitor 🔎 | `phase-05-inquisitor.md` | All boxes ticked; PASS gate signal |

## Critical files / tools

- `frontend/package.json` — only file Forge edits
- `frontend/pnpm-lock.yaml` — updated by Atrium pnpm install
- `frontend/node_modules/astro/tsconfigs/base.json` — tsconfig TS 6 safety reference (read-only)
- Skill: `git-branch-name`, `git-commit`, `git-pr`

## Verification

- ✅ Phase 01: `frontend/package.json` has react/react-dom 19.2.6, @types/react 19.2.15, @types/react-dom 19.2.3, typescript 6.0.3 — all exact pins, no range operators
- ✅ Phase 02: `pnpm install` exits 0 (0 peer warnings); `pnpm build` exits 0 (1.65s); `dist/index.html` has JSON-LD + canonical + h1
- ✅ Phase 03: `pnpm audit` 0 vulnerabilities / 393 deps
- ✅ Phase 04: PR #8 opened (branch chore/frontend/bump-react19-typescript6); only package.json + pnpm-lock.yaml changed; no AI attribution
- ✅ Phase 05: all 8 PR test-plan checkboxes ticked [x]; Inquisitor PASS

## Out of scope

- @astrojs/react version bump (5.0.5 already supports React 19)
- react-dropzone bump (15.0.0 is latest; no upgrade available)
- react 19.x type migration (project has zero existing React APIs — no migration surface)
- tsconfig.json changes (Astro base already TS 6 compliant)
- Backend deps (Python/uv — not touched)

## Resolved decisions

- 2026-05-25 — @types/react target: 19.2.15 (not unspecified "latest") — confirmed via npm registry by Augur 🔮
- 2026-05-25 — @types/react-dom target: 19.2.3 — confirmed via npm registry by Augur 🔮
- 2026-05-25 — typescript 6.0.3: exists on npm (released 2026-03-23), confirmed by Augur 🔮
- 2026-05-25 — tsconfig: no changes needed — `astro/tsconfigs/base.json` already sets all TS 6 preferred options
