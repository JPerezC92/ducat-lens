# Phase 01 — Triage

> **Owner:** task lead
> **Pre:** task spec read
> **Reads:** task metadata (bug-501 spec)
> **Writes:** runbook.md classification fields

## Steps

1. Classify: module `auth.sso`, region APAC, environment production.
2. Identifying values: ~90s post-SSO-redirect logout, `/api/me` returns 401 with valid-looking token.
3. SLA-due 2026-05-30T18:00 captured in header.

## Output

- runbook.md header populated with module / country / environment / SLA-due
- Symptom verbatim recorded

## Gate

- Module + identifying values populated
- SLA-due set

## Abort conditions

- Insufficient task metadata to classify

