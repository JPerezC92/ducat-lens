# Phase 02 — Prior art

> **Owner:** Cipher
> **Pre:** Phase 01 complete
> **Reads:** prior-art catalog at `.claude/skills/task-runbook-workspace/_fixtures/prior-art/`
> **Writes:** prior-art finding block in runbook.md

## Steps

1. Scan prior-art directory for matches on identifier / module / symptom.
2. Note match-strength per hit:
   - bug-401 (EU, auth.sso): symptom signature identical (90s timeout, `/api/me` 401, valid-looking token). Strong match.
   - bug-422 (US, auth.sso): symptom signature identical; explicit related-to bug-401; rollout gap pattern. Strong match.
   - feature-001 (commerce.cart): unrelated module. No match.
3. Verdict: **structural replay** of bug-401/bug-422 root cause (minute-boundary scheduler race), APAC region untreated.

## Output

- Finding block in runbook.md (see "Prior-art finding" section).
- Replay-candidate header set to `structural`.

## Gate

- Replay-candidate field set to verdict (`structural`).

## Abort conditions

- Ambiguous match between two equally strong prior cases (N/A — both prior cases describe the same root cause and fix).
