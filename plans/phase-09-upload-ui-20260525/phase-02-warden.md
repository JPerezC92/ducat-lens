# Phase 02: Vet @tanstack/react-table + shadcn component deps

## Owner

Warden 🔒 (Dependency Warden)

## Pre

- Phase 01 complete: Augur 🔮 (Senior Research Analyst) returned exact `@tanstack/react-table` pin
- shadcn CLI already installed (`shadcn@4.8.0` devDep)

## Reads

- `frontend/package.json`
- `frontend/pnpm-lock.yaml`
- Plan §Resolved decisions for the tanstack pin

## Writes

- None (read-only audit)

## Steps

1. Confirm `@tanstack/react-table@<pin>` exists on npm registry (`pnpm info`)
2. Run `pnpm audit` against current lockfile; baseline must be 0 vulns (PR #8 inherited state)
3. Audit transitive deps of `@tanstack/react-table`; flag any with critical/high CVEs
4. shadcn components (`table`, `badge`, `skeleton`, `card`); these are copy-paste local files, no new npm deps. Confirm via `pnpm dlx shadcn@4.8.0 add table --dry-run` if supported, OR inspect shadcn docs for which Radix primitives each component needs
5. Confirm Radix primitives needed by Table/Badge/Skeleton/Card are already in `radix-ui@1.4.3` meta-package (no additional `@radix-ui/*` adds)
6. License audit for `@tanstack/react-table`; must be MIT (Augur 🔮 (Senior Research Analyst) confirms in phase 01)

## Output

Gate signal: PASS / ADVISORY / BLOCK with one-line per finding

## Gate

- 0 critical CVEs on tanstack + transitive deps
- License OK
- No new Radix individual packages required (Nova preset uses meta-package)

## Abort conditions

- BLOCK signal → halt phase 09; report to Cipher 🔓 (Dev-Team Orchestrator); user must accept advisory or downgrade dep
- New Radix packages required outside meta-package → ADVISORY; surface to Cipher 🔓 (Dev-Team Orchestrator) for user acceptance before install

## MCP whitelist/blacklist

- Allowed: Bash for `pnpm audit`, `pnpm info`, `pnpm list`, `pnpm outdated`
- Forbidden: any `pnpm add` / `pnpm remove` / `pnpm install` (Warden 🔒 (Dependency Warden) never installs)
