# Phase 01 — Triage

> **Owner:** Cipher
> **Pre:** task spec read
> **Reads:** task metadata (bug-501, module auth.sso, country APAC, environment production)
> **Writes:** runbook.md classification fields

## Steps

1. Classify task: module `auth.sso`, region APAC, environment production.
2. Note identifying values: APAC region, production env, deadline 2026-05-30T18:00.
3. Set Replay-candidate per prior-art scan (Phase 02 result: `structural`).

## Output

- Updated runbook.md header with Task ID, Module, Symptom, SLA-due.

## Gate

- Module + identifying values populated.

## Abort conditions

- Insufficient task metadata to classify.
