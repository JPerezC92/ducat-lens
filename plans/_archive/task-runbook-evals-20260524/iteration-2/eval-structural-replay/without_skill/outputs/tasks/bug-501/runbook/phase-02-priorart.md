# Phase 02 — Prior art

> **Owner:** task lead
> **Pre:** Phase 01 complete
> **Reads:** prior-art catalog at `_fixtures/prior-art/`
> **Writes:** prior-art finding block in runbook.md; sets Replay-candidate

## Steps

1. Scanned prior-art directory for matches on module `auth.sso` + symptom "kicked back to login screen ~90s after SSO redirect, /api/me 401 with valid-looking token".
2. Hits: bug-401 (EU, exact-symptom match, resolved); bug-422 (US, exact-symptom + structural-rollout match, resolved). feature-001 unrelated (commerce.cart).
3. Pattern: same root cause has appeared in two prior regions because the fix rollout was region-scoped. APAC is the third region — high prior probability that the same minute-boundary scheduler is still in place.
4. Set Replay-candidate = `structural` (known fix exists; needs APAC config inspection to confirm before applying).

## Output

- Finding block in runbook.md citing bug-401 and bug-422
- H1 framed: APAC `auth.sso` session-refresh still on minute-boundary scheduler

## Gate

- Replay-candidate field set to `structural`
- At least one ranked hypothesis with confirm/refute path

## Abort conditions

- Ambiguous match between two equally strong prior cases (not applicable: bug-401/bug-422 point to same RC)

