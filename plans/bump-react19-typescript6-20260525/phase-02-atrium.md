# Phase 02 — Install + build verify

## Owner

Atrium 🏛️ (Frontend Architect)

## Pre

- Phase 01 complete: `frontend/package.json` has 5 updated exact pins
- No active dev server running on :4321

## Reads

- `frontend/package.json` — updated pins
- `frontend/pnpm-lock.yaml` — prior lockfile (will be updated)

## Writes

- `frontend/pnpm-lock.yaml` — updated by pnpm install
- `frontend/node_modules/` — packages updated in place
- `frontend/dist/` — rebuilt by pnpm build

## Steps

1. `cd frontend && pnpm install` — resolve new lockfile; expect exit 0
2. Check for peer warnings; react-dropzone peerDep annotation for React 19 may emit warning — acceptable (functional compatibility confirmed)
3. `pnpm build` — rebuild dist/ with new deps; expect exit 0
4. Verify `dist/index.html` exists
5. Grep `dist/index.html` for: `application/ld+json` (JSON-LD), `canonical` (canonical link), `<h1` (h1 tag) — all three must be present

## Output

- `frontend/pnpm-lock.yaml` — updated lockfile with react 19 + ts 6 dep tree
- `frontend/dist/index.html` — rebuilt; contains JSON-LD + canonical + h1

## Gate

- `pnpm install` exit 0
- `pnpm build` exit 0
- `dist/index.html` contains all 3 SEO markers: `application/ld+json`, `canonical`, `<h1`

## Abort conditions

- `pnpm install` exits non-zero (peer conflict, resolution error) → halt, report full error to Cipher
- `pnpm build` exits non-zero (type error, bundle error) → halt, report full error + build log to Cipher
- `dist/index.html` missing any SEO marker → halt, report to Cipher (regression)
