# Phase 01: Research @tanstack/react-table exact pin

## Owner

Augur 🔮 (Senior Research Analyst)

## Pre

- Brief approved (Cipher 🔓 (Dev-Team Orchestrator) confirmed user approval)
- Frontend stack already at React 19.2.6 + TS 6.0.3 + Astro 6.3.7

## Reads

- `frontend/package.json`: current pin baseline
- npm registry: `pnpm info @tanstack/react-table`
- TanStack docs (via context7 if needed)
- GitHub Advisory DB for any open CVEs

## Writes

- None directly. Updates plan.md `## Resolved decisions` via Cipher 🔓 (Dev-Team Orchestrator).

## Steps

1. Query npm: `pnpm info @tanstack/react-table version` from `D:\projects\ducat-lens\frontend\`
2. Confirm latest stable major (expect v8.x), exact patch version
3. Verify React 19 peer compatibility; check `peerDependencies.react` range on the published version
4. Verify license = MIT (or flag if not)
5. Check GitHub Advisory DB for any open CVEs on `@tanstack/react-table`
6. Cross-reference shadcn's recommended TanStack version (shadcn docs may state a minimum)

## Output

Single line for Cipher 🔓 (Dev-Team Orchestrator) to append to plan.md `## Resolved decisions`:
- `2026-05-25: @tanstack/react-table exact pin: X.Y.Z (license: MIT, React 19 peer: pass, CVE: clean). Augur 🔮 (Senior Research Analyst).`

## Gate

- Exact version is published on npm (no `next`/`alpha`/`beta` tags)
- React 19 peer compatibility confirmed
- License MIT (or explicit user acceptance if not)
- No critical CVEs

## Abort conditions

- TanStack v8 dropped React 19 support → halt; recommend alternative (e.g., react-table v7) to Cipher 🔓 (Dev-Team Orchestrator)
- License non-MIT/Apache/ISC/BSD → halt; surface to user
- Critical CVE found → halt; surface to user with severity + workaround
