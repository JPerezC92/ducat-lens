# Phase 01 — Triage

> **Owner:** investigation agent
> **Pre:** task spec read
> **Reads:** task metadata
> **Writes:** runbook.md classification fields

## Steps

1. Classify task by module/area. (auth.sso — set at scaffold time)
2. Note identifying values: country=APAC, environment=production.
3. Set Replay-candidate per prior-art scan. (structural — set at scaffold time, inherited from bug-401)

## Output

- Updated runbook.md header (populated at scaffold time)

## Gate

- Module + identifying values populated

## Abort conditions

- Insufficient task metadata to classify
