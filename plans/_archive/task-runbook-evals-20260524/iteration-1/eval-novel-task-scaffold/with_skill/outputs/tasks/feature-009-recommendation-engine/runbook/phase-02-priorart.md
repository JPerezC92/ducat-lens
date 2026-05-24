# Phase 02 — Prior art

> **Owner:** <fill>
> **Pre:** Phase 01 complete
> **Reads:** prior-art catalog
> **Writes:** prior-art finding block

## Steps

1. Scan prior-art directory for matches on identifier / module / symptom.
2. Note match-strength per hit.

## Output

- Finding block in runbook.md

## Gate

- Replay-candidate field set to verdict

## Abort conditions

- Ambiguous match between two equally strong prior cases
