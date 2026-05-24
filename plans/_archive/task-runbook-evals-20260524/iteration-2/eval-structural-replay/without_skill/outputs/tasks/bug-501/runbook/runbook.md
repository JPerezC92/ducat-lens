---
Phase: 2
Updated: 2026-05-24T00:00
SLA-due: 2026-05-30T18:00
Replay-candidate: structural
Hypotheses-outstanding: 1/3
Query-budget: 6/6
Same-query-reruns: 0/2
---

# Runbook

Task ID: bug-501
Module: auth.sso
Country: APAC
Environment: production
Symptom: Users in APAC production are being kicked back to the login screen about 90 seconds after SSO redirect; /api/me returns 401 with a valid-looking token.

## Prior-art finding

- **bug-401** (EU, resolved 2026-04-14): same symptom (~90s logout after SSO redirect, `/api/me` 401 with valid-looking token). Root cause: SSO token TTL 60s combined with minute-boundary cron scheduler racing token expiry. Fix: continuous timer with 30s pre-expiry margin.
- **bug-422** (US, resolved 2026-04-20): identical pattern to bug-401, surfaced because the original EU fix rollout did not cover US region. Same fix applied.
- **Verdict:** `structural` replay candidate. APAC is the third region exhibiting the same module + symptom signature. bug-422 already established the failure mode is "fix not rolled out per-region." High-confidence H1 below; needs config inspection to confirm vs refute before applying the bug-401 fix to APAC.

## Hypotheses

| # | Hypothesis | Supporting evidence | Confirm/refute |
|---|---|---|---|
| H1 | APAC `auth.sso` session-refresh still uses minute-boundary scheduler (bug-401 root cause, never rolled out to APAC) | bug-401 + bug-422 identical symptoms in two prior regions; bug-422 explicitly notes rollout was region-scoped | Inspect APAC session-refresh config; check scheduler type and pre-expiry margin |
