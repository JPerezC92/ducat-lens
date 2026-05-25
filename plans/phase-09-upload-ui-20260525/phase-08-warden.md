# Phase 08: Post-install dep audit

## Owner

Warden 🔒 (Dependency Warden)

## Pre

- Phase 07 complete: visual audit PASS

## Reads

- `frontend/package.json`
- `frontend/pnpm-lock.yaml`

## Writes

- None (read-only audit)

## Steps

1. `cd D:\projects\ducat-lens\frontend`
2. `pnpm audit`; must show 0 vulnerabilities (critical + high + moderate + low)
3. `pnpm list @tanstack/react-table`; confirm exact version matches phase 01 pin
4. `pnpm outdated`; informational only; no action required if exact pins are intentional
5. Confirm no new transitive deps slipped in beyond Augur 🔮 (Senior Research Analyst)'s tanstack tree analysis

## Output

- `pnpm audit` stdout snapshot
- Gate signal: PASS / ADVISORY

## Gate

- 0 vulnerabilities total
- tanstack pin matches phase 01

## Abort conditions

- Any vulnerability found → halt; report severity + CVE to Cipher 🔓 (Dev-Team Orchestrator)
- Pin mismatch between phase 01 decision and actual installed version → halt

## MCP whitelist/blacklist

- Allowed: Bash for `pnpm audit`, `pnpm list`, `pnpm outdated`, `pnpm info`
- Forbidden: any install/remove command; git
